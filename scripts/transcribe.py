"""Word-level transcripts for the chosen dialogue takes (mlx-whisper, offline on Apple Silicon).

Usage: transcribe.py <project> [--model mlx-community/whisper-large-v3-turbo]
Writes edit/transcripts/<take>.json; cached by file size + mtime.
"""
from __future__ import annotations

import argparse

from common import load_json, project_dir, run, save_json

DEFAULT_MODEL = "mlx-community/whisper-large-v3-turbo"
MAX_WORD = 0.7


def refine_onsets(src, words: list[dict]) -> None:
    """Move the start of a word that follows silence to where the voice actually begins.

    Whisper's word starts after a pause are often hundreds of ms early; a hook that opens
    on half a second of silence loses viewers, and a cut placed there is not 'tight'.
    """
    import librosa
    import numpy as np

    raw = run(["ffmpeg", "-v", "error", "-i", str(src), "-vn", "-ac", "1", "-ar", "16000",
               "-f", "s16le", "-"], text=False).stdout
    y = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768
    hop = 160  # 10ms
    rms = librosa.feature.rms(y=y, frame_length=400, hop_length=hop)[0]
    if not rms.size:
        return
    thresh = 0.15 * float(np.percentile(rms, 95))
    prev_end = 0.0
    for i, w in enumerate(words):
        if i == 0 or w["start"] - prev_end > 0.25:
            a, b = int(w["start"] * 100), int(w["end"] * 100)
            loud = np.nonzero(rms[a:b] > thresh)[0]
            if loud.size:
                w["start"] = round(max(w["start"], (a + loud[0]) / 100 - 0.03), 3)
        prev_end = w["end"]


def word_list(res: dict, src) -> list[dict]:
    """mlx-whisper result -> clean word timings (also used by analyze_ref.py)."""
    # whisper stretches a word over the silence before it (typically the first word
    # starts at 0.0); no spoken word lasts longer than MAX_WORD, so pull the start in
    words = [{"w": w["word"].strip(),
              "start": round(max(w["start"], w["end"] - MAX_WORD), 3), "end": round(w["end"], 3),
              "p": round(w.get("probability", 1.0), 3)}
             for seg in res["segments"] for w in seg.get("words", [])]
    refine_onsets(src, words)
    return words


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    args = ap.parse_args()

    project = project_dir(args.project)
    prod = load_json(project / "production.json")
    media = load_json(project / "edit" / "media.json")

    takes = sorted({media["chosen"][s["file_pattern"]] for s in prod["shots"]
                    if s["audio_type"] == "dialogue" and s["file_pattern"] in media["chosen"]})
    if not takes:
        print("Không có cảnh thoại, bỏ qua chép lời")
        return

    import mlx_whisper  # heavy import, only when needed

    for take in takes:
        src = project / "clips" / take
        out = project / "edit" / "transcripts" / f"{src.stem}.json"
        stamp = f"{src.stat().st_size}:{int(src.stat().st_mtime)}:{args.model}:w{MAX_WORD}:onset1"
        if out.exists() and load_json(out).get("stamp") == stamp:
            print(f"{take}: dùng cache")
            continue
        res = mlx_whisper.transcribe(str(src), path_or_hf_repo=args.model,
                                     word_timestamps=True, language="en", verbose=None)
        # whisper stretches a word over the silence before it (typically the first word
        # starts at 0.0); no spoken word lasts longer than MAX_WORD, so pull the start in
        words = word_list(res, src)
        save_json(out, {"take": take, "stamp": stamp, "text": res["text"].strip(), "words": words})
        print(f"{take}: {len(words)} từ — {res['text'].strip()}")


if __name__ == "__main__":
    main()
