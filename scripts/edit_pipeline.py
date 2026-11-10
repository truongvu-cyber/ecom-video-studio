"""Run the whole Editor pipeline, or resume from a step.

Usage: edit_pipeline.py <project> [--from <step>] [--to <step>] [--final] [--quality draft|looks|delivery]
Steps: validate inspect takes moments transcribe beats timeline plan render qc

The working loop for a revision (đổi use_sec, beats, overlay, override, nhạc):
  --from timeline --to plan   a few seconds: read edit/qc/plan.jpg, fix production.json, repeat
  --from timeline             renders the main version only (about a minute)
  --from timeline --final     once the cut is right: also the hook variants (about 40 s each)
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEPS = [
    ("validate", "validate.py"),
    ("inspect", "inspect_media.py"),
    ("takes", "takes_sheet.py"),
    ("moments", "find_moments.py"),
    ("transcribe", "transcribe.py"),
    ("beats", "beat_detect.py"),
    ("timeline", "build_timeline.py"),
    ("plan", "plan_sheet.py"),
    ("render", "render.py"),
    ("qc", "qc.py"),
]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--from", dest="start", default="validate", choices=[s for s, _ in STEPS])
    ap.add_argument("--to", dest="stop", default="qc", choices=[s for s, _ in STEPS])
    ap.add_argument("--quality", default="delivery")
    ap.add_argument("--final", action="store_true", help="xuất cả các biến thể hook (bản giao)")
    ap.add_argument("--no-variants", action="store_true", help="mặc định từ 2026-11-10; giữ để lệnh cũ còn chạy")
    args = ap.parse_args()

    names = [s for s, _ in STEPS]
    took: list[str] = []
    if names.index(args.stop) < names.index(args.start):
        sys.exit("--to đứng trước --from")
    for name, script in STEPS[names.index(args.start):names.index(args.stop) + 1]:
        print(f"\n=== {name} ===", flush=True)
        cmd = [sys.executable, str(HERE / script), args.project]
        if name == "render":
            cmd += ["--quality", args.quality]
            if not args.final:
                cmd.append("--no-variants")
        t0 = time.monotonic()
        if subprocess.run(cmd).returncode != 0:
            sys.exit(f"Dừng ở bước {name}")
        took.append(f"{name} {time.monotonic() - t0:.0f}s")
    print("\nThời gian: " + " · ".join(took))


if __name__ == "__main__":
    main()
