"""Final QC gate: technical checks + contact sheets + edit-report.md

Usage: qc.py <project>
Verdict: PASS (all automatic checks fine), REVIEW (something a person must look at,
including every strict print-fidelity shot), REJECT (file is broken or off-spec).
The agent must still look at edit/qc/*.jpg itself before handing over.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from common import load_json, loudness, media_info, project_dir, save_json

FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
THUMB_W = 270


def grab(video: Path, t: float, dest: Path) -> Path:
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", str(video),
                    "-frames:v", "1", "-q:v", "3", str(dest)], check=True)
    return dest


def sheet(video: Path, times: list[tuple[float, str]], plan: dict, dest: Path) -> None:
    """Thumbnails with the safe zone drawn in, labelled by time."""
    font = ImageFont.truetype(FONT, 16)
    thumb_h = int(THUMB_W * plan["height"] / plan["width"])
    cols = min(6, len(times))
    rows = (len(times) + cols - 1) // cols
    canvas = Image.new("RGB", (cols * THUMB_W, rows * (thumb_h + 24)), "#111")
    top = int(thumb_h * plan["safe_zone"].get("top", 0.15))
    bottom = thumb_h - int(thumb_h * plan["safe_zone"].get("bottom", 0.20))
    with tempfile.TemporaryDirectory() as td:
        for i, (t, label) in enumerate(times):
            img = Image.open(grab(video, t, Path(td) / f"{i}.jpg")).resize((THUMB_W, thumb_h))
            d = ImageDraw.Draw(img)
            d.line([(0, top), (THUMB_W, top)], fill="#ff3b30", width=2)
            d.line([(0, bottom), (THUMB_W, bottom)], fill="#ff3b30", width=2)
            x, y = (i % cols) * THUMB_W, (i // cols) * (thumb_h + 24)
            canvas.paste(img, (x, y + 24))
            ImageDraw.Draw(canvas).text((x + 6, y + 3), f"{t:.2f}s {label}", font=font, fill="white")
    dest.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(dest, quality=88)


def main() -> None:
    project = project_dir(sys.argv[1])
    prod = load_json(project / "production.json")
    plan = load_json(project / "edit" / "edit-plan.json")
    pid = plan["project_id"]
    final = project / "out" / f"final_{pid}.mp4"
    nomusic = project / "out" / f"final_{pid}_no-music.mp4"
    outputs = [p for p in (final, nomusic) if p.exists()]
    reject, review, notes = [], [], []

    if not outputs:
        reject.append("Không có file xuất trong out/")
    target_i = plan["audio"].get("target_lufs", -14)
    target_tp = plan["audio"].get("true_peak_db", -1)
    for out in outputs:
        info = media_info(out)
        if (info.get("width"), info.get("height")) != (plan["width"], plan["height"]):
            reject.append(f"{out.name}: kích thước {info.get('width')}x{info.get('height')}")
        if abs(info.get("fps", 0) - plan["fps"]) > 0.05:
            reject.append(f"{out.name}: fps {info.get('fps')}")
        if info.get("vcodec") != "h264" or info.get("pix_fmt") != "yuv420p":
            reject.append(f"{out.name}: codec {info.get('vcodec')}/{info.get('pix_fmt')}")
        if not info["has_audio"]:
            reject.append(f"{out.name}: mất tiếng")
        if abs(info["duration"] - plan["total_sec"]) > 0.15:
            review.append(f"{out.name}: dài {info['duration']:.2f}s, kế hoạch {plan['total_sec']}s")
        loud = loudness(out)
        if loud["input_i"] is None or abs(loud["input_i"] - target_i) > 1.0:
            review.append(f"{out.name}: loudness {loud['input_i']} LUFS (mục tiêu {target_i})")
        if loud["input_tp"] is not None and loud["input_tp"] > target_tp + 0.5:
            review.append(f"{out.name}: true peak {loud['input_tp']} dBTP")
        notes.append(f"{out.name}: {info['width']}x{info['height']} {info['fps']}fps "
                     f"{info['duration']:.2f}s, {loud['input_i']} LUFS, TP {loud['input_tp']}")

    for c in plan["cuts"]:
        if c["on_beat"] is False:
            notes.append(f"Cắt sau {c['after']} lệch beat {c['off_ms']}ms (ưu tiên giữ lời thoại)")
    for msg in plan["issues"]:
        review.append(msg)
    strict = [s for s in plan["segments"] if s.get("print_fidelity") == "strict"]
    for s in strict:
        review.append(f"{s['shot']}: cảnh có hình in — so frame với file thiết kế trước khi duyệt")

    qc_dir = project / "edit" / "qc"
    if outputs:
        video = outputs[0]
        times = []
        for s in plan["segments"]:
            mid = (s["tl_start"] + s["tl_end"]) / 2
            times += [(s["tl_start"] + 0.08, f"{s['shot']} vào"), (mid, s["shot"])]
        for o in plan["overlays"]:
            times.append((o["start"] + 0.4, f"chữ {o['shot']}"))
        times = sorted(times)
        sheet(video, times, plan, qc_dir / "sheet.jpg")
        for s in strict:
            grab(video, (s["tl_start"] + s["tl_end"]) / 2, qc_dir / f"print_{s['shot']}.jpg")

    verdict = "REJECT" if reject else ("REVIEW" if review else "PASS")
    lines = [f"# Edit report — {pid}", "", f"**Kết luận QC: {verdict}**", ""]
    if reject:
        lines += ["## Lỗi chặn (REJECT)", *[f"- {r}" for r in reject], ""]
    if review:
        lines += ["## Cần người xem (REVIEW)", *[f"- {r}" for r in review], ""]
    lines += ["## File xuất", *[f"- {n}" for n in notes], ""]
    lines += ["## Dựng", "| Shot | Take | Trong clip | Trên timeline | Âm thanh |", "|---|---|---|---|---|"]
    for s in plan["segments"]:
        lines.append(f"| {s['shot']} | {s['take']} | {s['src_in']:.2f}–{s['src_out']:.2f}s "
                     f"| {s['tl_start']:.2f}–{s['tl_end']:.2f}s | {s['audio_type']} |")
    m = plan["music"]
    lines += ["", "## Nhạc"]
    if m.get("file"):
        lines += [f"- {Path(m['file']).name} — {m.get('bpm')} BPM, vào lúc {m['delay']}s, "
                  f"phát từ giây {m['offset']} của bài; drop {m.get('drop_sec')}s",
                  f"- Nguồn/license: {m.get('license')}",
                  f"- Điểm cắt trúng beat: {sum(1 for c in plan['cuts'] if c['on_beat'])}/"
                  f"{sum(1 for c in plan['cuts'] if c['on_beat'] is not None)}"]
    else:
        lines.append("- Không dùng nhạc")
    takes = load_json(project / "edit" / "media.json")["takes"]
    rejected = [f"{f} ({'; '.join(a['issues'])})" for f, a in takes.items() if a["reject"]]
    if rejected:
        lines += ["", "## Take bị loại", *[f"- {r}" for r in rejected]]
    lines += ["", "Ảnh kiểm tra: `edit/qc/sheet.jpg`" + (", `edit/qc/print_*.jpg`" if strict else "")]
    (project / "out" / "edit-report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    save_json(qc_dir / "qc.json", {"verdict": verdict, "reject": reject, "review": review, "notes": notes})
    if verdict != "REJECT" and prod.get("stage") != "approved":
        prod["stage"] = "rendered"
        save_json(project / "production.json", prod)

    print(f"QC: {verdict}")
    for r in reject + review:
        print(" -", r)
    if verdict == "REJECT":
        sys.exit(1)


if __name__ == "__main__":
    main()
