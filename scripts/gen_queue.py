"""prompts.md + production.json -> edit/gen_queue.json: the fixed order of generation jobs.

Usage: gen_queue.py <project>
The queue is what the browser automation (or the user, by hand) executes:
character sheet -> keyframes (each checked) -> clips. Every job carries the
exact prompt, the reference files to upload, the mode, the output file name,
the checks that decide pass/fail and the retry budget. Nothing about a run is
improvised: a job not in this file is not generated.
"""
from __future__ import annotations

import re
import sys

from common import load_json, project_dir, save_json

MAX_RETRIES_PER_PROJECT = 2  # extra generations allowed beyond one per job
# Flow settings the user fixed on 2026-10-27 (see ad-creative/references/flow-runbook.md)
IMAGE_TOOL = "nano-banana-2.1"
VIDEO_TOOL = "omni-1.1-flash"
VIDEO_MODE = "ingredients"
DOWNLOAD = {"image": "1K", "video": "1080p"}  # image: original size, no upscale wait (only used for review); never a credit option


def fenced(block: str) -> str:
    m = re.search(r"```[a-z]*\n(.*?)```", block, re.S)
    return m.group(1).strip() if m else ""


def sections(md: str, pattern: str) -> list[tuple[str, str]]:
    """(heading, body) for every heading matching pattern, body until the next heading of same level."""
    out = []
    lines = md.splitlines()
    starts = [i for i, l in enumerate(lines) if re.match(pattern, l)]
    for k, i in enumerate(starts):
        level = len(lines[i]) - len(lines[i].lstrip("#"))
        end = len(lines)
        for j in range(i + 1, len(lines)):
            if lines[j].startswith("#") and (len(lines[j]) - len(lines[j].lstrip("#"))) <= level:
                end = j
                break
        out.append((lines[i], "\n".join(lines[i + 1:end])))
    return out


def field(body: str, *labels: str) -> str:
    for lab in labels:
        m = re.search(rf"\*\*{lab}[^*]*\*\*:?\s*([^\n·]+)", body)
        if m:
            return m.group(1).strip()
    return ""


def refs_of(body: str) -> list[str]:
    """`product.png`, `maya_sheet.png`, `keyframe_c1.png` named in the upload line, in order."""
    line = field(body, "Ảnh tải lên", "References")
    return [m.strip("`") for m in re.findall(r"`([^`]+\.(?:png|jpg|jpeg|webp))`", line)]


def main() -> None:
    project = project_dir(sys.argv[1])
    prod = load_json(project / "production.json")
    md = (project / "prompts.md").read_text(encoding="utf-8")
    jobs = []

    # character sheet(s): fenced block(s) under "Bước 0" whose save-as name ends in _sheet.png
    for head, body in sections(md, r"^## (Bước 0|Step 0)"):
        for m in re.finditer(r"```[a-z]*\n(.*?)```\s*\n\s*\*\*(?:Lưu thành|Save as)[^*]*\*\*:?\s*`?([^`\n]+_sheet\.png)`?",
                             body, re.S):
            jobs.append({"kind": "image", "id": m.group(2).replace(".png", ""), "tool": IMAGE_TOOL,
                         "prompt": m.group(1).strip(), "refs": [], "ratio": "16:9",
                         "save_as": f"frames/{m.group(2)}", "checks": ["one person, no text, no watermark"]})

    for head, body in sections(md, r"^### (Keyframe|Khung) *\d+"):
        n = int(re.search(r"(\d+)", head).group(1))
        save = field(body, "Lưu thành", "Save as").strip("`") or f"keyframe_c{n}.png"
        jobs.append({"kind": "image", "id": f"keyframe_c{n}", "tool": IMAGE_TOOL,
                     "prompt": fenced(body), "refs": refs_of(body), "ratio": "9:16",
                     "save_as": f"frames/{save}", "download": DOWNLOAD["image"],
                     "checks": [c.strip() for c in field(body, "Soát trước khi làm video", "Check before animating").split("·") if c.strip()],
                     "scene": field(body, "Cảnh")})

    for head, body in sections(md, r"^## Clip *\d+"):
        n = int(re.search(r"(\d+)", head).group(1))
        first = field(body, "Khung đầu", "First frame")
        ingredients = bool(re.search(r"ingredient", body, re.I))
        refs = re.findall(r"`([^`]+\.(?:png|jpg|jpeg|webp))`", field(body, "Khung đầu", "First frame")) or \
            re.findall(r"`([^`]+\.(?:png|jpg|jpeg|webp))`", body.split("```")[0])
        neg = field(body, "Phủ định", "Negative")
        strict = any(s.get("print_fidelity") == "strict" and s["file_pattern"].startswith(f"c{n:02d}")
                     for s in prod["shots"])
        prompt = fenced(body)
        if strict:
            # Runbook §3b: Omni in ingredients mode swapped the print on cubs c04 (VW logo) when the
            # keyframe was the only ingredient. For strict-print clips the print source (the first
            # upload of that clip's keyframe, i.e. the product/design file) goes FIRST in the
            # ingredients and the prompt names it.
            kf = next((j for j in jobs if j["id"] == f"keyframe_c{n}"), None)
            if kf and kf["refs"]:
                refs = [kf["refs"][0]] + [r for r in refs if r != kf["refs"][0]]
            prompt = ("The printed design in this clip is exactly the one in the first reference image; "
                      "keep it unchanged, sharp and identical in every frame. " + prompt)
        jobs.append({"kind": "video", "id": f"c{n:02d}", "tool": VIDEO_TOOL,
                     "mode": VIDEO_MODE,  # user rule 2026-10-27: every clip via Thành phần (ingredients)
                     "prompt": prompt, "negative": neg,
                     "refs": [r for r in dict.fromkeys(refs)], "duration": 8, "ratio": "9:16", "resolution": "1080p",
                     "save_as": f"clips/c{n:02d}_a.mp4", "retry_as": f"clips/c{n:02d}_b.mp4",
                     "download": DOWNLOAD["video"],
                     "scene": field(body, "Cảnh"), "strict_print": strict})

    queue = {"project_id": prod["project_id"], "retry_budget": MAX_RETRIES_PER_PROJECT,
             "order": "images first; a clip is generated only after its first-frame image passed its checks",
             "jobs": jobs}
    save_json(project / "edit" / "gen_queue.json", queue)
    imgs = [j for j in jobs if j["kind"] == "image"]
    vids = [j for j in jobs if j["kind"] == "video"]
    print(f"{len(imgs)} ảnh, {len(vids)} clip, hạn mức gen lại {MAX_RETRIES_PER_PROJECT} -> edit/gen_queue.json")
    for j in jobs:
        extra = f" mode={j['mode']}" if j["kind"] == "video" else ""
        print(f"  {j['kind']:5} {j['id']:14} refs={j['refs']}{extra} -> {j['save_as']}")


if __name__ == "__main__":
    main()
