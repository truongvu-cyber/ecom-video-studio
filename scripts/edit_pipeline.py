"""Run the whole Editor pipeline, or resume from a step.

Usage: edit_pipeline.py <project> [--from validate|inspect|moments|transcribe|beats|timeline|render|qc]
                                  [--quality draft|looks|delivery]

A revision (đổi use_sec, overlay, override, nhạc) usually only needs --from timeline.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEPS = [
    ("validate", "validate.py"),
    ("inspect", "inspect_media.py"),
    ("moments", "find_moments.py"),
    ("transcribe", "transcribe.py"),
    ("beats", "beat_detect.py"),
    ("timeline", "build_timeline.py"),
    ("render", "render.py"),
    ("qc", "qc.py"),
]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--from", dest="start", default="validate", choices=[s for s, _ in STEPS])
    ap.add_argument("--quality", default="delivery")
    ap.add_argument("--no-variants", action="store_true")
    args = ap.parse_args()

    names = [s for s, _ in STEPS]
    for name, script in STEPS[names.index(args.start):]:
        print(f"\n=== {name} ===", flush=True)
        cmd = [sys.executable, str(HERE / script), args.project]
        if name == "render":
            cmd += ["--quality", args.quality]
            if args.no_variants:
                cmd.append("--no-variants")
        if subprocess.run(cmd).returncode != 0:
            sys.exit(f"Dừng ở bước {name}")


if __name__ == "__main__":
    main()
