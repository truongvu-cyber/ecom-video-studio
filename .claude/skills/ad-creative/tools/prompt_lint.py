#!/usr/bin/env python3
"""
prompt_lint.py - check AI video prompts before you spend credits on them.

Reads a prompt file in the video-prompt-studio template (## Clip N headings, each with a
fenced prompt block and an optional **Negative:** line), or any text/Markdown
file of prompts in fenced blocks, or a single prompt from stdin. Checks each
prompt against what video models are known to get wrong and against the target
model's limits in models.json:

  - length for the model, vague filler words, speed words on the subject
  - more than one camera move in a single-shot clip, multi-shot on a model
    that cannot do it, Hailuo bracket commands over three
  - text, logos and prices asked of the model, crowds of subjects
  - unproven claims (named brands and IP only with --check-names)
  - Veo dialogue in quotes (burns subtitles), lines too long for the clip
  - the locks (CHARACTER / PRODUCT / STYLE) not pasted word for word,
    unfilled <placeholders>, missing camera or light, contradictory light
  - clip lengths the model cannot generate, total length against --target
  - every '## Clip N' has its '### Keyframe N' image prompt (clips marked
    "First frame: filmed" are exempt)

FAIL means fix before generating. WARN means fix it or know why not.
Exit code 1 when anything FAILs.

Usage
  python3 prompt_lint.py prompts.md --model kling3 --target 30
  python3 prompt_lint.py prompts.md --model veo --json
  pbpaste | python3 prompt_lint.py - --model seedance

Standard library only.
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WORDS_PER_SECOND = 2.5

VAGUE = [
    "beautiful", "stunning", "amazing", "awesome", "gorgeous", "epic", "nice",
    "cool", "perfect", "masterpiece", "best quality", "high quality", "ultra quality",
    "breathtaking", "incredible", "magical", "aesthetic", "vibes", "trending",
]
SPEED = ["fast", "quickly", "rapidly", "lunge", "lunges", "lurch", "lurches",
         "sprint", "sprints", "dash", "dashes", "in a hurry", "super fast"]
CAMERA = [
    "dolly in", "dolly out", "push in", "push-in", "pull back", "pull out", "pull-back",
    "pan left", "pan right", "whip pan", "whip-pan", "tilt up", "tilt down", "tracking",
    "orbit", "arc shot", "crane up", "crane down", "jib", "crash zoom", "snap zoom",
    "zoom in", "zoom out", "dolly zoom", "rack focus", "handheld", "gimbal", "steadicam",
    "static", "locked-off", "locked off", "fpv", "drone", "aerial", "flyover", "pov",
    "following shot", "leading shot", "truck left", "truck right", "pedestal",
    "time freeze", "bullet time", "hyperlapse", "timelapse", "selfie",
]
MOVES = [
    "dolly in", "dolly out", "push in", "push-in", "pull back", "pull out", "pan left",
    "pan right", "whip pan", "whip-pan", "tilt up", "tilt down", "tracking", "orbit",
    "arc shot", "crane up", "crane down", "crash zoom", "snap zoom", "zoom in",
    "zoom out", "dolly zoom", "rack focus", "truck left", "truck right", "fpv",
    "flyover", "time freeze", "bullet time",
]
LIGHT = [
    "light", "lit", "lighting", "glow", "sun", "golden hour", "blue hour", "lamp",
    "candle", "neon", "daylight", "shadow", "backlit", "rim", "high-key", "low-key",
    "overcast", "dusk", "dawn", "night", "tungsten", "softbox", "studio",
]
PEOPLE = ["woman", "man", "girl", "boy", "person", "friend", "child", "kid", "mother",
          "father", "mom", "dad", "grandma", "grandpa", "teen", "baby", "couple"]
CROWD = ["crowd", "people", "group of", "family of", "audience", "friends"]
NAMES = [
    "disney", "pixar", "ghibli", "dreamworks", "marvel", "dc comics", "star wars",
    "harry potter", "pokemon", "pokémon", "grinch", "elf on the shelf", "barbie",
    "hello kitty", "lego", "stanley cup", "stanley tumbler", "stanley quencher",
    "yeti tumbler", "yeti cooler", "yeti rambler", "magsafe", "tesla", "nike", "adidas",
    "coca-cola", "starbucks", "apple logo", "wes anderson", "christopher nolan",
    "spielberg", "miyazaki", "taylor swift", "mrbeast", "nfl", "nba", "fifa", "pantone",
]
CLAIMS = [
    r"\bsafer\b", r"\bsaves? (you )?(money|on)\b", r"\bguarantee(d)?\b", r"\bclinically\b",
    r"\bcures?\b", r"\bheals?\b", r"\b#1\b", r"\bnumber one\b", r"\bbest[- ]selling\b",
    r"\bproven\b", r"\b100% (safe|natural)\b", r"\bnon[- ]toxic\b", r"\bfda\b",
]
TEXT_ASKS = [
    r"\blabel (that )?(reads|says)\b", r"\btext (that )?(reads|says)\b",
    r"\bsign (that )?(reads|says)\b", r"\bwritten on\b", r"\bprice tag\b",
    r"\$\s?\d", r"\bcaption(s)? (that|reading)\b", r"\bheadline\b", r"\bslogan\b",
]
CLEAN_PHRASES = [
    r"no (on-screen )?(subtitles|captions|text|logos?|watermarks?|lettering)",
    r"without (any )?(text|logos?|captions|subtitles)",
    r"no visible (text|logo|branding)",
]
CONTRADICTIONS = [
    (r"golden hour", r"\b(midnight|night sky|heavy (rain|downpour)|downpour|blizzard)\b"),
    (r"photoreal|live[- ]action|cinema camera", r"\b(anime|cartoon|2d animation|claymation|pixel art)\b"),
    (r"\bstatic\b|locked[- ]off", r"\b(orbit|tracking|dolly|crane|whip|creeping|push in)\b"),
    (r"high-key", r"low-key"),
]
STRICT_NAMES = False   # brands, teams and characters are the user's call; --check-names warns about them
ALLOWED_TOKENS = re.compile(r"@\w+|<<<\w+>>>")
PLACEHOLDER = re.compile(r"<[^<>\n]{2,80}>|\[(?:STYLE|CHARACTER|PRODUCT|AUDIO|NEGATIVE)[^\]]*\]|\{\{[^}]+\}\}", re.I)
HEADING = re.compile(r"^#{2,4}\s*(clip|shot|scene|cảnh|canh|keyframe|key frame)\s*(?:for clip\s*)?(\d+)(.*)$", re.I)
FIRST_FRAME = re.compile(r"\*\*(?:First frame|Khung đầu)[^*]*\*\*:?\s*([^\n·]+)", re.I)
REF_ANCHOR = re.compile(r"\bimage\s*\d|\breference\b|@product|@image\d|<<<image_\d+>>>|\bimg\s*\d|\bphoto\b", re.I)
KEEP_CLAUSE = re.compile(r"\b(keep (it|them|her|him)?\s*exactly|exactly as in|unchanged|do not (change|redraw|alter|restyle)|identical|same shape)\b", re.I)
RATIO = re.compile(r"9:16|\bvertical\b|\bportrait\b|--ar\s*\d", re.I)
HOLD = re.compile(r"\b(hold|holds|holding|held|grip|in (her|his|their) hands?)\b", re.I)
GRIP = re.compile(r"\b(fingers?|thumb|palm|grip|wrapped|both hands|(right|left) hand|at chest height|cupped)\b", re.I)
FENCE = re.compile(r"```[a-zA-Z]*\n(.*?)```", re.S)
DUR = re.compile(r"(?<![\d.])(\d{1,2}(?:\.\d)?)\s?s\b")
TIMECODE = re.compile(r"\b\d{1,2}\s?[-–]\s?\d{1,2}\s?s\b|\bshot \d+\b", re.I)
LOCK = re.compile(r"^\*\*(CHARACTER|PRODUCT|STYLE)[^*]*\*\*\s*:?\s*(.*)$", re.I)


def load_models():
    with open(os.path.join(HERE, "models.json"), encoding="utf-8") as fh:
        data = json.load(fh)
    data.pop("_note", None)
    return data


def norm(s):
    return re.sub(r"\s+", " ", s).strip().lower()


def has(text, term):
    return re.search(r"(?<![\w-])" + re.escape(term) + r"(?![\w-])", text) is not None


def parse(raw):
    """Return (locks, clips). Each clip: label, duration, prompt, negative."""
    lines = raw.splitlines()
    locks = {}
    i = 0
    while i < len(lines):
        m = LOCK.match(lines[i].strip())
        if m:
            name, body = m.group(1).upper(), [m.group(2)]
            j = i + 1
            while j < len(lines) and lines[j].strip() and not lines[j].lstrip().startswith(("**", "#", "```")):
                body.append(lines[j].strip())
                j += 1
            text = " ".join(b for b in body if b).strip()
            if text:
                locks.setdefault(name, []).append(text)
            i = j
            continue
        i += 1

    clips, cur = [], None
    for line in lines:
        h = HEADING.match(line.strip())
        if h:
            if cur:
                clips.append(cur)
            d = DUR.search(h.group(3))
            kind = "image" if h.group(1).lower().startswith("key") else "video"
            cur = {"label": f"{'Keyframe' if kind == 'image' else h.group(1).title()} {h.group(2)}",
                   "duration": None if kind == "image" else (float(d.group(1)) if d else None),
                   "kind": kind, "body": []}
            continue
        if cur is not None:
            cur["body"].append(line)
    if cur:
        clips.append(cur)

    out = []
    if clips:
        for c in clips:
            body = "\n".join(c["body"])
            blocks = FENCE.findall(body)
            if not blocks:
                out.append({"label": c["label"], "duration": c["duration"], "prompt": "",
                            "negative": "", "missing": True, "kind": c["kind"], "first_frame": ""})
                continue
            neg = ""
            nm = re.search(r"\*\*(?:Negative|Phủ định)[^*]*\*\*:?\s*`?([^`\n]+)`?", body, re.I)
            if nm:
                neg = nm.group(1)
            elif len(blocks) > 1:
                neg = blocks[1]
            ff = FIRST_FRAME.search(body)
            out.append({"label": c["label"], "duration": c["duration"], "prompt": blocks[0].strip(),
                        "negative": neg.strip(), "kind": c["kind"],
                        "first_frame": ff.group(1).strip() if ff else ""})
    else:
        found = list(FENCE.finditer(raw))
        if not found:
            out.append({"label": "Prompt 1", "duration": None, "prompt": raw.strip(), "negative": ""})
        for k, m in enumerate(found):
            before = raw[max(0, m.start() - 80):m.start()].lower()
            text = m.group(1).strip()
            if out and re.search(r"negative|avoid", before.splitlines()[-1] if before.splitlines() else ""):
                out[-1]["negative"] = text
            elif text:
                end = found[k + 1].start() if k + 1 < len(found) else len(raw)
                nm = re.search(r"\*\*(?:Negative|Phủ định)[^*]*\*\*:?\s*`?([^`\n]+)`?", raw[m.end():end], re.I)
                out.append({"label": f"Prompt {len(out) + 1}", "duration": None, "prompt": text,
                            "negative": nm.group(1).strip() if nm else ""})
    for c in out:
        c.setdefault("missing", False)
        c.setdefault("kind", "video")
        c.setdefault("first_frame", "")
        a = re.search(r"^\s*avoid\s*:\s*(.+)$", c["prompt"], re.I | re.M | re.S)
        c["avoid"] = a.group(1).strip() if a else ""
        m = re.search(r"^\s*(negative( prompt)?|avoid)\s*:\s*(.+)$", c["prompt"], re.I | re.M | re.S)
        if m and m.group(1).lower().startswith("negative"):
            if not c["negative"]:
                c["negative"] = m.group(3).strip()
            c["prompt"] = c["prompt"][:m.start()].strip()
    return locks, out


def spoken(prompt):
    lines = []
    for m in re.finditer(r"\bsays?\b[^:\n\"“]*[:,]?\s*[\"“]?([^\"”\n]+)", prompt, re.I):
        lines.append(m.group(1))
    for m in re.finditer(r"^\s*-\s*@?\w+\s*:\s*[\"“]([^\"”]+)", prompt, re.M):
        lines.append(m.group(1))
    return lines


def lint_clip(c, model, key, locks):
    res = []
    if c.get("missing"):
        return [("FAIL", "No fenced prompt block under this heading.")]
    p = c["prompt"]
    low = p.lower()
    if c.get("avoid"):
        # the Avoid: line lists exclusions; check it only for names, not as content
        body = re.sub(r"^\s*avoid\s*:.*$", " ", p, flags=re.I | re.M | re.S).lower()
    else:
        body = low
    clean = body
    for pat in CLEAN_PHRASES:
        clean = re.sub(pat, " ", clean)

    def add(level, msg):
        res.append((level, msg))

    words = len(re.findall(r"[\w'’-]+", ALLOWED_TOKENS.sub("x", p)))
    lo, hi = model["words"]
    if words > hi * 1.5:
        add("FAIL", f"{words} words. {model['label']} works best at {lo}-{hi}; long prompts drop details.")
    elif words > hi:
        add("WARN", f"{words} words, above the {lo}-{hi} sweet spot for {model['label']}.")
    elif words < lo:
        add("WARN", f"{words} words, below {lo}. Add the camera move, the light, or the style lock.")

    found = [w for w in VAGUE if has(body, w)]
    if found:
        add("WARN", f"Filler words: {', '.join(found)}. Replace with something visible (light, lens, material).")

    fast = [w for w in SPEED if has(body, w)]
    if fast:
        lvl = "FAIL" if key.startswith("seedance") and "fast" in fast else "WARN"
        add(lvl, f"Speed words on the subject: {', '.join(fast)}. They warp faces and limbs; move the camera or cut instead.")

    multi = bool(TIMECODE.search(p))
    moves = sorted({m.replace("-", " ") for m in MOVES if has(body, m)})
    if multi and not model.get("multishot"):
        add("WARN", f"Timecodes or shot labels, but {model['label']} makes one shot per generation. Split into clips.")
    if not multi and len(moves) > 1:
        add("WARN", f"{len(moves)} camera moves in one shot ({', '.join(moves)}). Keep one; split the rest.")
    if not any(has(low, t) for t in CAMERA) and not re.search(r"\[(push|pull|pan|tilt|zoom|truck|pedestal|shake|tracking|static)", low):
        add("WARN", "No camera framing or move. Say the shot size and one move (or 'static').")
    i2v = re.search(r"keyframe|\.(png|jpe?g|webp)|photo|last frame", c.get("first_frame", ""), re.I)
    if not i2v and not any(has(low, t) for t in LIGHT):
        add("WARN", "No light described. Light changes quality more than any other line.")

    if key == "hailuo":
        n = len(re.findall(r"\[(push|pull|pan|tilt|zoom|truck|pedestal|shake|tracking|static)[^\]]*\]", low))
        if n > 3:
            add("WARN", f"{n} bracket camera commands; Hailuo follows at most three.")

    texty = [pat for pat in TEXT_ASKS if re.search(pat, clean)]
    if texty:
        add("WARN", "Asks the model for text, a logo or a price. Those come out garbled; add them in the edit.")

    people = {w for w in PEOPLE if has(body, w)}
    if any(has(body, w) for w in CROWD) or len(people) >= 3:
        add("WARN", "Several people or a crowd. Faces merge past two or three subjects; keep one person per clip if you can.")

    names = [n for n in NAMES if has(low, n) and not (n == "magsafe" and "magsafe-compatible" in low)]
    if names and STRICT_NAMES:
        add("WARN", f"Named brand or IP: {', '.join(names)}. Some models refuse or blur names; if so, describe the look.")
    if re.search(r"\bin the style of\b", low):
        add("WARN", "'in the style of' usually names someone. Describe the look with a style block.")

    claims = [re.search(c_, body).group(0) for c_ in CLAIMS if re.search(c_, body)]
    if claims:
        add("WARN", f"Claim words: {', '.join(claims)}. Only keep them if the user can prove them.")

    for a, b in CONTRADICTIONS:
        if multi and "static" in a:
            continue  # different shots may legitimately use different moves
        if re.search(a, body) and re.search(b, body):
            add("WARN", f"Possible contradiction: '{re.search(a, body).group(0)}' with '{re.search(b, body).group(0)}'.")

    if key == "veo" and re.search(r"\bsays?\b[^\n:]*:\s*[\"“]", p, re.I):
        add("WARN", "Veo dialogue in quotes tends to burn subtitles. Use 'She says: line' without quotes.")
    lines = spoken(p)
    if lines and key == "veo" and not re.search(r"no (subtitles|captions)", low + " " + c["negative"].lower()):
        add("WARN", "Dialogue without 'no subtitles' in the prompt or negative.")
    if lines and not model.get("audio"):
        add("WARN", f"{model['label']} makes no speech. Keep the line as acting direction and dub it in post.")
    if lines and c["duration"]:
        n = sum(len(x.split()) for x in lines)
        if n > WORDS_PER_SECOND * c["duration"] + 1:
            add("WARN", f"{n} spoken words in {c['duration']:g}s. About {int(WORDS_PER_SECOND * c['duration'])} fit; shorten it.")
    if any(len(x.split()) > 22 for x in lines):
        add("WARN", "A spoken line runs past ~20 words; lip-sync degrades. Split it.")

    bans = len(re.findall(r"\bno [a-z-]+", low))
    if model.get("negative_field") and bans > 6:
        add("WARN", f"{bans} 'no ...' bans in the prompt. Move most of them to the negative field; describe what IS there.")
    if model.get("negative_field") and not c["negative"] and not c.get("avoid"):
        add("WARN", f"{model['label']} has a negative field and this clip has none.")

    ph = [m.group(0) for m in PLACEHOLDER.finditer(p)]
    if ph:
        add("FAIL", f"Unfilled placeholder: {ph[0]}{' (+%d more)' % (len(ph) - 1) if len(ph) > 1 else ''}.")

    for name, texts in locks.items():
        usable = [t for t in texts if not PLACEHOLDER.search(t)]
        if not usable:
            continue
        if name == "CHARACTER" and not people and "@avatar" not in low:
            continue
        if name == "PRODUCT" and "@product" in low:
            continue
        if re.search(r"keyframe|\.(png|jpe?g|webp)|photo|last frame", c.get("first_frame", ""), re.I):
            continue  # image-to-video: the image carries the look; motion only
        if not any(norm(t) in norm(p) for t in usable):
            add("WARN", f"{name} lock is not pasted word for word. Rephrased locks are how faces and products drift.")

    if c["duration"] and c["duration"] not in [float(d) for d in model["durations"]]:
        add("WARN", f"{c['duration']:g}s is not a length {model['label']} generates ({', '.join(map(str, model['durations']))}s).")
    return res


def lint_image(c, model, locks):
    if c.get("missing"):
        return [("FAIL", "No fenced prompt block under this heading.")]
    p = c["prompt"]
    low = p.lower()
    clean = low
    for pat in CLEAN_PHRASES:
        clean = re.sub(pat, " ", clean)
    res = []
    add = lambda lv, m: res.append((lv, m))
    words = len(re.findall(r"[\w'’-]+", p))
    lo, hi = model["words"]
    if words > hi * 1.5:
        add("FAIL", f"{words} words; {model['label']} works best at {lo}-{hi}.")
    elif words > hi or words < lo:
        add("WARN", f"{words} words, outside the {lo}-{hi} range for {model['label']}.")
    has_product = bool(locks.get("PRODUCT")) or re.search(r"\bproduct\b", low)
    if has_product and not REF_ANCHOR.search(p):
        add("FAIL", "Does not point at the product photo (say 'Image 1 is the product...').")
    if has_product and not KEEP_CLAUSE.search(p):
        add("WARN", "No keep clause: say the product stays exactly as in the photo (shape, colours, markings).")
    if not RATIO.search(p):
        add("WARN", "No ratio. Keyframes for Reels need 9:16 vertical.")
    if HOLD.search(p) and not GRIP.search(p):
        add("WARN", "Someone holds the product but the grip is not described (which hand, fingers, height).")
    found = [w for w in VAGUE if has(clean, w)]
    if found:
        add("WARN", f"Filler words: {', '.join(found)}.")
    names = [n for n in NAMES if has(low, n) and not (n == "magsafe" and "magsafe-compatible" in low)]
    if names and STRICT_NAMES:
        add("WARN", f"Named brand or IP: {', '.join(names)}. Some models refuse or blur names.")
    who = re.sub(r"\b(?:a |an |the )?(?:woman|man|girl|boy|person|child|kid)'s (?:right |left )?(?:hand|hands|finger|fingers|arm)\b", " ", clean)
    who = re.sub(r"\b(?:no|nobody|without (?:a|any)) (?:person|people|one)\b[^.]*", " ", who)
    people = {w for w in PEOPLE if has(who, w)}
    if any(has(who, w) for w in CROWD) or len(people) >= 3:
        add("WARN", "Several people: faces merge and hands multiply. One person per keyframe if you can.")
    if any(re.search(pat, clean) for pat in TEXT_ASKS):
        add("WARN", "Asks for text or a logo. Keep only the product's real markings; add the rest in the edit.")
    ph = [m.group(0) for m in PLACEHOLDER.finditer(p)]
    if ph:
        add("FAIL", f"Unfilled placeholder: {ph[0]}.")
    for name in ("STYLE", "CHARACTER"):
        usable = [t_ for t_ in locks.get(name, []) if not PLACEHOLDER.search(t_)]
        if not usable or (name == "CHARACTER" and not people):
            continue
        if not any(norm(t_) in norm(p) for t_ in usable):
            add("WARN", f"{name} lock is not pasted word for word; keyframes drift apart without it.")
    return res


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("input", nargs="?", default="-", help="prompt file, or - for stdin")
    ap.add_argument("--model", default="generic", help="key in models.json (default generic)")
    ap.add_argument("--target", type=float, help="target total length in seconds")
    ap.add_argument("--image-model", default="image-generic", help="image model for '## Keyframe N' blocks (default image-generic)")
    ap.add_argument("--check-names", action="store_true",
                    help="warn about named brands, teams and characters (off by default)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    global STRICT_NAMES
    STRICT_NAMES = args.check_names

    models = load_models()
    video = {k: v for k, v in models.items() if v.get("kind", "video") == "video"}
    images = {k: v for k, v in models.items() if v.get("kind") == "image"}
    if args.model in images and args.input:
        args.image_model, args.model = args.model, "generic"   # a file of image prompts only
        image_only = True
    else:
        image_only = False
    if args.model not in video:
        sys.exit(f"Unknown video model '{args.model}'. Choose from: {', '.join(video)}")
    if args.image_model not in images:
        sys.exit(f"Unknown image model '{args.image_model}'. Choose from: {', '.join(images)}")
    model, imodel = video[args.model], images[args.image_model]
    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    locks, clips = parse(raw)
    if image_only:
        for c in clips:
            c["kind"] = "image"
    if not clips:
        sys.exit("No prompts found. Put each prompt in a ``` fenced block, under '## Clip N · 5s' headings.")

    headed = any(re.match(r"(Clip|Shot|Scene|Cảnh|Canh|Keyframe) \d+$", c["label"], re.I) for c in clips)
    keyframe_nums = {re.search(r"(\d+)$", c["label"]).group(1) for c in clips if c["kind"] == "image" and headed}
    report, fails, warns = [], 0, 0
    for c in clips:
        r = lint_image(c, imodel, locks) if c["kind"] == "image" else lint_clip(c, model, args.model, locks)
        if c["kind"] == "video" and headed and not re.search(r"filmed", c.get("first_frame", ""), re.I):
            num_ = re.search(r"(\d+)$", c["label"]).group(1)
            if num_ not in keyframe_nums:
                r.append(("FAIL", f"No keyframe prompt for this clip. Add '### Keyframe {num_}' (product photo + prompt -> first frame)."))
            elif not re.search(r"keyframe", c.get("first_frame", ""), re.I):
                r.append(("WARN", f"First frame should be keyframe_c{num_}.png."))
        fails += sum(1 for lv, _ in r if lv == "FAIL")
        warns += sum(1 for lv, _ in r if lv == "WARN")
        report.append({"clip": c["label"], "duration": c["duration"], "issues": r})

    total_notes = []
    durs = [c["duration"] for c in clips if c["duration"] and c["kind"] == "video"]
    if args.target and durs:
        total = sum(durs)
        if abs(total - args.target) > max(3, args.target * 0.15):
            total_notes.append(f"Clips add up to {total:g}s generated against a {args.target:g}s target (trim in the edit, or change the plan).")

    if args.json:
        json.dump({"model": args.model, "fails": fails, "warns": warns, "clips": [
            {"clip": r["clip"], "duration": r["duration"],
             "issues": [{"level": lv, "message": m} for lv, m in r["issues"]]} for r in report],
            "notes": total_notes, "locks_found": sorted(locks)}, sys.stdout, indent=2)
        print()
    else:
        print(f"\nPROMPT LINT  ·  {model['label']} + {imodel['label']}  ·  {len(clips)} prompt(s)  ·  locks found: "
              f"{', '.join(sorted(locks)) or 'none'}")
        print("=" * 78)
        for r in report:
            d = f" · {r['duration']:g}s" if r["duration"] else ""
            if not r["issues"]:
                print(f"PASS  {r['clip']}{d}")
                continue
            worst = "FAIL" if any(lv == "FAIL" for lv, _ in r["issues"]) else "WARN"
            print(f"{worst}  {r['clip']}{d}")
            for lv, m in r["issues"]:
                print(f"      {lv:<4}  {m}")
        print("-" * 78)
        for n in total_notes:
            print(f"  - {n}")
        verdict = "FIX BEFORE GENERATING" if fails else ("REVIEW THE WARNINGS" if warns else "READY")
        print(f"{fails} fail, {warns} warn  ->  {verdict}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
