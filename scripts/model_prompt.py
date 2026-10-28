"""Model card -> CHARACTER lock, photo sheet prompt and look prompts (ad-creative/references/model-photo.md).

Usage: model_prompt.py <project> <cast/name.json> [--look id] [--image-n 2]
Reads projects/<project>/<card>, checks it, prints:
  - the CHARACTER lock (identity fields, in order) to paste under "Các khóa"
  - the Bước 0 sheet prompt (photograph, 4 views, studio) -> frames/<name>_sheet.png
  - one prompt per look, slots in the fixed order of model-photo.md §5
Exit code 1 when a check fails, so a card with a missing slot, a banned word or a fan item
that is not product.json world.cues[0] never reaches Flow.
"""
from __future__ import annotations

import argparse
import re
import sys

from common import load_json, project_dir

IDENTITY_REQUIRED = ["subject", "build", "skin", "face", "eyes", "hair", "fan_item", "outfit"]
IDENTITY_ORDER = ["subject", "build", "skin", "face", "eyes", "hair", "marks", "accessories", "fan_item", "outfit"]
LOOK_REQUIRED = ["id", "title", "shot", "setting", "expression", "pose", "camera", "light", "background", "focus", "quality"]
BANNED = ["sensual", "seductive", "sexy", "lingerie", "cleavage", "exposing", "revealing", "naked", "flawless"]
WARN_WORDS, FAIL_WORDS = 260, 380  # Nano Banana 2.1 in Flow: prompt_lint sweet spot / hard limit


def words(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9'’-]+", text))


def clause(*parts: str) -> str:
    return ", ".join(p.strip().rstrip(".,;") for p in parts if p and p.strip())


def character_lock(idn: dict) -> str:
    return clause(*(idn.get(k, "") for k in IDENTITY_ORDER))


def sheet_prompt(idn: dict) -> str:
    return ("Photograph, character reference sheet, one image, 16:9: a real person photographed in a studio, "
            "three full-body views (front, side, back) on the left, one chest-up close-up on the right, "
            "plain light-grey background, even soft light, real skin and fabric texture with visible pores, "
            "relaxed natural expression at the lens, no illustration, not a cartoon, no 3D render, no CGI. "
            f"{character_lock(idn)}. No other text, no watermark.")


def look_prompt(name: str, idn: dict, look: dict, image_n: int) -> str:
    person = dict(idn)
    if look.get("hair_style"):
        person["hair"] = look["hair_style"]
    if look.get("outfit"):
        person["outfit"] = look["outfit"]
    lines = [
        f"Photorealistic vertical 9:16 {look['shot']}, {look['setting']}, a genuine smartphone photo.",
        f"Image {image_n} is {name}: keep the exact face, skin tone and proportions; do not change the face.",
        f"{character_lock(person)}." + (f" Makeup: {look['makeup'].rstrip('.')}." if look.get("makeup") else ""),
        f"{look['expression'].rstrip('.;')}; {look['pose'].rstrip('.')}.",
        f"{look['camera'].rstrip('.')}.",
        f"{look['light'].rstrip('.')}.",
        f"Background: {look['background'].rstrip('.')}.",
        f"{look['focus'].rstrip('.;')}; {look['quality'].rstrip('.')}"
        + ("" if "pores" in look["quality"] else "; real skin texture with visible pores")
        + ("" if "beauty filter" in look["quality"] else ", no beauty filter")
        + ". No text, no watermark.",
    ]
    return "\n".join(l[:1].upper() + l[1:] for l in lines)


def check(card: dict, product: dict) -> list[str]:
    errs: list[str] = []
    idn = card.get("identity") or {}
    for k in IDENTITY_REQUIRED:
        if not str(idn.get(k, "")).strip():
            errs.append(f"identity.{k} trống")
    cues = ((product.get("world") or {}).get("cues") or [])
    if cues and cues[0].lower() not in str(idn.get("fan_item", "")).lower():
        errs.append(f"identity.fan_item phải chứa nguyên văn world.cues[0]: '{cues[0]}' (formats.md §4b)")
    if not card.get("looks"):
        errs.append("không có look nào")
    for lk in card.get("looks", []):
        for k in LOOK_REQUIRED:
            if not str(lk.get(k, "")).strip():
                errs.append(f"look {lk.get('id', '?')}: {k} trống")
    text = " ".join(str(v) for v in idn.values()) + " " + " ".join(str(v) for lk in card.get("looks", []) for v in lk.values())
    for w in BANNED:
        if re.search(rf"\b{w}\b", text, re.I):
            errs.append(f"từ cấm '{w}' (Flow từ chối / quảng cáo bị gắn cờ — model-photo.md §2)")
    return errs


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("card", help="đường dẫn trong project, ví dụ cast/kayla.json")
    ap.add_argument("--look", default="", help="chỉ in look này")
    ap.add_argument("--image-n", type=int, default=2, help="số thứ tự ảnh sheet trong danh sách ảnh tải lên")
    a = ap.parse_args()
    pdir = project_dir(a.project)
    card = load_json(pdir / a.card)
    product = load_json(pdir / "product.json") if (pdir / "product.json").exists() else {}
    errs = check(card, product)
    name, idn = card.get("name", "?"), card.get("identity", {})

    print(f"**CHARACTER - {name} (nhân vật):**\n{character_lock(idn)}\n")
    sp = sheet_prompt(idn)
    print(f"**Sheet ({words(sp)} từ) — Lưu thành:** `{name.lower()}_sheet.png`\n```\n{sp}\n```\n")
    for lk in card.get("looks", []):
        if a.look and lk.get("id") != a.look:
            continue
        if any(not str(lk.get(k, "")).strip() for k in LOOK_REQUIRED):
            continue
        lp = look_prompt(name, idn, lk, a.image_n)
        n = words(lp)
        flag = " — QUÁ DÀI" if n > FAIL_WORDS else (" — dài, nên rút" if n > WARN_WORDS else "")
        if n > FAIL_WORDS:
            errs.append(f"look {lk['id']}: {n} từ > {FAIL_WORDS}")
        print(f"**Look `{lk['id']}` — {lk['title']} ({n} từ{flag})**\n```\n{lp}\n```\n")

    if errs:
        print("FAIL:\n - " + "\n - ".join(errs))
        sys.exit(1)
    print("OK: thẻ mẫu đủ mục, không từ cấm, đồ fan đúng world.cues[0]")


if __name__ == "__main__":
    main()
