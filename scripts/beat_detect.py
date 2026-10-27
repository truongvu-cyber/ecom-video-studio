"""Pick the music track and find its beats and drop.

Usage: beat_detect.py <project>
music.source: file -> that file; auto -> best match in music-library/tags.json
(license filled in, mood overlap, bpm in range); none -> no music.
Writes edit/music.json.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import numpy as np

from common import MUSIC_LIBRARY, ROOT, load_json, project_dir, run, save_json


def used_elsewhere(project: Path) -> set[str]:
    """Track files other projects already used (user rule 2026-10-27: every ad gets a new track)."""
    used = set()
    for m in (ROOT / "projects").glob("*/edit/music.json"):
        if m.parent.parent == project:
            continue
        f = (load_json(m) or {}).get("file")
        if f:
            used.add(Path(f).name)
    return used


def pick_auto(music: dict, exclude: set[str] = frozenset()) -> tuple[Path | None, str, int]:
    tags = load_json(MUSIC_LIBRARY / "tags.json").get("tracks", [])
    moods = set((music.get("mood") or "").lower().replace(",", " ").split())
    lo, hi = (music.get("bpm_range") or [0, 999])
    best, best_key, best_score = None, None, -1
    for t in tags:
        f = MUSIC_LIBRARY / t["file"]
        lic = t.get("license") or ""
        if not f.exists() or not lic or lic.startswith("TODO") or t["file"] in exclude:
            continue
        # the synthetic test beat must never end up in a real ad
        if lic.startswith("TEST ONLY") and os.environ.get("ALLOW_TEST_MUSIC") != "1":
            continue
        overlap = len(moods & set(t.get("mood", [])))
        if overlap == 0:
            continue  # right tempo but wrong mood (e.g. a rap track for a lo-fi ad) is not a match
        score = overlap * 2 + (1 if t.get("bpm") and lo <= t["bpm"] <= hi else 0)
        # ties: closest tempo to the middle of the range, then file name (never insertion order)
        mid = (lo + hi) / 2
        key = (score, -abs((t.get("bpm") or mid) - mid), t["file"])
        if best is None or key > best_key:
            best, best_key, best_score = (f, lic), key, score
    if not best:
        return None, "không có bài nào trong music-library khớp mood", -1
    return best[0], best[1], int(best_score)


def analyze(path: Path) -> dict:
    import librosa

    sr = 22050
    raw = run(["ffmpeg", "-v", "error", "-i", str(path), "-vn", "-ac", "1", "-ar", str(sr),
               "-f", "s16le", "-"], text=False).stdout
    y = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768
    # track the kick/bass band of the percussive part: full-band onsets often lock onto
    # off-beat hi-hats, which puts every cut half a beat early
    perc = librosa.effects.percussive(y)
    env = librosa.onset.onset_strength(y=perc, sr=sr, fmax=250, n_mels=32)
    tempo, beats = librosa.beat.beat_track(onset_envelope=env, sr=sr, units="time")
    rms = librosa.feature.rms(y=y)[0]
    times = librosa.times_like(rms, sr=sr)
    # drop = point where the next 2s are loudest compared with the previous 2s
    win = max(1, int(2.0 / (times[1] - times[0])))
    c = np.concatenate([[0.0], np.cumsum(rms)])
    idx = np.arange(len(rms))
    rise = np.full(len(rms), -np.inf)
    ok = (idx >= win) & (idx + win <= len(rms))
    i = idx[ok]
    rise[ok] = (c[i + win] - c[i]) / win - (c[i] - c[i - win]) / win
    valid = (times > 2.0) & ok
    drop = float(times[valid][np.argmax(rise[valid])]) if valid.any() else None
    if drop is not None and len(beats):
        drop = float(beats[np.argmin(np.abs(beats - drop))])  # snap drop to a beat
    # librosa's tempo is a coarse grid estimate; the average beat spacing is the real tempo
    bpm = 60.0 * (len(beats) - 1) / float(beats[-1] - beats[0]) if len(beats) > 1 else float(np.atleast_1d(tempo)[0])
    return {"bpm": round(bpm, 1),
            "beats": [round(float(b), 3) for b in beats],
            "drop_sec": round(drop, 3) if drop is not None else None,
            "duration": round(len(y) / sr, 3)}


def main() -> None:
    project = project_dir(sys.argv[1])
    music = load_json(project / "production.json")["music"]
    out = project / "edit" / "music.json"
    if music["source"] == "none":
        save_json(out, {"file": None})
        print("Không dùng nhạc")
        return
    if music["source"] == "file":
        f = ROOT / music["file"] if (ROOT / music["file"]).exists() else project / music["file"]
        license_note = "nhạc do người dùng cung cấp"
    else:
        exclude = used_elsewhere(project)
        f, license_note, score = pick_auto(music, exclude)
        # nothing unused in the library fits the mood: fetch new tracks (user allowed any
        # source for internal use; search leans on what is current) and pick again
        if (f is None or score < 1) and music.get("allow_fetch", True) and music.get("mood"):
            print(f"Thư viện không còn bài mới hợp '{music['mood']}' (đã loại {len(exclude)} bài project khác dùng), đang tìm nhạc mới...")
            cmd = [sys.executable, str(Path(__file__).parent / "fetch_music.py"), f"{music['mood']} 2026",
                   "--mood", music["mood"], "--count", "3"]
            if music.get("bpm_range"):
                cmd += ["--bpm", *map(str, music["bpm_range"])]
            subprocess.run(cmd)
            f, license_note, score = pick_auto(music, exclude)
        if f is None:
            sys.exit(f"LỖI: {license_note}")
    data = {"file": str(f.resolve()), "license": license_note, **analyze(f)}
    save_json(out, data)
    print(f"{f.name}: {data['bpm']} BPM, {len(data['beats'])} beat, drop {data['drop_sec']}s, dài {data['duration']}s")


if __name__ == "__main__":
    main()
