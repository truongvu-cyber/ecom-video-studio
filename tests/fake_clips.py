"""Generate stand-in clips for any project from its production.json, to test the
Creative -> Editor hand-off before real Veo clips exist.

Usage: fake_clips.py <project-id>
Dialogue clips speak all their shots' lines in order (macOS `say`), with pauses;
other clips get sfx. Writes clips/cNN_a.mp4. Never run it on a project whose
clips/ already holds real footage: it refuses if any cNN_a.mp4 exists.
"""
from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import soundfile as sf

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from common import load_json, project_dir  # noqa: E402
import make_fixtures as fx  # noqa: E402

COLORS = ["#3a5a8c", "#2f7d4f", "#6a3a8c", "#8c6a3a", "#3a7d7d", "#7d3a5a"]


def speech(lines: list[str], tmp: Path, sec: float = 8.0) -> np.ndarray:
    out = fx.ambient(sec)
    t = 0.5
    for i, line in enumerate(lines):
        aiff = tmp / f"l{i}.aiff"
        subprocess.run(["say", "-v", "Samantha", "-r", "180", "-o", str(aiff), line], check=True)
        wav = tmp / f"l{i}.wav"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(aiff), "-ar", str(fx.SR), "-ac", "1", str(wav)], check=True)
        y, _ = sf.read(wav, dtype="float32")
        s = int(t * fx.SR)
        out[s:s + len(y)] += y[: max(0, len(out) - s)] * 0.8
        t += len(y) / fx.SR + 0.5
    return out


def main() -> None:
    project = project_dir(sys.argv[1])
    prod = load_json(project / "production.json")
    clips: dict[str, list[dict]] = {}
    for s in prod["shots"]:
        clips.setdefault(re.match(r"(c\d+)", s["file_pattern"]).group(1), []).append(s)
    if any((project / "clips" / f"{c}_a.mp4").exists() for c in clips):
        sys.exit("clips/ đã có clip thật, không ghi đè")
    fx.PROJECT = project
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        for k, (name, shots) in enumerate(sorted(clips.items())):
            lines = [s["dialogue"] for s in shots if s["audio_type"] == "dialogue"]
            audio = speech(lines, tmp) if lines else fx.sfx_track(8.0)
            label = f"{name.upper()}\n{shots[0]['role'].upper()}"
            fx.make_clip(f"{name}_a", label, COLORS[k % len(COLORS)], audio, tmp=tmp)
            print(f"{name}_a.mp4: {' / '.join(lines) if lines else 'sfx'}")


if __name__ == "__main__":
    main()
