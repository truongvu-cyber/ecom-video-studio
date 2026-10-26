"""Measure each chosen take so the cut can land on the right moment.

Usage: find_moments.py <project>
Writes edit/moments.json: per take, a motion profile (10 Hz), the biggest
appearance change ("split", where Veo switched to the second action), the
busiest window ("peak") and the calmest window ("calm") for the shot lengths
the plan asks for. build_timeline.py uses these when a shot sets
`moment: a | b | peak | calm`.
"""
from __future__ import annotations

import sys

import numpy as np

from common import load_json, project_dir, run, save_json

FPS = 10
W, H = 64, 114
HEAD = 0.25  # skip the first frames of a Veo clip
EDGE = 0.4   # keep windows this far from the clip edges


def frames_of(path) -> np.ndarray:
    raw = run(["ffmpeg", "-v", "error", "-i", str(path), "-an", "-vf",
               f"fps={FPS},scale={W}:{H},format=gray", "-f", "rawvideo", "-"], text=False).stdout
    return np.frombuffer(raw, dtype=np.uint8).reshape(-1, H, W).astype(np.float32) / 255.0


def profile(fr: np.ndarray) -> dict:
    n = len(fr)
    dur = n / FPS
    motion = np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2))  # n-1 values, index i = between frame i and i+1
    motion = np.concatenate([[motion[0]], motion]) if n > 1 else np.zeros(n)

    # split: time where the picture before differs most from the picture after (1 s windows)
    win = FPS
    best_t, best_d = dur / 2, 0.0
    for i in range(win + int(HEAD * FPS), n - win):
        d = float(np.abs(fr[i - win:i].mean(axis=0) - fr[i:i + win].mean(axis=0)).mean())
        if d > best_d:
            best_t, best_d = i / FPS, d
    typical = float(np.median([np.abs(fr[i - win:i].mean(axis=0) - fr[i:i + win].mean(axis=0)).mean()
                               for i in range(win, n - win, max(1, (n - 2 * win) // 20))] or [1e-6]))
    strength = best_d / max(typical, 1e-6)

    # the change is usually a camera move (pan to the door, push in): the second action
    # starts where that move settles, not where it begins
    thr = float(np.median(motion)) * 1.5
    i = int(best_t * FPS)
    while i < n - 1 and (i / FPS) < best_t + 1.5 and motion[i] > thr:
        i += 1
    settled = i / FPS

    return {"duration": round(dur, 3), "motion": [round(float(m), 4) for m in motion],
            "split": round(best_t, 2), "settled": round(settled, 2), "split_strength": round(strength, 2),
            "split_reliable": strength >= 2.0}


def window(motion: list[float], dur: float, length: float, lo: float, hi: float, want: str) -> float:
    """Start time of the `length`-second window with max ('peak') or min ('calm') motion inside [lo, hi]."""
    m = np.array(motion)
    k = max(1, int(round(length * FPS)))
    starts = range(int(lo * FPS), max(int(lo * FPS) + 1, int((min(hi, dur) - length) * FPS) + 1))
    scores = [(m[s:s + k].mean(), s) for s in starts if s + k <= len(m)]
    if not scores:
        return lo
    pick = max(scores) if want == "peak" else min(scores)
    return round(pick[1] / FPS, 2)


def main() -> None:
    project = project_dir(sys.argv[1])
    prod = load_json(project / "production.json")
    media = load_json(project / "edit" / "media.json")

    lengths: dict[str, set[float]] = {}
    for s in prod["shots"]:
        take = media["chosen"].get(s["file_pattern"])
        if take:
            lengths.setdefault(take, set()).add(round(float(s["use_sec"]) * float(s.get("speed", 1.0)), 2))

    out = {}
    for take, lens in lengths.items():
        fr = frames_of(project / "clips" / take)
        p = profile(fr)
        dur = p["duration"]
        second = p["settled"] if p["split_reliable"] else dur / 2
        p["windows"] = {}
        for L in sorted(lens):
            p["windows"][str(L)] = {
                "a": round(HEAD, 2),
                "b": round(min(second + 0.1, max(HEAD, dur - L - 0.05)), 2),
                "peak": window(p["motion"], dur, L, HEAD, dur - EDGE, "peak"),
                "calm": window(p["motion"], dur, L, HEAD, dur - EDGE, "calm"),
            }
        out[take] = p
        flag = f", ổn định từ {p['settled']}s" if p["split_reliable"] else " (yếu, dùng giữa clip)"
        print(f"{take}: đổi hành động ở {p['split']}s{flag}; "
              + "; ".join(f"{L}s → peak {w['peak']}s, calm {w['calm']}s" for L, w in p["windows"].items()))

    save_json(project / "edit" / "moments.json", out)


if __name__ == "__main__":
    main()
