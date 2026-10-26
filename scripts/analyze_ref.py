"""Measure a reference (winning) video for mode C of ad-creative.

Usage: analyze_ref.py <project> refs/<file>.mp4 [--threshold 0.3]
Writes refs/<stem>/analysis.json and refs/<stem>/sheet.jpg (one frame per scene).
The agent turns this into the beat table; the numbers here are measurements only.
"""
from __future__ import annotations

import argparse
import subprocess
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from common import inside, media_info, project_dir, run, save_json

FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
MIN_SCENE = 0.25


def scene_cuts(video: Path, threshold: float, fps: float) -> list[float]:
    """Hard cuts = frames whose colour difference to the previous frame spikes.

    ffmpeg's scene score is luma-weighted and misses cuts between shots of similar
    brightness, so compare small RGB frames directly.
    """
    w, h = 48, 84
    raw = run(["ffmpeg", "-v", "error", "-i", str(video), "-an", "-vf", f"scale={w}:{h}",
               "-pix_fmt", "rgb24", "-f", "rawvideo", "-"], text=False).stdout
    frames = np.frombuffer(raw, dtype=np.uint8).reshape(-1, h, w, 3).astype(np.float32)
    if len(frames) < 2:
        return []
    diff = np.abs(np.diff(frames, axis=0)).mean(axis=(1, 2, 3)) / 255.0
    out: list[float] = []
    for i, d in enumerate(diff):
        lo, hi = max(0, i - 15), min(len(diff), i + 16)
        local = np.median(np.concatenate([diff[lo:i], diff[i + 1:hi]])) if hi - lo > 1 else 0
        if d > threshold * 0.25 and d > 4 * local + 0.01:
            t = round((i + 1) / fps, 3)
            if not out or t - out[-1] >= MIN_SCENE:
                out.append(t)
    return out


def transcript(video: Path) -> list[dict]:
    try:
        import mlx_whisper
    except ImportError:
        return []
    from transcribe import DEFAULT_MODEL, word_list

    res = mlx_whisper.transcribe(str(video), path_or_hf_repo=DEFAULT_MODEL,
                                 word_timestamps=True, verbose=None)
    return word_list(res, video)


def music_bpm(video: Path) -> float | None:
    import librosa

    raw = run(["ffmpeg", "-v", "error", "-i", str(video), "-vn", "-ac", "1", "-ar", "22050",
               "-f", "s16le", "-"], text=False).stdout
    y = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768
    if len(y) < 22050 * 3 or np.sqrt((y ** 2).mean()) < 1e-3:
        return None
    perc = librosa.effects.percussive(y)
    env = librosa.onset.onset_strength(y=perc, sr=22050, fmax=250, n_mels=32)
    _, beats = librosa.beat.beat_track(onset_envelope=env, sr=22050, units="time")
    if len(beats) < 8:
        return None
    return round(60.0 * (len(beats) - 1) / float(beats[-1] - beats[0]), 1)


def contact_sheet(video: Path, scenes: list[dict], info: dict, dest: Path) -> None:
    font = ImageFont.truetype(FONT, 16)
    tw = 216
    th = int(tw * info["height"] / info["width"])
    cols = min(6, len(scenes))
    rows = (len(scenes) + cols - 1) // cols
    canvas = Image.new("RGB", (cols * tw, rows * (th + 40)), "#111")
    with tempfile.TemporaryDirectory() as td:
        for i, s in enumerate(scenes):
            f = Path(td) / f"{i}.jpg"
            t = (s["start"] + s["end"]) / 2
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", str(video),
                            "-frames:v", "1", "-q:v", "3", str(f)], check=True)
            x, y = (i % cols) * tw, (i // cols) * (th + 40)
            canvas.paste(Image.open(f).resize((tw, th)), (x, y + 40))
            d = ImageDraw.Draw(canvas)
            d.text((x + 6, y + 2), f"#{i + 1} {s['start']:.1f}-{s['end']:.1f}s", font=font, fill="white")
            d.text((x + 6, y + 20), f"{s['end'] - s['start']:.1f}s", font=font, fill="#ffd60a")
    canvas.save(dest, quality=88)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("video")
    ap.add_argument("--threshold", type=float, default=0.3)
    args = ap.parse_args()

    project = project_dir(args.project, need_production=False)
    video = inside(project, args.video)
    info = media_info(video)
    dur = info["duration"]
    cuts = scene_cuts(video, args.threshold, info.get("fps") or 30.0)
    bounds = [0.0] + [c for c in cuts if 0 < c < dur] + [dur]
    scenes = [{"start": round(a, 2), "end": round(b, 2)} for a, b in zip(bounds, bounds[1:])]

    words = transcript(video) if info["has_audio"] else []
    for s in scenes:
        s["words"] = " ".join(w["w"] for w in words if s["start"] <= w["end"] - 0.05 < s["end"])  # whisper starts run early; ends are reliable
    speech = sum(w["end"] - w["start"] for w in words)

    out_dir = project / "refs" / video.stem
    out_dir.mkdir(parents=True, exist_ok=True)
    analysis = {
        "file": args.video, "duration": round(dur, 2),
        "size": f"{info.get('width')}x{info.get('height')}",
        "scenes": scenes, "scene_count": len(scenes),
        "avg_shot_sec": round(dur / len(scenes), 2),
        "cuts_per_sec": round((len(scenes) - 1) / dur, 2) if dur else 0,
        "speech_share": round(speech / dur, 2) if dur else 0,
        "word_count": len(words),
        "words_per_sec_when_talking": round(len(words) / speech, 2) if speech else 0,
        "music_bpm": music_bpm(video) if info["has_audio"] else None,
        "transcript": " ".join(w["w"] for w in words),
        "words": words,
    }
    save_json(out_dir / "analysis.json", analysis)
    contact_sheet(video, scenes, info, out_dir / "sheet.jpg")

    print(f"{video.name}: {dur:.1f}s, {len(scenes)} cảnh, trung bình {analysis['avg_shot_sec']}s/cảnh, "
          f"lời chiếm {analysis['speech_share']:.0%}, nhạc {analysis['music_bpm']} BPM")
    for i, s in enumerate(scenes, 1):
        print(f"  #{i} {s['start']:5.1f}-{s['end']:5.1f}s  {s['words']}")
    print(f"-> {out_dir.relative_to(project)}/analysis.json, sheet.jpg")


if __name__ == "__main__":
    main()
