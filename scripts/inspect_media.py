"""Inspect every take and pick one per file_pattern on technical grounds.

Usage: inspect_media.py <project>
Writes edit/media.json. Visual/print checks (méo sản phẩm, sai chữ) are NOT done here:
the agent reviews the contact sheets with its own eyes (/watch) and can force a take
via shots[].chosen_take.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

from common import load_json, loudness, media_info, project_dir, ratio_of, save_json

MIN_SEC = 2.0


def black_intervals(path: Path) -> list[list[float]]:
    res = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-an",
                          "-vf", "blackdetect=d=0.1:pic_th=0.95", "-f", "null", "-"],
                         capture_output=True, text=True)
    out = []
    for m in re.finditer(r"black_start:([\d.]+) black_end:([\d.]+)", res.stderr):
        out.append([float(m.group(1)), float(m.group(2))])
    return out


def assess(path: Path, prod: dict, needs_audio: bool) -> dict:
    info = media_info(path)
    issues, reject = [], False
    want = prod["spec"]["ratio"]
    if "width" not in info:
        return {"file": path.name, "reject": True, "issues": ["không có hình"], "score": 0, **info}
    got = ratio_of(info["width"], info["height"])
    if got != want.replace(" ", ""):
        issues.append(f"sai tỉ lệ {got} (cần {want})")
        reject = True
    if info["duration"] < MIN_SEC:
        issues.append(f"quá ngắn {info['duration']:.1f}s")
        reject = True
    if needs_audio and not info["has_audio"]:
        issues.append("clip thoại nhưng không có tiếng")
        reject = True
    blacks = black_intervals(path)
    black_sec = sum(b - a for a, b in blacks)
    if black_sec > 0:
        issues.append(f"khung đen {black_sec:.1f}s")
    loud = loudness(path) if info["has_audio"] else {"input_i": None}
    if needs_audio and (loud["input_i"] is None or loud["input_i"] < -45):
        issues.append("tiếng gần như im lặng")
        reject = True
    usable = info["duration"] - black_sec
    score = 0 if reject else round(100 * usable / info["duration"] - 5 * len(issues), 1)
    return {"file": path.name, **info, "black": blacks, "loudness_i": loud["input_i"],
            "issues": issues, "reject": reject, "score": score}


def main() -> None:
    project = project_dir(sys.argv[1])
    prod = load_json(project / "production.json")
    clips_dir = project / "clips"

    patterns: dict[str, dict] = {}
    for s in prod["shots"]:
        p = patterns.setdefault(s["file_pattern"], {"needs_audio": False, "forced": None, "shots": []})
        p["shots"].append(s["id"])
        p["needs_audio"] |= s["audio_type"] == "dialogue"
        if s.get("chosen_take"):
            p["forced"] = s["chosen_take"]

    result = {"takes": {}, "chosen": {}, "problems": []}
    for pattern, p in patterns.items():
        files = sorted(clips_dir.glob(pattern))
        assessed = [assess(f, prod, p["needs_audio"]) for f in files]
        for a in assessed:
            result["takes"][a["file"]] = a
        if p["forced"]:
            chosen = p["forced"]
            if chosen not in result["takes"]:
                result["problems"].append(f"{pattern}: chosen_take {chosen} không tồn tại")
                continue
        else:
            ok = [a for a in assessed if not a["reject"]]
            if not ok:
                result["problems"].append(f"{pattern} (shot {', '.join(p['shots'])}): mọi take đều lỗi, cần gen lại")
                continue
            chosen = max(ok, key=lambda a: a["score"])["file"]
        result["chosen"][pattern] = chosen

    save_json(project / "edit" / "media.json", result)
    for f, a in result["takes"].items():
        mark = "REJECT" if a["reject"] else f"score {a['score']}"
        print(f"{f:14} {mark:12} {'; '.join(a['issues'])}")
    for pattern, f in result["chosen"].items():
        print(f"chọn {pattern} -> {f}")
    if result["problems"]:
        for msg in result["problems"]:
            print("LỖI:", msg)
        sys.exit(1)


if __name__ == "__main__":
    main()
