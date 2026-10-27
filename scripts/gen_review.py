"""Review sheet for generated assets + written pass/fail marks (keyframes.md §5b).

Usage:
  gen_review.py <project>                       -> edit/qc/gen_review.jpg + prints the checks
  gen_review.py <project> --mark <job> pass|fail "<why>"   -> appends to edit/gen_review.jsonl

The sheet shows every keyframe (frames/keyframe_c*.png) and every clip (clips/c*.mp4, one
frame per second) with the checks that apply under it: product.json `placement_checks`
(every asset) + the prompt's "Soát trước khi làm video" (keyframe N) / "Soát clip" (clip N).
A clip with no `pass` mark is reported by validate.py; the agent marks after reading the sheet,
and a fail is fixed (prompt sentence rewritten, `flow_run.py --only <job>`) before the next stage.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from common import load_json, media_info, project_dir

FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_R = "/System/Library/Fonts/Supplemental/Arial.ttf"
TW = 180          # width of one clip frame
KW = 300          # width of one keyframe
SHEET_W = 1800


def field(block: str, *names: str) -> str:
    for n in names:
        m = re.search(r"\*\*%s[^*]*\*\*:?\s*(.+)" % re.escape(n), block)
        if m:
            return m.group(1).strip()
    return ""


def sections(md: str, pattern: str) -> list[tuple[str, str]]:
    out, cur, buf = [], None, []
    for line in md.splitlines():
        if re.match(pattern, line) or re.match(r"^##", line):
            if cur is not None:
                out.append((cur, "\n".join(buf)))
            cur, buf = (line, []) if re.match(pattern, line) else (None, [])
            continue
        if cur is not None:
            buf.append(line)
    if cur is not None:
        out.append((cur, "\n".join(buf)))
    return out


def checks_from_prompts(project: Path) -> dict[str, list[str]]:
    """{'keyframe_c1': [...], 'c01': [...]} from prompts.md."""
    md = (project / "prompts.md").read_text(encoding="utf-8") if (project / "prompts.md").exists() else ""
    out: dict[str, list[str]] = {}
    for head, body in sections(md, r"^### (Keyframe|Khung) *\d+"):
        n = int(re.search(r"(\d+)", head).group(1))
        out[f"keyframe_c{n}"] = [c.strip() for c in field(body, "Soát trước khi làm video", "Check before animating").split("·") if c.strip()]
    for head, body in sections(md, r"^## Clip *\d+"):
        n = int(re.search(r"(\d+)", head).group(1))
        out[f"c{n:02d}"] = [c.strip() for c in field(body, "Soát clip", "Check clip").split("·") if c.strip()]
    return out


def wrap(draw, text: str, font, width: int) -> list[str]:
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def marks(project: Path) -> dict[str, dict]:
    p = project / "edit" / "gen_review.jsonl"
    out: dict[str, dict] = {}
    if p.exists():
        for line in p.read_text().splitlines():
            if line.strip():
                j = json.loads(line)
                out[j["job"]] = j  # last mark wins
    return out


def build(project: Path) -> Path:
    product = load_json(project / "product.json") if (project / "product.json").exists() else {}
    placement = product.get("placement_checks", [])
    checks = checks_from_prompts(project)
    done = marks(project)
    font, small = ImageFont.truetype(FONT, 20), ImageFont.truetype(FONT_R, 16)
    blocks: list[Image.Image] = []

    def caption(label: str, items: list[str], width: int) -> Image.Image:
        probe = ImageDraw.Draw(Image.new("RGB", (1, 1)))
        lines = [(label, font)]
        for it in items:
            for k, l in enumerate(wrap(probe, it, small, width - 30)):
                lines.append((("• " if k == 0 else "  ") + l, small))
        h = 8 + sum(26 if f is font else 20 for _, f in lines)
        img = Image.new("RGB", (width, h), "#111")
        d = ImageDraw.Draw(img)
        y = 4
        for t, f in lines:
            d.text((8, y), t, fill="#ffd84d" if f is font else "#ddd", font=f)
            y += 26 if f is font else 20
        return img

    def status(job: str) -> str:
        m = done.get(job)
        return f"  [{m['result'].upper()}] {m.get('why', '')}" if m else "  [chưa soát]"

    with tempfile.TemporaryDirectory() as td:
        for kf in sorted((project / "frames").glob("keyframe_c*.png")):
            job = kf.stem
            im = Image.open(kf).convert("RGB")
            im.thumbnail((KW, KW * 2))
            cap = caption(job + status(job), placement + checks.get(job, []), SHEET_W - KW - 20)
            row = Image.new("RGB", (SHEET_W, max(im.height, cap.height) + 10), "#111")
            row.paste(im, (0, 5))
            row.paste(cap, (KW + 20, 5))
            blocks.append(row)
        for c in sorted((project / "clips").glob("c*.mp4")):
            job = c.stem[:3]
            info = media_info(c)
            th = int(TW * info["height"] / info["width"])
            times = [0.2 + k for k in range(int(info["duration"]))]
            strip = Image.new("RGB", (TW * len(times), th), "#111")
            for k, t in enumerate(times):
                f = Path(td) / f"{c.stem}_{k}.jpg"
                subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", str(c),
                                "-frames:v", "1", "-q:v", "4", str(f)], check=True)
                fr = Image.open(f).convert("RGB").resize((TW, th))
                strip.paste(fr, (TW * k, 0))
            if strip.width > SHEET_W:
                strip = strip.resize((SHEET_W, int(strip.height * SHEET_W / strip.width)))
            cap = caption(c.stem + status(c.stem), placement + checks.get(job, []), SHEET_W)
            row = Image.new("RGB", (SHEET_W, strip.height + cap.height + 10), "#111")
            row.paste(strip, (0, 5))
            row.paste(cap, (0, strip.height + 5))
            blocks.append(row)
    if not blocks:
        raise SystemExit("Chưa có keyframe hay clip nào để soát")
    sheet = Image.new("RGB", (SHEET_W, sum(b.height for b in blocks) + 8 * len(blocks)), "#000")
    y = 0
    for b in blocks:
        sheet.paste(b, (0, y))
        y += b.height + 8
    out = project / "edit" / "qc" / "gen_review.jpg"
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, quality=88)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--mark", nargs=3, metavar=("JOB", "RESULT", "WHY"))
    args = ap.parse_args()
    project = project_dir(args.project, need_production=False)
    if args.mark:
        job, result, why = args.mark
        if result not in ("pass", "fail"):
            raise SystemExit("kết quả phải là pass hoặc fail")
        with open(project / "edit" / "gen_review.jsonl", "a") as f:
            f.write(json.dumps({"t": datetime.now().isoformat(timespec="seconds"), "job": job,
                                "result": result, "why": why}, ensure_ascii=False) + "\n")
        print(f"{job}: {result} — {why}")
        return
    out = build(project)
    product = load_json(project / "product.json") if (project / "product.json").exists() else {}
    print(f"-> {out.relative_to(project)}")
    print("Soát vị trí (product.json.placement_checks):")
    for p in product.get("placement_checks", []) or ["(chưa có — thêm vào product.json)"]:
        print("  •", p)
    done = marks(project)
    for job, cs in checks_from_prompts(project).items():
        st = done.get(job, {}).get("result", "chưa soát")
        print(f"{job} [{st}]: " + (" · ".join(cs) if cs else "(không có dòng Soát)"))


if __name__ == "__main__":
    main()
