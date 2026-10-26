"""Check Agent 1's output before the user spends credits.

Usage: creative_check.py <project>
1. validate.py --no-clips (schemas, claims with evidence)
2. prompt_lint.py on prompts.md (Veo + Nano Banana Pro)
3. prompts.md <-> production.json agree: every clip referenced has a prompt and a
   keyframe, dialogue lines match the dialogue clip, word budget, margins, total length.
Exit 1 on any FAIL.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

from common import ROOT, load_json, project_dir

LINT = ROOT / ".claude" / "skills" / "ad-creative" / "tools" / "prompt_lint.py"
MAX_DIALOGUE_WORDS = 18
# product.json "unknown" topic -> words that would state it in the ad
UNKNOWN_CUES = {
    "price": ["price", "cheap", "deal", "sale", "discount", "\\$"],
    "ship": ["ship", "deliver", "arriv"],
    "colo": ["colou?r", "black", "white", "navy", "pink", "red", "blue", "green"],
    "size": ["size", "fits", "xl", "small", "large"],
    "fabric": ["cotton", "fleece", "fabric", "soft", "cozy", "warm", "thick", "premium", "quality"],
    "material": ["cotton", "leather", "steel", "wood", "ceramic", "premium", "quality"],
    "review": ["review", "stars", "rated", "loved by", "customers"],
}


def words(text: str) -> list[str]:
    return re.findall(r"[a-z0-9']+", text.lower())


def clip_blocks(md: str) -> dict[int, str]:
    out, cur, buf = {}, None, []
    for line in md.splitlines():
        m = re.match(r"^##\s*Clip\s*(\d+)", line, re.I)
        if m or re.match(r"^##\s", line):
            if cur is not None:
                out[cur] = "\n".join(buf)
            cur, buf = (int(m.group(1)), []) if m else (None, [])
            continue
        if cur is not None:
            buf.append(line)
    if cur is not None:
        out[cur] = "\n".join(buf)
    return out


def main() -> None:
    project = project_dir(sys.argv[1])
    py = sys.executable
    fails: list[str] = []
    warns: list[str] = []

    v = subprocess.run([py, str(Path(__file__).parent / "validate.py"), str(project), "--no-clips"],
                       capture_output=True, text=True)
    print(v.stdout.strip())
    if v.returncode != 0:
        fails.append("validate.py báo lỗi (xem trên)")

    prompts = project / "prompts.md"
    if not prompts.exists():
        sys.exit("Thiếu prompts.md")
    prod = load_json(project / "production.json")
    lint = subprocess.run([py, str(LINT), str(prompts), "--model", "veo", "--image-model",
                           prod.get("gen_model", {}).get("image", "nano-banana-pro"),
                           "--target", str(prod["spec"]["target_sec"])],
                          capture_output=True, text=True)
    print(lint.stdout.strip())
    if lint.returncode != 0:
        fails.append("prompt_lint báo FAIL (xem trên)")

    md = prompts.read_text(encoding="utf-8")
    blocks = clip_blocks(md)
    keyframes = {int(n) for n in re.findall(r"^###\s*Keyframe\s*(\d+)", md, re.M | re.I)}

    used: dict[int, list[dict]] = {}
    for s in prod["shots"]:
        m = re.match(r"c(\d+)", s["file_pattern"])
        if not m:
            fails.append(f"{s['id']}: file_pattern phải dạng cNN*.mp4")
            continue
        used.setdefault(int(m.group(1)), []).append(s)

    for n, shots in sorted(used.items()):
        if n not in blocks:
            fails.append(f"Clip {n} được dùng trong production.json nhưng không có '## Clip {n}' trong prompts.md")
            continue
        if n not in keyframes:
            fails.append(f"Clip {n} thiếu '### Keyframe {n}'")
        if f"c{n}_a.mp4" not in blocks[n] and f"c{n:02d}_a.mp4" not in blocks[n]:
            warns.append(f"Clip {n}: không ghi tên lưu file (c{n:02d}_a.mp4)")
        body = " ".join(words(blocks[n]))
        dlg = [s for s in shots if s["audio_type"] == "dialogue"]
        for s in shots:
            gen = s.get("gen_sec", 8)
            if s["use_sec"] > gen - 1:
                fails.append(f"{s['id']}: use_sec {s['use_sec']} > gen_sec - 1 ({gen - 1}); Editor không còn chỗ cắt")
        if dlg:
            total = sum(len(words(s["dialogue"] or "")) for s in dlg)
            if total > MAX_DIALOGUE_WORDS:
                fails.append(f"Clip {n}: {total} từ thoại, tối đa {MAX_DIALOGUE_WORDS} cho một clip 8s")
            for s in dlg:
                line = " ".join(words(s["dialogue"] or ""))
                if line and line not in body:
                    fails.append(f"{s['id']}: câu thoại '{s['dialogue']}' không có nguyên văn trong prompt clip {n}")
                need = len(words(s["dialogue"] or "")) / 2.5 + 0.4
                if s["use_sec"] < need:
                    warns.append(f"{s['id']}: use_sec {s['use_sec']}s ngắn hơn thời gian nói (~{need:.1f}s)")
            if "ingredient" not in blocks[n].lower() and "reference" not in blocks[n].lower():
                warns.append(f"Clip {n} có thoại: nên gen bằng Veo Ingredients (first-frame hay mất tiếng)")
        else:
            if "speech" not in body and "no dialogue" not in body:
                warns.append(f"Clip {n} là B-roll: nên ghi 'no speech' trong Audio")
        if "subtitle" not in body:
            fails.append(f"Clip {n}: thiếu 'no subtitles' (Veo hay tự in phụ đề)")

    product = load_json(project / prod.get("product_ref", "product.json"))
    for s in prod["shots"]:
        said = " ".join(words(f"{s.get('dialogue') or ''} {s.get('overlay') or ''}"))
        for item in product.get("unknown", []):
            for topic, cues in UNKNOWN_CUES.items():
                if topic in item.lower() and any(re.search(rf"\b{c}", said) for c in cues):
                    fails.append(f"{s['id']}: nói về '{item}' nhưng product.json ghi là chưa biết")

    dlg_clips = [n for n, ss in used.items() if any(s["audio_type"] == "dialogue" for s in ss)]
    if len(dlg_clips) > 1:
        warns.append(f"Có {len(dlg_clips)} clip thoại ({dlg_clips}): giọng sẽ khác nhau giữa các clip")
    total = sum(s["use_sec"] for s in prod["shots"])
    target = prod["spec"]["target_sec"]
    if abs(total - target) > 2:
        warns.append(f"Tổng use_sec {total:.1f}s lệch mục tiêu {target}s")
    unused = sorted(set(blocks) - set(used))
    if unused:
        warns.append(f"Clip {unused} có prompt nhưng không shot nào dùng")

    print("\n== creative_check ==")
    for f in fails:
        print("FAIL:", f)
    for w in warns:
        print("WARN:", w)
    print("KẾT LUẬN:", "SỬA TRƯỚC KHI GEN" if fails else ("XEM CẢNH BÁO" if warns else "SẴN SÀNG GEN"))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
