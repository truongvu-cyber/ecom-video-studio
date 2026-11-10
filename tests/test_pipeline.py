"""Smoke tests with assertions for the Editor pipeline and the generation gate.

Usage: .venv/bin/python -m unittest discover tests -v      (about 3 minutes, macOS only)
Builds the fake project (make_fixtures.py), copies it to a temp folder outside the repo and runs
the real pipeline on it. What is asserted is what broke before: frame-exact cuts, the frame
timing of the transitions, take selection, loudness, the schema gate and the creative-check gate.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
from common import loudness, media_info  # noqa: E402

PY = sys.executable
ENV = {**os.environ, "ALLOW_TEST_MUSIC": "1"}


def run(script: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run([PY, str(SCRIPTS / script), *args], capture_output=True, text=True, env=ENV)


_made = False


def fixtures() -> Path:
    """Build projects/demo-hoodie once per test run (clips, music, product.json, production.json)."""
    global _made
    if not _made:
        made = subprocess.run([PY, str(ROOT / "tests" / "make_fixtures.py")], capture_output=True, text=True)
        assert made.returncode == 0, made.stderr[-600:]
        _made = True
    return ROOT / "projects" / "demo-hoodie"


def frame_stats(video: Path) -> tuple[np.ndarray, np.ndarray]:
    """Per frame: mean brightness, and colour distance to the previous frame."""
    w, h = 36, 64
    raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", str(video), "-an", "-vf", f"scale={w}:{h}",
                          "-pix_fmt", "rgb24", "-f", "rawvideo", "-"], capture_output=True).stdout
    f = np.frombuffer(raw, dtype=np.uint8).reshape(-1, h, w, 3).astype(np.float32)
    return f.mean(axis=(1, 2, 3)), np.abs(np.diff(f, axis=0)).mean(axis=(1, 2, 3))


class Pipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        fixtures()
        cls.tmp = Path(tempfile.mkdtemp(prefix="evs-test-"))
        cls.project = cls.tmp / "demo-hoodie"
        shutil.copytree(ROOT / "projects" / "demo-hoodie", cls.project)
        cls.first = run("edit_pipeline.py", str(cls.project))
        cls.plan = json.loads((cls.project / "edit" / "edit-plan.json").read_text()) \
            if (cls.project / "edit" / "edit-plan.json").exists() else None
        cls.final = cls.project / "out" / "final_demo-hoodie.mp4"

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_1_pipeline_runs_and_writes_outputs(self) -> None:
        self.assertEqual(self.first.returncode, 0, self.first.stdout[-800:] + self.first.stderr[-800:])
        for name in ("final_demo-hoodie.mp4", "final_demo-hoodie_no-music.mp4", "preview_demo-hoodie.mp4", "edit-report.md"):
            self.assertTrue((self.project / "out" / name).exists(), name)
        qc = json.loads((self.project / "edit" / "qc" / "qc.json").read_text())
        self.assertNotEqual(qc["verdict"], "REJECT", qc)

    def test_2_take_selection(self) -> None:
        chosen = json.loads((self.project / "edit" / "media.json").read_text())["chosen"]
        self.assertEqual(chosen["c01*.mp4"], "c01_a.mp4", "the 1:1 take must lose")
        self.assertEqual(chosen["c03*.mp4"], "c03_b.mp4", "the take with a black head must lose")

    def test_3_cuts_are_frame_exact(self) -> None:
        fps = self.plan["fps"]
        info = media_info(self.final)
        self.assertEqual(round(info["duration"] * fps), round(self.plan["total_sec"] * fps))
        _, diff = frame_stats(self.final)
        found = [i + 1 for i, d in enumerate(diff) if d > 12]
        planned = [round(s["tl_start"] * fps) for s in self.plan["segments"][1:]]
        for cut in planned:
            self.assertIn(cut, found, f"no picture change on frame {cut}; changes at {found}")

    def test_4_cuts_land_on_beats(self) -> None:
        offs = [abs(c["off_ms"]) for c in self.plan["cuts"] if c.get("off_ms") is not None]
        self.assertTrue(offs and max(offs) <= 45, offs)

    def test_5_loudness(self) -> None:
        l = loudness(self.final)
        self.assertAlmostEqual(l["input_i"], -14.0, delta=1.5)
        self.assertLessEqual(l["input_tp"], -0.5)

    def test_6_transition_frames(self) -> None:
        p = self.project / "production.json"
        prod = json.loads(p.read_text())
        for s in prod["shots"]:
            s["transition"] = {"s02": "blackflash", "s04": "flicker", "s05": "wipe"}.get(s["id"], "cut")
        p.write_text(json.dumps(prod, ensure_ascii=False, indent=2))
        prod["variants"] = [{"id": "hookB", "overlay_overrides": {"s01": "New hook"}}]
        p.write_text(json.dumps(prod, ensure_ascii=False, indent=2))
        res = run("edit_pipeline.py", str(self.project), "--from", "timeline")
        self.assertEqual(res.returncode, 0, res.stdout[-800:] + res.stderr[-800:])
        # the working loop renders the main version only; approving without the variants is refused
        self.assertFalse((self.project / "out" / "final_demo-hoodie_hookB.mp4").exists())
        self.assertIn("hookB", run("approve.py", str(self.project)).stderr)
        self.assertTrue((self.project / "edit" / "qc" / "cuts.jpg").exists())
        plan = json.loads((self.project / "edit" / "edit-plan.json").read_text())
        fps = plan["fps"]
        start = {s["shot"]: round(s["tl_start"] * fps) for s in plan["segments"]}
        lum, _ = frame_stats(self.final)
        normal = float(np.median(lum[: start["s02"] - 3]))
        dark = normal * 0.15

        c = start["s02"]  # blackflash: exactly the two frames before the cut
        self.assertLess(max(lum[c - 2], lum[c - 1]), dark, lum[c - 4:c + 2])
        self.assertGreater(min(lum[c - 3], lum[c]), normal * 0.5, lum[c - 4:c + 2])

        a, b = start["s04"], start["s05"]  # flicker: dark from its first frame, four 2-frame blinks, each brighter
        shot = lum[a:b]
        self.assertLess(shot[0], dark)
        blinks = [i for i in range(1, len(shot)) if shot[i] > dark and shot[i - 1] <= dark]
        self.assertEqual(len(blinks), 4, shot.round(0))
        peaks = [shot[i] for i in blinks]
        self.assertEqual(peaks, sorted(peaks), peaks)
        self.assertLess(max(peaks), normal * 0.8)

        self.assertLess(lum[b], dark)  # wipe: covered on its first frame, open after 0.6 s
        self.assertGreater(lum[b + round(0.7 * fps)], lum[b + round(0.2 * fps)])


    def test_7_beats_and_plan_sheet(self) -> None:
        p = self.project / "production.json"
        prod = json.loads(p.read_text())
        want = {"s02": 4, "s04": 2.5}
        for s in prod["shots"]:
            s.pop("transition", None)
            if s["id"] in want:
                s["beats"] = want[s["id"]]
        p.write_text(json.dumps(prod, ensure_ascii=False, indent=2))
        before = self.final.stat().st_mtime
        res = run("edit_pipeline.py", str(self.project), "--from", "timeline", "--to", "plan")
        self.assertEqual(res.returncode, 0, res.stdout[-800:] + res.stderr[-800:])
        self.assertTrue((self.project / "edit" / "qc" / "plan.jpg").exists())
        self.assertEqual(self.final.stat().st_mtime, before, "--to plan must not render")
        plan = json.loads((self.project / "edit" / "edit-plan.json").read_text())
        beat = 60.0 / plan["music"]["bpm"]
        seg = {s["shot"]: s for s in plan["segments"]}
        cut = {c["after"]: c for c in plan["cuts"]}
        for sid, n in want.items():
            self.assertLessEqual(abs(cut[sid]["off_ms"]), 45, cut[sid])
            length = seg[sid]["tl_end"] - seg[sid]["tl_start"]
            # exactly n beats when the shot starts on the grid, never more than one beat short of it
            self.assertLessEqual(length, n * beat + 0.05, (sid, length))
            self.assertGreater(length, (n - 1) * beat, (sid, length))
        on_grid = abs(cut["s01"]["off_ms"]) <= 45
        if on_grid:
            self.assertAlmostEqual(seg["s02"]["tl_end"] - seg["s02"]["tl_start"], 4 * beat, delta=0.05)


class Gates(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="evs-gate-"))
        self.project = self.tmp / "p"
        (self.project / "edit").mkdir(parents=True)
        src = fixtures()
        for n in ("product.json", "production.json"):
            shutil.copy(src / n, self.project / n)

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_validate_rejects_bad_schema(self) -> None:
        p = self.project / "production.json"
        prod = json.loads(p.read_text())
        prod["stage"] = "brief"
        p.write_text(json.dumps(prod))
        res = run("validate.py", str(self.project), "--no-clips")
        self.assertEqual(res.returncode, 1)
        self.assertIn("stage", res.stdout)

    def test_validate_rejects_claim_without_evidence(self) -> None:
        p = self.project / "product.json"
        product = json.loads(p.read_text())
        product["claims"].append({"text": "Ships in 2 days", "evidence": ""})
        p.write_text(json.dumps(product))
        res = run("validate.py", str(self.project), "--no-clips")
        self.assertEqual(res.returncode, 1)
        self.assertIn("Ships in 2 days", res.stdout)

    def test_flow_run_stops_on_creative_check_fail(self) -> None:
        # no prompts.md -> creative_check fails -> nothing may reach the browser
        (self.project / "edit" / "gen_queue.json").write_text(json.dumps({"project_id": "p", "jobs": [
            {"kind": "video", "id": "c01", "prompt": "x", "refs": [], "save_as": "clips/c01_a.mp4"}]}))
        res = run("flow_run.py", str(self.project), "--dry-run")
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("creative_check FAIL", res.stdout + res.stderr)
        self.assertFalse((self.project / "edit" / "gen_log.jsonl").exists())

    def test_prompt_lint_knows_only_the_house_models(self) -> None:
        lint = ROOT / ".claude" / "skills" / "ad-creative" / "tools" / "prompt_lint.py"
        md = self.tmp / "p.md"
        md.write_text("## Clip 1 · 8s\n```\nMedium shot, static camera, soft window light. A hand sets a mug on a desk.\n```\n")
        ok = subprocess.run([PY, str(lint), str(md), "--model", "veo"], capture_output=True, text=True)
        self.assertNotIn("Unknown", ok.stdout + ok.stderr)
        bad = subprocess.run([PY, str(lint), str(md), "--model", "kling"], capture_output=True, text=True)
        self.assertIn("Unknown video model", bad.stdout + bad.stderr)


if __name__ == "__main__":
    unittest.main()
