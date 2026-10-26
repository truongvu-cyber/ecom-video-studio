"""Find and download music for an ad, add it to music-library/tags.json.

Usage:
  fetch_music.py "<mood words>" [--count 3] [--bpm 75 95]   search YouTube, keep the best fits
  fetch_music.py --url <link> [--mood "chill lofi"]          a track the user points at (any site yt-dlp reads)

The user allowed any source for INTERNAL use (2026-10-23): every track fetched here is
tagged "INTERNAL ONLY" so the edit report flags it before anyone runs it as a paid ad.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

from common import MUSIC_LIBRARY, load_json, save_json

YTDLP = str(Path(sys.executable).parent / "yt-dlp")
MIN_SEC, MAX_SEC = 60, 420
SECTION = "*00:30-02:00"  # long mixes: take 90 s past the intro


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:50] or "track"


def search(query: str, n: int) -> list[dict]:
    out = subprocess.run([YTDLP, "--flat-playlist", "-J", f"ytsearch{n}:{query}"],
                         capture_output=True, text=True, check=True).stdout
    return [e for e in json.loads(out).get("entries", []) if e.get("id")]


def download(url: str, name: str, section: str | None) -> Path:
    MUSIC_LIBRARY.mkdir(exist_ok=True)
    tmpl = str(MUSIC_LIBRARY / f"{name}.%(ext)s")
    cmd = [YTDLP, "-x", "--audio-format", "mp3", "--audio-quality", "2", "--no-playlist",
           "-o", tmpl, url]
    if section:
        cmd[1:1] = ["--download-sections", section, "--force-keyframes-at-cuts"]
    subprocess.run(cmd, capture_output=True, text=True, check=True)
    path = MUSIC_LIBRARY / f"{name}.mp3"
    if not path.exists():
        raise RuntimeError(f"Tải không thành công: {url}")
    return path


def register(path: Path, title: str, url: str, moods: list[str]) -> dict:
    from beat_detect import analyze

    a = analyze(path)
    tags = load_json(MUSIC_LIBRARY / "tags.json")
    tags["tracks"] = [t for t in tags["tracks"] if t["file"] != path.name]
    entry = {"file": path.name, "title": title, "source_url": url, "mood": moods,
             "bpm": a["bpm"], "drop_sec": a["drop_sec"], "duration": a["duration"],
             "license": f"INTERNAL ONLY — fetched from {url}, rights not cleared for paid ads",
             "allowed_platforms": ["internal"], "expires": None}
    tags["tracks"].append(entry)
    save_json(MUSIC_LIBRARY / "tags.json", tags)
    return entry


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("query", nargs="?")
    ap.add_argument("--url")
    ap.add_argument("--mood", default="")
    ap.add_argument("--count", type=int, default=3)
    ap.add_argument("--bpm", type=float, nargs=2)
    args = ap.parse_args()
    if not args.query and not args.url:
        sys.exit("Cần từ khoá tìm kiếm hoặc --url")

    moods = [w for w in re.findall(r"[a-z]+", (args.mood or args.query or "").lower())
             if w not in {"music", "instrumental", "no", "copyright", "song", "track", "beat", "beats"}]
    added = []
    if args.url:
        info = json.loads(subprocess.run([YTDLP, "-J", "--no-playlist", args.url],
                                         capture_output=True, text=True, check=True).stdout)
        long_mix = (info.get("duration") or 0) > MAX_SEC
        path = download(args.url, slug(info.get("title", "track")), SECTION if long_mix else None)
        added.append(register(path, info.get("title", ""), args.url, moods))
    else:
        found = search(f"{args.query} instrumental", 15)
        short = [e for e in found if MIN_SEC <= (e.get("duration") or 0) <= MAX_SEC]
        picks = (short or found)[: args.count * 2]
        for e in picks:
            if len(added) >= args.count:
                break
            url = f"https://www.youtube.com/watch?v={e['id']}"
            long_mix = (e.get("duration") or 0) > MAX_SEC
            try:
                path = download(url, f"{slug(e.get('title', ''))}-{e['id']}", SECTION if long_mix else None)
                entry = register(path, e.get("title", ""), url, moods)
            except (subprocess.CalledProcessError, RuntimeError) as err:
                print(f"bỏ qua {url}: {str(err).splitlines()[0][:120]}")
                continue
            if args.bpm and entry["bpm"] and not (args.bpm[0] <= entry["bpm"] <= args.bpm[1]):
                print(f"  ({entry['bpm']} BPM ngoài khoảng {args.bpm}, vẫn giữ trong thư viện)")
            added.append(entry)

    for t in added:
        print(f"+ {t['file']}: {t['bpm']} BPM, drop {t['drop_sec']}s, {t['duration']}s — {t['title'][:70]}")
    if not added:
        sys.exit("Không tải được bài nào")


if __name__ == "__main__":
    main()
