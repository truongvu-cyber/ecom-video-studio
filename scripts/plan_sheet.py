"""The edit plan as one picture, before anything is rendered -> edit/qc/plan.jpg

Usage: plan_sheet.py <project>
One cell per shot: the first, middle and last frame of exactly the source window the plan will
use, the band the overlay text will sit in, the transition into the shot and how far its cut is
from the beat. Read it before rendering: a wrong window, text over a face or an off-beat cut is
fixed in production.json in seconds here, instead of after a render.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from build_timeline import BANDS, SNAP_TOL
from common import load_json, project_dir

FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FW = 150  # width of one frame
RED, YELLOW, WHITE = "#ff3b30", "#ffd60a", "#ffffff"


def main() -> None:
    project = project_dir(sys.argv[1])
    plan = load_json(project / "edit" / "edit-plan.json")
    w, h = plan["width"], plan["height"]
    fh = int(FW * h / w)
    head = 40
    cell_w, cell_h = FW * 3 + 8, fh + head
    segs = plan["segments"]
    cols = min(3, len(segs))
    rows = (len(segs) + cols - 1) // cols
    canvas = Image.new("RGB", (cols * cell_w, rows * cell_h + 26), "#111")
    font, small = ImageFont.truetype(FONT, 15), ImageFont.truetype(FONT, 12)
    off = {c["after"]: c for c in plan["cuts"]}
    text = {o["shot"]: o for o in plan["overlays"]}
    crop = f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},scale={FW}:{fh}"
    bad = 0
    with tempfile.TemporaryDirectory() as td:
        for k, s in enumerate(segs):
            x0, y0 = (k % cols) * cell_w, (k // cols) * cell_h
            d = ImageDraw.Draw(canvas)
            src = project / "clips" / s["take"]
            span = s["src_out"] - s["src_in"]
            for j, f in enumerate((0.0, 0.5, 1.0)):
                t = s["src_in"] + max(0.0, span * f - (0.05 if f == 1.0 else 0))
                p = Path(td) / f"{k}_{j}.jpg"
                subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", str(src),
                                "-frames:v", "1", "-vf", crop, "-q:v", "4", str(p)])
                if p.exists():
                    canvas.paste(Image.open(p), (x0 + j * FW, y0 + head))
                else:
                    d.rectangle([x0 + j * FW, y0 + head, x0 + (j + 1) * FW - 1, y0 + head + fh], outline=RED)
                    d.text((x0 + j * FW + 6, y0 + head + 6), "không đọc được frame", font=small, fill=RED)
                    bad += 1
            o = text.get(s["shot"])
            if o:  # where the text will sit, on every frame of the shot
                a, b = BANDS.get(o["pos"], BANDS["top"])
                for j in range(3):
                    d.rectangle([x0 + j * FW + 6, y0 + head + int(a * fh), x0 + (j + 1) * FW - 7, y0 + head + int(b * fh)],
                                outline=YELLOW, width=2)
                d.text((x0 + 10, y0 + head + int(a * fh) + 3), o["text"].replace("*", "")[:26], font=small, fill=YELLOW)
            c = off.get(s["shot"])
            beat = ""
            colour = WHITE
            if c and c["off_ms"] is not None:
                beat = f" · cắt {c['off_ms']:+d}ms"
                if abs(c["off_ms"]) > SNAP_TOL * 1000:
                    colour = RED
                    bad += 1
            d.text((x0 + 4, y0 + 3), f"{s['shot']} {s['take']} {s['src_in']:.2f}-{s['src_out']:.2f}"
                   + (f" x{s['speed']}" if s["speed"] != 1 else ""), font=font, fill=WHITE)
            d.text((x0 + 4, y0 + 21), f"tl {s['tl_start']:.2f}-{s['tl_end']:.2f} ({s['tl_end'] - s['tl_start']:.2f}s) · "
                   f"{s.get('transition') or 'cut'}{beat}", font=small, fill=colour)
        ImageDraw.Draw(canvas).text((4, rows * cell_h + 5), f"{plan['project_id']} · {plan['total_sec']}s · khung vàng = vị trí chữ · "
                                    f"đỏ = cắt lệch beat hoặc lỗi · hiệu ứng {plan['effects']['used']}/{plan['effects']['cuts']} nhát cắt "
                                    f"(hạn mức {plan['effects']['budget']}) · {len(plan['issues'])} chú ý", font=small, fill=WHITE)
    dest = project / "edit" / "qc" / "plan.jpg"
    dest.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(dest, quality=88)
    print(f"-> edit/qc/plan.jpg ({len(segs)} cảnh, {bad} chỗ đỏ) — đọc ảnh này trước khi render")


if __name__ == "__main__":
    main()
