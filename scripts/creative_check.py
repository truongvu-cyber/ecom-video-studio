"""Check Agent 1's output before the user spends credits.

Usage: creative_check.py <project>
1. validate.py --no-clips (schemas, claims with evidence)
2. prompt_lint.py on prompts.md (Veo + Nano Banana Pro)
3. prompts.md <-> production.json agree: every clip referenced has a prompt and a
   keyframe, dialogue lines match the dialogue clip, word budget, margins, total length.
Exit 1 on any FAIL.
"""
from __future__ import annotations

import json
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


# formats.md §2, the machine-checkable part. use_sec bounds are (min, max) for B-roll shots.
FORMATS = {
    "ugc_dialogue": {"keep_native": True, "captions": True, "fx": "none", "text": "pill",
                     "use": (2.0, 4.0), "shots": (5, 7), "dialogue_clips": 1},
    "hype_montage": {"keep_native": False, "captions": False, "fx": "hype", "text": "bold",
                     "use": (1.2, 2.5), "shots": (8, 8), "dialogue_clips": 0},
    "calm_lofi": {"keep_native": True, "captions": False, "fx": "none", "text": "pill",
                  "use": (2.5, 4.0), "shots": (4, 6), "dialogue_clips": 0},
    "demo_steps": {"keep_native": None, "captions": False, "fx": "hype", "text": "bold",
                   "use": (1.2, 2.5), "shots": (8, 8), "dialogue_clips": 0},
}
MAX_OVERLAY_WORDS = 4

# realism.md (user rule 2026-10-27): a clip with a person, hand or face must carry the REALISM
# lock, state the blocking, and list the physics negatives.
PERSON_WORDS = r"\b(man|woman|guy|girl|person|people|friend|he|she|his|her|hand|hands|finger|fingers|face|thumb|palm)\b"
REALISM_MARK = "every movement obeys physics"          # a phrase only the REALISM lock contains
BLOCKING_MARK = r"\b(beside|next to|outside|around|behind|in front of|on the (driver|passenger)|one step|stands?|standing|sits?|sitting)\b"
PATH_VERBS = r"\b(walks? (up|over|in)|comes? (over|up)|steps? in|leans? in|reach(es)? across|runs? to)\b"
PHYSICS_NEG = ["passing through", "clipping", "extra fingers", "floating"]


def lock(md: str, name: str) -> list[str]:
    """Text of every lock whose heading starts with `name` (CHARACTER, STYLE, STYLE - day...)."""
    return [m.group(1) for m in re.finditer(r"\*\*%s[^*]*\*\*:?\s*\n(.+)" % name, md)]


def check_character(md: str, project: Path, fails: list[str], warns: list[str]) -> None:
    """formats.md §4 (user rule 2026-10-27): every project invents its own person and generates
    its own sheet — a CHARACTER lock needs a Bước 0 sheet block, and the sheet file must not be
    a copy of another project's."""
    if not lock(md, "CHARACTER"):
        return
    sheets = re.findall(r"```[a-z]*\n.*?```\s*\n\s*\*\*(?:Lưu thành|Save as)[^*]*\*\*:?\s*`?([^`\n]+_sheet\.png)`?", md, re.S)
    if not sheets:
        fails.append("Có khoá CHARACTER nhưng Bước 0 không có block gen ảnh nhân vật (`Lưu thành: <name>_sheet.png`) — "
                     "mỗi project một người mới, không dùng lại sheet cũ (formats.md §4)")
        return
    import hashlib
    for name in sheets:
        f = project / "frames" / name
        if not f.exists():
            continue
        h = hashlib.md5(f.read_bytes()).hexdigest()
        for other in (ROOT / "projects").iterdir():
            if other == project or not other.is_dir():
                continue
            for g in (other / "frames").glob("*_sheet.png"):
                if hashlib.md5(g.read_bytes()).hexdigest() == h:
                    fails.append(f"frames/{name} trùng với {other.name}/frames/{g.name}: sheet phải gen mới cho project này")


def check_world(md: str, product: dict, fails: list[str], warns: list[str]) -> None:
    """formats.md §4b: with product.json.world, CHARACTER and every STYLE lock carry a cue."""
    world = product.get("world")
    if not world:
        if re.search(r"\b(team|club|fan|fans|jersey|logo)\b", json.dumps(product).lower()):
            warns.append("product.json không có 'world' dù sản phẩm thuộc đội/brand — thêm world.cues (formats.md §4b)")
        return
    cues = [c.lower() for c in world.get("cues", [])]
    if len(cues) < 2:
        fails.append("product.json world.cues cần ≥2 mục: [0] đồ fan trên người, [1:] vật trong bối cảnh (formats.md §4b)")
        return
    for text in lock(md, "CHARACTER"):
        if cues[0] not in text.lower():
            fails.append(f"Khoá CHARACTER thiếu nguyên văn đồ fan world.cues[0]: '{world['cues'][0][:50]}…' (formats.md §4b)")
    for text in lock(md, "STYLE"):
        if not any(c in text.lower() for c in cues[1:]):
            fails.append(f"Một khoá STYLE không có vật bối cảnh nào trong world.cues[1:] nguyên văn (formats.md §4b): '{text[:50]}…'")


def check_placement(md: str, product: dict, blocks: dict[int, str], keyframes: set[int],
                    fails: list[str], warns: list[str]) -> None:
    """keyframes.md §5b: placement_checks exist and every keyframe/clip repeats its own checks."""
    pcs = product.get("placement_checks") or []
    if not pcs:
        fails.append("product.json thiếu placement_checks (vị trí/trạng thái sản phẩm phải đúng) — keyframes.md §5b")
        return
    pwords = {w for p in pcs for w in words(p) if len(w) > 3}
    for n in sorted(keyframes):
        m = re.search(r"^###\s*Keyframe\s*%d\b.*?(?=^###|^## |\Z)" % n, md, re.M | re.S | re.I)
        line = m.group(0) if m else ""
        soat = re.search(r"\*\*Soát trước khi làm video[^*]*\*\*:?\s*(.+)", line)
        if not soat or len(pwords & set(words(soat.group(1)))) < 2:
            fails.append(f"Keyframe {n}: dòng 'Soát trước khi làm video' không nhắc lại kiểm tra vị trí sản phẩm (placement_checks)")
    for n, block in sorted(blocks.items()):
        soat = re.search(r"\*\*Soát clip[^*]*\*\*:?\s*(.+)", block)
        if not soat:
            fails.append(f"Clip {n}: thiếu dòng '**Soát clip:**' (vị trí sản phẩm + hành động phải đúng ở mọi giây)")
        elif len(pwords & set(words(soat.group(1)))) < 2:
            fails.append(f"Clip {n}: 'Soát clip' không nhắc lại kiểm tra vị trí sản phẩm (placement_checks)")


def check_people(n: int, block: str, fails: list[str], warns: list[str]) -> None:
    prompt = "\n".join(re.findall(r"```[a-z]*\n(.*?)```", block, re.S)).lower()
    # "no person in frame" / "no people" is the opposite of a person being there
    if not re.search(PERSON_WORDS, re.sub(r"\bno (person|people|one|hands?)\b[^.]*", "", prompt)):
        return
    if REALISM_MARK not in prompt:
        fails.append(f"Clip {n} có người/tay: thiếu khoá REALISM (realism.md §1) dán trong prompt")
    neg = " ".join(re.findall(r"\*\*(?:Phủ định|Negative)[^*]*\*\*:?\s*`?([^`\n]+)", block)).lower()
    missing = [w for w in PHYSICS_NEG if w not in neg]
    if missing:
        fails.append(f"Clip {n} có người/tay: negative thiếu {missing} (realism.md §4)")
    if re.search(PATH_VERBS, prompt) and not re.search(r"\b(around|along|past)\b", prompt):
        fails.append(f"Clip {n}: có 'walks up/comes over/leans in…' mà không ghi đường đi vòng qua vật cản (realism.md §2)")
    if not re.search(BLOCKING_MARK, prompt):
        warns.append(f"Clip {n}: chưa ghi vị trí người so với xe/cửa/vật rắn (realism.md §2)")


def check_format(prod: dict, fails: list[str], warns: list[str]) -> None:
    fmt = prod.get("format")
    if not fmt:
        warns.append("Thiếu 'format' (ugc_dialogue | hype_montage | calm_lofi | demo_steps): không kiểm tra được preset")
        return
    f = FORMATS[fmt]
    audio, caps = prod.get("audio", {}), prod.get("captions", {})
    fx = (prod.get("fx") or {}).get("preset", "none")
    text = (prod.get("text_style") or {}).get("preset", "pill")
    if f["keep_native"] is not None and audio.get("keep_native", True) != f["keep_native"]:
        fails.append(f"format {fmt}: audio.keep_native phải là {str(f['keep_native']).lower()}")
    if caps.get("enabled", True) != f["captions"]:
        fails.append(f"format {fmt}: captions.enabled phải là {str(f['captions']).lower()}")
    if fx != f["fx"]:
        fails.append(f"format {fmt}: fx.preset phải là '{f['fx']}' (đang '{fx}')")
    if text != f["text"]:
        warns.append(f"format {fmt}: text_style.preset nên là '{f['text']}' (đang '{text}')")
    n = len(prod["shots"])
    if not f["shots"][0] <= n <= f["shots"][1]:
        warns.append(f"format {fmt}: nên có {f['shots'][0]}–{f['shots'][1]} shot (đang {n})")
    # dialogue shots only matter when the voice is kept; muted formats may still use
    # a talking clip as footage (the transcript then just locates the moment)
    dlg = {s["file_pattern"] for s in prod["shots"] if s["audio_type"] == "dialogue"}
    if fmt == "ugc_dialogue" and len(dlg) != 1:
        fails.append(f"format {fmt}: cần đúng 1 clip thoại (đang {len(dlg)})")
    lo, hi = f["use"]
    for s in prod["shots"]:
        if s["audio_type"] == "dialogue":
            continue
        if not lo <= s["use_sec"] <= hi:
            warns.append(f"{s['id']}: use_sec {s['use_sec']}s ngoài khoảng {lo}–{hi}s của format {fmt}")
        if fmt in ("hype_montage", "demo_steps") and not s.get("moment") and not (s.get("override") or {}).get("src_in"):
            warns.append(f"{s['id']}: format {fmt} cần 'moment' (a/b/peak/calm) để Editor lấy đúng nửa clip")
    if fmt != "ugc_dialogue" and not (prod.get("music") or {}).get("drop_on"):
        warns.append(f"format {fmt}: nên đặt music.drop_on = shot payoff")
    if len(prod.get("variants") or []) < 2:
        warns.append("Thiếu biến thể hook: cần 3 hook khác kiểu (variants có ≥ 2 mục)")


def check_overlays(prod: dict, fails: list[str], warns: list[str]) -> None:
    bold = (prod.get("text_style") or {}).get("preset") == "bold"
    for s in prod["shots"]:
        ov = s.get("overlay")
        if not ov:
            continue
        n = len(re.findall(r"[A-Za-z0-9'’]+", ov))
        if n > MAX_OVERLAY_WORDS + 2:
            fails.append(f"{s['id']}: overlay {n} từ ('{ov}'), tối đa {MAX_OVERLAY_WORDS}")
        elif n > MAX_OVERLAY_WORDS:
            warns.append(f"{s['id']}: overlay {n} từ, nên ≤ {MAX_OVERLAY_WORDS} ('{ov}')")
        if bold and "*" not in ov and s["role"] != "cta":
            warns.append(f"{s['id']}: chữ bold nên có một từ nhấn *word* ('{ov}')")


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
        check_people(n, blocks[n], fails, warns)

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

    check_format(prod, fails, warns)
    check_overlays(prod, fails, warns)
    check_world(md, product, fails, warns)
    check_character(md, project, fails, warns)
    check_placement(md, product, blocks, keyframes, fails, warns)

    print("\n== creative_check ==")
    for f in fails:
        print("FAIL:", f)
    for w in warns:
        print("WARN:", w)
    print("KẾT LUẬN:", "SỬA TRƯỚC KHI GEN" if fails else ("XEM CẢNH BÁO" if warns else "SẴN SÀNG GEN"))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
