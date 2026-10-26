"""One frame per second of every clip in clips/ -> edit/qc/takes.jpg

Usage: takes_sheet.py <project>
The sheet is how the agent (and the user) read a clip before cutting it:
which second holds which action, where lettering drifts, where the camera moves.
Runs after inspect so it covers every take, chosen or not.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from common import media_info, project_dir

FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
TW = 180
STEP = 1.0


def main() -> None:
    project = project_dir(sys.argv[1], need_production=False)
    clips = sorted((project / "clips").glob("c*.mp4"))
    if not clips:
        sys.exit("Không có clip trong clips/")
    font = ImageFont.truetype(FONT, 18)
    rows = []
    with tempfile.TemporaryDirectory() as td:
        for r, c in enumerate(clips):
            info = media_info(c)
            th = int(TW * info["height"] / info["width"])
            times = [0.2] + [t for t in frange(STEP, info["duration"] - 0.3, STEP)] + [round(info["duration"] - 0.2, 2)]
            row = Image.new("RGB", (TW * len(times), th + 26), "#111")
            for k, t in enumerate(times):
                f = Path(td) / f"{r}_{k}.jpg"
                subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", str(c),
                                "-frames:v", "1", "-q:v", "4", str(f)], check=True)
                row.paste(Image.open(f).resize((TW, th)), (k * TW, 26))
                ImageDraw.Draw(row).text((k * TW + 4, 4), f"{c.stem} {t:.1f}s", font=font, fill="white")
            rows.append(row)
    sheet = Image.new("RGB", (max(r.width for r in rows), sum(r.height for r in rows)), "#111")
    y = 0
    for r in rows:
        sheet.paste(r, (0, y))
        y += r.height
    out = project / "edit" / "qc" / "takes.jpg"
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, quality=85)
    print(f"{len(clips)} clip -> {out.relative_to(project)}")


def frange(a: float, b: float, step: float):
    t = a
    while t < b:
        yield round(t, 2)
        t += step


if __name__ == "__main__":
    main()
