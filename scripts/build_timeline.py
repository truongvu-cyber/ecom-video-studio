"""production.json + chosen takes + transcripts + beats -> edit/edit-plan.json

Usage: build_timeline.py <project>

Cut priority (from the V3 plan): 1) never cut inside a spoken word,
2) keep the planned story order and rough length, 3) land cuts on a beat.
A beat is only taken when the move stays inside the silence/free footage around the cut.
Never freezes a frame: short non-dialogue footage may be slowed down to at most 15%,
anything worse is reported for a regenerate.
"""
from __future__ import annotations

import re
import sys
from difflib import SequenceMatcher

from common import load_json, project_dir, save_json, spec_size

PAD_IN = 0.12        # breath before the first word
PAD_OUT = 0.20       # tail after the last word
WORD_GUARD = 0.04    # never come closer than this to a neighbour word
BROLL_HEAD = 0.25    # skip the very first frames of a Veo clip
MIN_SHOT = 0.8
MAX_SLOWDOWN = 0.85  # speed factor floor for non-dialogue shots
SNAP_TOL = 0.045
MAX_MUSIC_DELAY = 3.0  # music may enter this late so its drop lands on the CTA


_ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
_TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def _num_words(n: int) -> list[str]:
    """0–999 as the words a script would spell them (whisper writes digits: "60" for "sixty")."""
    if n < 20:
        return [_ONES[n]]
    if n < 100:
        return [_TENS[n // 10]] + ([_ONES[n % 10]] if n % 10 else [])
    if n < 1000:
        return [_ONES[n // 100], "hundred"] + (_num_words(n % 100) if n % 100 else [])
    return [str(n)]


def norm(text: str) -> list[str]:
    out = []
    for t in re.findall(r"[a-z0-9']+", text.lower()):
        out += _num_words(int(t)) if t.isdigit() else [t]
    return out


def find_dialogue(words: list[dict], target: str, cursor: int) -> tuple[int, int, float]:
    tgt = " ".join(norm(target))
    n = max(1, len(norm(target)))
    best = (cursor, min(len(words), cursor + n) - 1, 0.0)
    for size in (n - 1, n, n + 1):
        if size < 1:
            continue
        for i in range(cursor, len(words) - size + 1):
            cand = " ".join(t for w in words[i:i + size] for t in norm(w["w"]))
            r = SequenceMatcher(None, cand, tgt).ratio()
            if r > best[2]:
                best = (i, i + size - 1, r)
    return best


def script_spelling(heard: list[dict], line: str) -> list[dict]:
    """Captions show the script's spelling where whisper misheard a word.

    Whisper writes names it does not know phonetically ("UEKR" for "Uecker"); the
    timing is right, the text is not. Swap in script words wherever the two word
    lists line up one-to-one.
    """
    script = line.split()
    a = [" ".join(norm(w["w"])) for w in heard]
    b = [" ".join(norm(w)) for w in script]
    out = [dict(w) for w in heard]
    for op, i1, i2, j1, j2 in SequenceMatcher(None, a, b).get_opcodes():
        if op == "replace" and i2 - i1 == j2 - j1:
            for k in range(i2 - i1):
                out[i1 + k]["w"] = script[j1 + k]
    return out


def dialogue_segment(shot: dict, words: list[dict], dur: float, cursor: int, issues: list[str]):
    i, j, score = find_dialogue(words, shot["dialogue"], cursor)
    if score < 0.6:
        issues.append(f"{shot['id']}: không tìm thấy câu thoại trong clip (khớp {score:.0%}) — kiểm tra lại take")
    elif score < 0.85:
        issues.append(f"{shot['id']}: lời trong clip lệch kịch bản (khớp {score:.0%})")
    w0, wn = words[i], words[j]
    prev_end = words[i - 1]["end"] if i > 0 else 0.0
    next_start = words[j + 1]["start"] if j + 1 < len(words) else dur
    lo = max(0.0, prev_end + WORD_GUARD if i > 0 else 0.0)
    hi = min(dur, next_start - WORD_GUARD if j + 1 < len(words) else dur)
    src_in = max(lo, w0["start"] - PAD_IN)
    src_out = min(hi, wn["end"] + PAD_OUT)
    need = shot["use_sec"] - (src_out - src_in)
    if need > 0:  # stretch into silence only, tail first
        add = min(need, hi - src_out)
        src_out += add
        src_in = max(lo, src_in - (need - add))
    seg = {
        "src_in": src_in, "src_out": src_out, "speed": 1.0,
        "out_min": wn["end"] + 0.08, "out_max": hi,
        "words": script_spelling(words[i:j + 1], shot["dialogue"]),
        "match": round(score, 3),
    }
    return seg, j + 1


def broll_segment(shot: dict, take: dict, issues: list[str]) -> dict:
    dur = take["duration"]
    start = BROLL_HEAD
    for a, b in take.get("black", []):
        if a <= start < b or (a < start + 0.5 and b > start):
            start = b + 0.05
    end_limit = dur
    for a, b in take.get("black", []):
        if a > start:
            end_limit = min(end_limit, a)
    avail = end_limit - start
    use = shot["use_sec"]
    speed = 1.0
    if avail < use:
        factor = avail / use
        if factor >= MAX_SLOWDOWN:
            speed = factor
            issues.append(f"{shot['id']}: clip thiếu {use - avail:.2f}s, làm chậm còn {factor:.0%}")
        else:
            issues.append(f"{shot['id']}: clip chỉ còn {avail:.2f}s dùng được (cần {use}s) — rút ngắn cảnh, nên gen lại")
            use = avail
    src_out = start + min(use * speed, avail)
    return {"src_in": start, "src_out": src_out, "speed": speed,
            "out_min": start + MIN_SHOT * speed, "out_max": end_limit, "words": []}


def moment_start(moments: dict, take: str, shot: dict, speed: float, issues: list[str]) -> float | None:
    """Start time for shot.moment from edit/moments.json (find_moments.py)."""
    m = moments.get(take)
    if not m:
        issues.append(f"{shot['id']}: moment='{shot['moment']}' nhưng chưa chạy find_moments.py cho {take}")
        return None
    key = str(round(float(shot["use_sec"]) * speed, 2))
    win = m["windows"].get(key) or next(iter(m["windows"].values()))
    return float(win[shot["moment"]])


BANDS = {  # normalised y-ranges the overlay styles occupy (see render.py CSS)
    "top": (0.17, 0.27), "center": (0.47, 0.57), "lower": (0.52, 0.61), "bottom": (0.70, 0.79),
}


def auto_overlay_pos(project, seg: dict, captions_on: bool, kind: str) -> str:
    """Pick the band of the frame with the least detail at the shot's middle frame.

    Edge density is a cheap stand-in for 'something important is here': faces,
    printed text, hands and products are edge-dense; sky, asphalt and walls are not.
    """
    import numpy as np

    from common import run as _run

    t = (seg["src_in"] + seg["src_out"]) / 2
    raw = _run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(project / "clips" / seg["take"]),
                "-frames:v", "1", "-vf", "scale=108:192,format=gray", "-f", "rawvideo", "-"], text=False).stdout
    if len(raw) < 108 * 192:
        return "top"
    img = np.frombuffer(raw[:108 * 192], dtype=np.uint8).reshape(192, 108).astype(np.float32)
    edges = np.abs(np.diff(img, axis=0))[:, :-1] + np.abs(np.diff(img, axis=1))[:-1, :]
    bands = dict(BANDS)
    if captions_on:
        bands["bottom"] = (0.62, 0.71)
    if kind == "cta":
        bands = {"top": bands["top"], "center": bands["center"], "bottom": bands["bottom"]}
    scores = {name: float(edges[int(a * 191):int(b * 191)].mean()) for name, (a, b) in bands.items()}
    order = ["top", "bottom", "lower", "center"]  # tie-break: least intrusive first
    best = min(order, key=lambda n: (round(scores.get(n, 9e9), 1), order.index(n)) if n in scores else (9e9, 9))
    return best


def layout(segments: list[dict]) -> float:
    t = 0.0
    for s in segments:
        s["tl_start"] = t
        t += (s["src_out"] - s["src_in"]) / s["speed"]
        s["tl_end"] = t
    return t


def snap_cuts(segments: list[dict], beats_tl: list[float], interval: float) -> None:
    for k, s in enumerate(segments):
        layout(segments)
        t = s["tl_end"]
        near = [b for b in beats_tl if abs(b - t) <= interval / 2]
        if not near:
            continue
        b = min(near, key=lambda x: abs(x - t))
        want = (b - t) * s["speed"]
        lo, hi = s["out_min"] - s["src_out"], s["out_max"] - s["src_out"]
        delta = min(max(want, lo), hi)
        if k == len(segments) - 1 and delta < 0 and want < 0:
            delta = 0.0  # ending: only ever extend, never trim the last line
        s["src_out"] += delta
    layout(segments)


def phrases(words: list[dict], seg: dict) -> list[dict]:
    out, cur = [], []
    for w in words:
        t0 = seg["tl_start"] + (w["start"] - seg["src_in"]) / seg["speed"]
        t1 = seg["tl_start"] + (w["end"] - seg["src_in"]) / seg["speed"]
        if cur and (len(cur) >= 3 or t0 - cur[-1]["end"] > 0.35):
            out.append(cur)
            cur = []
        cur.append({"w": w["w"], "start": round(t0, 3), "end": round(t1, 3)})
        if re.search(r"[.?!,]$", w["w"]):
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return [{"start": p[0]["start"], "end": p[-1]["end"], "words": p} for p in out]


def main() -> None:
    project = project_dir(sys.argv[1])
    prod = load_json(project / "production.json")
    media = load_json(project / "edit" / "media.json")
    music = load_json(project / "edit" / "music.json")
    issues: list[str] = []

    keep_native = prod["audio"].get("keep_native", True)
    mpath = project / "edit" / "moments.json"
    moments = load_json(mpath) if mpath.exists() else {}
    cursors: dict[str, int] = {}
    segments = []
    for shot in prod["shots"]:
        take_name = media["chosen"].get(shot["file_pattern"])
        if not take_name:
            sys.exit(f"{shot['id']}: chưa có take hợp lệ, chạy inspect_media.py trước")
        take = media["takes"][take_name]
        if shot["audio_type"] == "dialogue":
            tr_path = project / "edit" / "transcripts" / f"{take_name.rsplit('.', 1)[0]}.json"
            words = load_json(tr_path)["words"]
            seg, cursors[take_name] = dialogue_segment(shot, words, take["duration"],
                                                       cursors.get(take_name, 0), issues)
            if not keep_native:
                # voice is muted: the transcript still picks the right moment of the
                # clip, but the end is free to move to the beat
                seg["out_min"] = seg["src_in"] + MIN_SHOT
                seg["out_max"] = take["duration"]
        else:
            seg = broll_segment(shot, take, issues)
        if "speed" in shot and (shot["audio_type"] != "dialogue" or not keep_native):
            sp = float(shot["speed"])
            seg["speed"] = sp
            seg["src_out"] = min(take["duration"], seg["src_in"] + shot["use_sec"] * sp)
            seg["out_min"] = seg["src_in"] + MIN_SHOT * sp
            seg["out_max"] = take["duration"]
        if shot.get("moment") and not (shot.get("override") or {}).get("src_in"):
            start = moment_start(moments, take_name, shot, seg["speed"], issues)
            if start is not None:
                seg["src_in"] = start
                seg["src_out"] = min(take["duration"], start + shot["use_sec"] * seg["speed"])
                seg["out_min"] = start + MIN_SHOT * seg["speed"]
                seg["out_max"] = take["duration"]
                if shot["moment"] == "a" and moments[take_name]["split_reliable"]:
                    seg["out_max"] = max(seg["out_min"], min(take["duration"], moments[take_name]["split"] - 0.05))
        ov = shot.get("override") or {}
        if "src_out" in ov:
            seg["src_in"] = ov.get("src_in", seg["src_in"])
            seg["src_out"] = min(take["duration"], ov["src_out"])
            seg["out_min"] = seg["out_max"] = seg["src_out"]  # manual cut: do not snap
        elif "src_in" in ov:
            # manual start only: keep the planned length and still let the end find a beat
            seg["src_in"] = ov["src_in"]
            seg["src_out"] = min(take["duration"], ov["src_in"] + shot["use_sec"] * seg["speed"])
            seg["out_min"] = ov["src_in"] + MIN_SHOT * seg["speed"]
            seg["out_max"] = take["duration"]
            if take["duration"] - ov["src_in"] < shot["use_sec"]:
                issues.append(f"{shot['id']}: từ giây {ov['src_in']} clip chỉ còn {take['duration'] - ov['src_in']:.1f}s")
        seg.update({"shot": shot["id"], "role": shot["role"], "take": take_name,
                    "audio_type": shot["audio_type"], "overlay": shot.get("overlay"),
                    "overlay_pos": shot.get("overlay_pos", "top"),
                    "cta_pos": shot.get("overlay_pos"),  # CTA keeps its own spot unless set
                    "print_fidelity": shot.get("print_fidelity", "normal")})
        segments.append(seg)

    total = layout(segments)
    # music time m plays at timeline time  m - offset + delay  (delay = music enters late)
    offset, delay, cuts, beats_tl = 0.0, 0.0, [], []

    def align(cta_start: float) -> tuple[float, float]:
        drop = music.get("drop_sec")
        if drop is None or cta is None or prod["music"].get("drop_on") == "none":
            return 0.0, 0.0
        if drop >= cta_start:
            return drop - cta_start, 0.0
        if cta_start - drop <= MAX_MUSIC_DELAY:
            return 0.0, cta_start - drop
        return 0.0, 0.0

    if music.get("file"):
        beats = music["beats"]
        interval = 60.0 / music["bpm"]
        # the drop lands on the CTA by default, or on the shot named in music.drop_on
        drop_on = prod["music"].get("drop_on")
        cta = next((s for s in segments if s["shot"] == drop_on), None) if drop_on else None
        cta = cta or next((s for s in segments if s["role"] == "cta"), None)
        offset, delay = align(cta["tl_start"] if cta else 0.0)
        # snapping moves the drop shot, which moves the music, which moves every beat:
        # repeat until the grid stops shifting (once the drop shot sits on a beat the
        # realignment is a whole number of beats and earlier cuts stay on the beat)
        for _ in range(4):
            entry = [delay] if delay > 0 else []  # the music's entry is a cut point too
            snap_cuts(segments, entry + [b - offset + delay for b in beats if b - offset + delay > 0.2], interval)
            new_offset, new_delay = align(cta["tl_start"] if cta else 0.0)
            moved = abs(new_offset - offset) + abs(new_delay - delay)
            offset, delay = new_offset, new_delay
            if moved < 0.005:
                break
        total = segments[-1]["tl_end"]
        # a short track (e.g. a TikTok sound) must not end before the video does
        room = music["duration"] - offset + delay
        if total > room + 0.02:
            last = segments[-1]
            cut = min(total - room, (last["tl_end"] - last["tl_start"]) - MIN_SHOT)
            last["src_out"] -= cut * last["speed"]
            total = layout(segments)
            if total > room + 0.02:
                issues.append(f"Nhạc chỉ dài {room:.1f}s nhưng video dài {total:.1f}s")
        if prod["music"].get("drop_on") == "none":
            pass
        elif cta and music.get("drop_sec") is not None and offset == 0 and delay == 0 \
                and abs(music["drop_sec"] - cta["tl_start"]) > SNAP_TOL:
            issues.append(f"Không đặt được drop nhạc trùng cảnh {cta['shot']}")
        if offset + total - delay > music["duration"]:
            offset = max(0.0, music["duration"] - total + delay)
            issues.append("Nhạc ngắn hơn video tính từ đoạn drop: drop không trùng cảnh đã chọn")
        beats_tl = ([delay] if delay > 0 else []) + [b - offset + delay for b in beats]
        for s in segments[:-1]:
            if s["tl_end"] < delay - SNAP_TOL:
                cuts.append({"after": s["shot"], "at": round(s["tl_end"], 3), "beat": None,
                             "off_ms": None, "on_beat": None})
                continue
            b = min(beats_tl, key=lambda x: abs(x - s["tl_end"]))
            cuts.append({"after": s["shot"], "at": round(s["tl_end"], 3),
                         "beat": round(b, 3), "off_ms": round((s["tl_end"] - b) * 1000),
                         "on_beat": abs(s["tl_end"] - b) <= SNAP_TOL})

    for s in segments:
        if (s["src_out"] - s["src_in"]) / s["speed"] < MIN_SHOT:
            issues.append(f"{s['shot']}: cảnh chỉ dài {(s['src_out'] - s['src_in']):.2f}s, quá ngắn")

    captions = []
    if prod.get("captions", {}).get("enabled", True):
        for s in segments:
            if s["audio_type"] == "dialogue":
                captions += phrases(s["words"], s)
    overlays = []
    captions_on = bool(captions)
    for s in segments:
        if s["overlay"]:
            start = s["tl_start"] + 0.1
            kind = "cta" if s["role"] == "cta" else "headline"
            pos = s["cta_pos"] if kind == "cta" else s["overlay_pos"]
            if pos == "auto":
                pos = auto_overlay_pos(project, s, captions_on, kind)
                s["overlay_pos_auto"] = pos
            overlays.append({"shot": s["shot"], "text": s["overlay"], "kind": kind, "pos": pos,
                             "start": round(start, 3),
                             "end": round(max(start + 0.6, s["tl_end"] - 0.05), 3)})
    duck = []
    for s in segments if keep_native else []:
        if s["audio_type"] == "dialogue" and s["words"]:
            a = s["tl_start"] + (s["words"][0]["start"] - s["src_in"]) / s["speed"]
            b = s["tl_start"] + (s["words"][-1]["end"] - s["src_in"]) / s["speed"]
            if duck and a - duck[-1][1] < 0.4:
                duck[-1][1] = round(b, 3)
            else:
                duck.append([round(a, 3), round(b, 3)])

    target = prod["spec"]["target_sec"]
    if abs(total - target) > 2:
        issues.append(f"Tổng {total:.1f}s lệch mục tiêu {target}s")

    w, h = spec_size(prod)
    plan = {
        "project_id": prod["project_id"], "width": w, "height": h, "fps": prod["spec"]["fps"],
        "safe_zone": prod["spec"].get("safe_zone", {"top": 0.15, "bottom": 0.20}),
        "total_sec": round(total, 3),
        "audio": {**prod["audio"], "duck_regions": duck},
        "music": {"file": music.get("file"), "offset": round(offset, 3), "delay": round(delay, 3),
                  "bpm": music.get("bpm"), "drop_sec": music.get("drop_sec"),
                  "license": music.get("license")},
        "segments": [{k: (round(v, 3) if isinstance(v, float) else v) for k, v in s.items()
                      if k not in ("out_min", "out_max", "cta_pos")} for s in segments],
        "cuts": cuts, "captions": captions, "overlays": overlays, "issues": issues,
        "text_style": prod.get("text_style", {"preset": "pill"}),
        "fx": prod.get("fx", {"preset": "none"}),
        "beats_tl": [round(b, 3) for b in beats_tl if 0 <= b <= total],
        "variants": prod.get("variants", []),
    }
    save_json(project / "edit" / "edit-plan.json", plan)

    for s in plan["segments"]:
        extra = f" x{s['speed']}" if s["speed"] != 1.0 else ""
        extra += f" chữ→{s['overlay_pos_auto']}" if s.get("overlay_pos_auto") else ""
        print(f"{s['shot']} {s['take']:10} src {s['src_in']:5.2f}-{s['src_out']:5.2f} "
              f"tl {s['tl_start']:5.2f}-{s['tl_end']:5.2f} {s['audio_type']}{extra}")
    for c in cuts:
        if c["on_beat"] is None:
            print(f"cắt sau {c['after']} lúc {c['at']}s: trước khi nhạc vào")
        else:
            print(f"cắt sau {c['after']} lúc {c['at']}s: {'trúng beat' if c['on_beat'] else 'lệch'} {c['off_ms']}ms")
    print(f"Tổng {total:.2f}s, nhạc vào lúc {delay:.2f}s (phát từ giây {offset:.2f} của bài)")
    for i in issues:
        print("CHÚ Ý:", i)


if __name__ == "__main__":
    main()
