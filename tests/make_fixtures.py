"""Build a fake project (projects/demo-hoodie) that imitates Veo 3 output.

- c01_a: 8s dialogue clip (macOS `say`), the one voice clip shared by 3 shots
- c01_b: same take rendered 1080x1080 -> must be rejected (wrong ratio)
- c02_a: sfx clip; c03_a: b-roll with 2s black head; c03_b: clean b-roll -> c03_b should win
- music-library/test-beat-120.wav: synthetic 120 BPM track with an energy drop at 8s
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from common import MUSIC_LIBRARY, ROOT, save_json  # noqa: E402

SR = 48000
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
PROJECT = ROOT / "projects" / "demo-hoodie"


def card(path: Path, size: tuple[int, int], color: str, label: str) -> None:
    img = Image.new("RGB", size, color)
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT, 90)
    # a face-like block in the upper half so QC can see if overlays cover it
    w, h = size
    d.ellipse([w * 0.3, h * 0.18, w * 0.7, h * 0.40], fill="#f2c9a0")
    d.multiline_text((w / 2, h * 0.55), label, font=font, fill="white", anchor="mm", align="center")
    img.save(path)


def ambient(sec: float, level: float = 0.003) -> np.ndarray:
    rng = np.random.default_rng(1)
    return rng.normal(0, level, int(sec * SR)).astype(np.float32)


def speech_track(sec: float, tmp: Path) -> np.ndarray:
    """Three lines with real pauses so the cutter has silences to work with."""
    lines = ["Wait, you can put his name on it?", "Any name, any color.", "The link is right below."]
    out = ambient(sec)
    t = 0.6
    for i, line in enumerate(lines):
        aiff = tmp / f"line{i}.aiff"
        subprocess.run(["say", "-v", "Samantha", "-r", "175", "-o", str(aiff), line], check=True)
        wav = tmp / f"line{i}.wav"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(aiff), "-ar", str(SR), "-ac", "1", str(wav)], check=True)
        y, _ = sf.read(wav, dtype="float32")
        s = int(t * SR)
        out[s:s + len(y)] += y[: max(0, len(out) - s)] * 0.8
        t += len(y) / SR + 0.55
    return out


def sfx_track(sec: float) -> np.ndarray:
    out = ambient(sec)
    rng = np.random.default_rng(2)
    for start in np.arange(0.8, sec - 0.5, 1.3):  # rustle bursts
        n = int(0.25 * SR)
        burst = rng.normal(0, 0.08, n) * np.hanning(n)
        s = int(start * SR)
        out[s:s + n] += burst.astype(np.float32)
    return out


def make_clip(name: str, label: str, color: str, audio: np.ndarray | None, size=(1080, 1920),
              black_head: float = 0.0, sec: float = 8.0, tmp: Path | None = None) -> None:
    png = tmp / f"{name}.png"
    card(png, size, color, label)
    wav = tmp / f"{name}.wav"
    sf.write(wav, audio if audio is not None else ambient(sec, 0.0005), SR)
    w, h = size
    # moving box gives real motion; optional black head tests black-frame avoidance
    vf = (f"[0:v]scale={w}:{h},format=yuv420p[bg];"
          f"[2:v]scale=240:240[mv];"
          f"[bg][mv]overlay=x='(W-240)*(0.5+0.4*sin(t*1.7))':y='H*0.72'[o]")
    if black_head:
        vf += f";[o]fade=t=in:st={black_head}:d=0.01[v]"
    else:
        vf += ";[o]null[v]"
    subprocess.run([
        "ffmpeg", "-y", "-v", "error",
        "-loop", "1", "-framerate", "30", "-t", str(sec), "-i", str(png),
        "-i", str(wav),
        "-f", "lavfi", "-t", str(sec), "-i", "testsrc2=size=240x240:rate=30",
        "-filter_complex", vf, "-map", "[v]", "-map", "1:a",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-r", "30",
        "-c:a", "aac", "-b:a", "192k", "-shortest",
        str(PROJECT / "clips" / f"{name}.mp4"),
    ], check=True)


def music_track(path: Path, sec: float = 30.0, bpm: int = 120) -> None:
    t = np.arange(int(sec * SR)) / SR
    y = np.zeros_like(t, dtype=np.float32)
    beat = 60 / bpm
    drop = 8.0
    for i, bt in enumerate(np.arange(0, sec, beat)):
        s = int(bt * SR)
        n = int(0.18 * SR)
        k = np.sin(2 * np.pi * 55 * np.arange(n) / SR) * np.exp(-np.arange(n) / (0.05 * SR))
        y[s:s + n] += (0.5 if bt < drop else 0.9) * k[: len(y) - s].astype(np.float32)
        hs = int((bt + beat / 2) * SR)
        hn = int(0.04 * SR)
        if hs + hn < len(y):
            y[hs:hs + hn] += (np.random.default_rng(i).normal(0, 0.05, hn) * np.hanning(hn)).astype(np.float32)
    pad = 0.06 * (np.sin(2 * np.pi * 220 * t) + np.sin(2 * np.pi * 277 * t) + np.sin(2 * np.pi * 330 * t))
    bass = np.where(t >= drop, 0.12 * np.sin(2 * np.pi * 110 * t), 0.0)
    y += (pad + bass).astype(np.float32)
    y /= np.max(np.abs(y)) * 1.1
    sf.write(path, np.stack([y, y], axis=1), SR)


def main() -> None:
    if PROJECT.exists():
        shutil.rmtree(PROJECT)
    for sub in ("clips", "frames", "refs", "edit", "out"):
        (PROJECT / sub).mkdir(parents=True)
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        voice = speech_track(8.0, tmp)
        make_clip("c01_a", "C01 TAKE A\nDIALOGUE", "#3a5a8c", voice, tmp=tmp)
        make_clip("c01_b", "C01 TAKE B\nWRONG RATIO", "#8c3a3a", voice, size=(1080, 1080), tmp=tmp)
        make_clip("c02_a", "C02\nPERSONALIZE SFX", "#2f7d4f", sfx_track(8.0), tmp=tmp)
        make_clip("c03_a", "C03 TAKE A\nBLACK HEAD", "#6a3a8c", sfx_track(8.0), black_head=2.0, tmp=tmp)
        make_clip("c03_b", "C03 TAKE B\nLIFESTYLE", "#8c6a3a", sfx_track(8.0), tmp=tmp)

    music = MUSIC_LIBRARY / "test-beat-120.wav"
    music_track(music)

    save_json(PROJECT / "product.json", {
        "schema_version": "1.0", "product_id": "demo-hoodie", "name": "Custom Name Hoodie",
        "model": "pod_custom", "reference_images": [], "design_files": [],
        "invariants": ["Tên in ở ngực trái, chữ trắng"],
        "facts": [{"key": "personalization", "value": "In tên theo yêu cầu", "source": "user"}],
        "inferred": [{"key": "persona", "value": "Người mua làm quà cho bạn trai"}],
        "unknown": ["chất liệu", "giá", "thời gian ship"],
        "claims": [{"text": "Any name, any color", "evidence": "personalization"}],
    })
    save_json(PROJECT / "production.json", {
        "schema_version": "1.0",
        "project_id": "demo-hoodie",
        "product_ref": "product.json",
        "platform": "tiktok_reels",
        "stage": "clips_ready",
        "gen_model": {"image": "nano-banana", "video": "veo-3"},
        "spec": {"ratio": "9:16", "resolution": "1080x1920", "fps": 30, "target_sec": 15,
                 "safe_zone": {"top": 0.15, "bottom": 0.20}},
        "audio": {"source": "native", "music_duck_db": -12, "target_lufs": -14,
                  "true_peak_db": -1, "export_no_music": True},
        "music": {"source": "file", "file": "music-library/test-beat-120.wav"},
        "captions": {"enabled": True, "style": "word-highlight"},
        "shots": [
            {"id": "s01", "role": "hook", "file_pattern": "c01*.mp4", "use_sec": 2.5,
             "audio_type": "dialogue", "dialogue": "Wait, you can put his name on it?",
             "overlay": "Gift idea he'll actually wear", "overlay_pos": "lower"},
            {"id": "s02", "role": "personalize", "file_pattern": "c02*.mp4", "use_sec": 3,
             "audio_type": "sfx", "overlay": "Any name · any color", "overlay_pos": "lower",
             "print_fidelity": "strict"},
            {"id": "s03", "role": "demo", "file_pattern": "c01*.mp4", "use_sec": 1.8,
             "audio_type": "dialogue", "dialogue": "Any name, any color."},
            {"id": "s04", "role": "lifestyle", "file_pattern": "c03*.mp4", "use_sec": 3,
             "audio_type": "music_only", "overlay": None},
            {"id": "s05", "role": "cta", "file_pattern": "c01*.mp4", "use_sec": 2.5,
             "audio_type": "dialogue", "dialogue": "The link is right below.",
             "overlay": "Personalize yours ↓"},
        ],
    })
    print(f"Fixtures ready: {PROJECT}")


if __name__ == "__main__":
    main()
