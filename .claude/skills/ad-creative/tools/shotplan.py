#!/usr/bin/env python3
"""
shotplan.py - turn a short-video script into a clip plan that a video model can
actually generate.

Video models generate fixed lengths (Kling 2.x: 5 or 10 s, Veo: 4/6/8 s, and so
on). A script is timed by words: one line per beat (voiceover, dialogue or
on-screen text), first line = hook, last line = CTA. This script lines the two up: every
spoken beat becomes a clip, each clip gets the shortest length the model can
generate that still covers the beat, and long beats are split. On multi-shot
models (--multishot) consecutive beats are grouped into one generation with up
to the model's shot limit.

It prints the plan, how many seconds you will generate versus use (credits
spent on footage you trim away), and with --skeleton writes a Markdown file of
clip headers ready for the prompts.

Usage
  python3 shotplan.py script.txt --model kling --target 30   (default model: generic)
  python3 shotplan.py script.txt --model kling3 --multishot
  python3 shotplan.py --beats-json beats.json --model veo   (JSON from another tool:
      {"beats": [{"n", "start", "dur", "words", "text", "label"}], "target"})
  python3 shotplan.py script.txt --model veo --skeleton prompts.md
  python3 shotplan.py script.txt --model seedance --json

Models: keys of models.json (kling, kling3, veo, sora, seedance, seedance2,
hailuo, runway, luma, wan, generic). Standard library only.
"""

import argparse
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WORDS_PER_SECOND = 2.5  # conservative fit for clean lip-sync; prompt_lint uses the same rate


def load_models():
    with open(os.path.join(HERE, "models.json"), encoding="utf-8") as fh:
        data = json.load(fh)
    data.pop("_note", None)
    return {k: v for k, v in data.items() if v.get("kind", "video") == "video"}


WORD_RE = re.compile(r"[\w$%'’-]+")
MIN_BEAT = 1.2  # seconds; even a two-word line needs room on screen


def time_lines(raw, wpm):
    """One spoken or on-screen line per text line -> timed beats."""
    lines = [ln.strip() for ln in raw.splitlines()]
    lines = [ln for ln in lines if ln and not ln.startswith("#")]
    wps = wpm / 60.0
    beats, t = [], 0.0
    for n, ln in enumerate(lines, 1):
        words = len(WORD_RE.findall(ln))
        dur = round(max(MIN_BEAT, words / wps), 2)
        label = "HOOK" if n == 1 else ("CTA" if n == len(lines) and len(lines) > 1 else "")
        beats.append({"n": n, "start": round(t, 2), "dur": dur, "words": words, "text": ln, "label": label})
        t += dur
    return beats


def load_beats(args):
    if args.beats_json:
        with open(args.beats_json, encoding="utf-8") as fh:
            data = json.load(fh)
        return data["beats"], data.get("target")
    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    if "BEAT SHEET" in raw and "====" in raw:
        sys.exit("This looks like a printed beat sheet. Pass the script itself (one line per beat), "
                 "or a JSON beat sheet with --beats-json.")
    beats = time_lines(raw, args.wpm)
    if not beats:
        sys.exit("The script is empty. Give one spoken or on-screen line per line.")
    return beats, None


def fit(seconds, durations):
    """Shortest allowed duration that covers `seconds`, else the longest."""
    for d in sorted(durations):
        if d >= seconds - 0.05:
            return d
    return max(durations)


def purpose(label, index, total):
    if label == "HOOK" or index == 0:
        return "Hook"
    if label == "CTA" or index == total - 1:
        return "CTA / end"
    return "Build / proof"


def plan_single(beats, model):
    durations = model["durations"]
    longest = max(durations)
    clips = []
    for i, b in enumerate(beats):
        pieces = max(1, math.ceil(b["dur"] / longest - 1e-9))
        part = b["dur"] / pieces
        for p in range(pieces):
            start = b["start"] + p * part
            clips.append({
                "beats": [b["n"]],
                "start": round(start, 2),
                "use": round(part, 2),
                "generate": fit(part, durations),
                "shots": 1,
                "purpose": purpose(b.get("label", ""), i, len(beats)),
                "text": b["text"] if pieces == 1 else f"{b['text']} (part {p + 1}/{pieces})",
                "words": b["words"] if pieces == 1 else math.ceil(b["words"] / pieces),
            })
    return clips


def plan_multi(beats, model):
    durations = model["durations"]
    longest = max(durations)
    limit = model.get("max_shots", 1)
    clips, group = [], []

    def close():
        if not group:
            return
        use = sum(b["dur"] for b in group)
        first = beats.index(group[0])
        labels = [b.get("label", "") for b in group]
        last = beats.index(group[-1]) == len(beats) - 1
        clips.append({
            "beats": [b["n"] for b in group],
            "start": round(group[0]["start"], 2),
            "use": round(use, 2),
            "generate": fit(use, durations),
            "shots": len(group),
            "purpose": "CTA / end" if ("CTA" in labels or last) and first != 0 else purpose(labels[0], first, len(beats)),
            "text": " / ".join(b["text"] for b in group),
            "words": sum(b["words"] for b in group),
        })
        group.clear()

    for i, b in enumerate(beats):
        # The hook gets its own generation so its first frame can be chosen on purpose.
        if i == 1:
            close()
        if group and (sum(x["dur"] for x in group) + b["dur"] > longest or len(group) >= limit):
            close()
        if b["dur"] > longest:
            close()
            for c in plan_single([b], model):
                c["purpose"] = purpose(b.get("label", ""), i, len(beats))
                clips.append(c)
            continue
        group.append(b)
    close()
    return clips


def tc(s):
    return f"{int(s // 60)}:{s % 60:04.1f}"


def notes_for(clips, model, target):
    notes = []
    used = sum(c["use"] for c in clips)
    gen = sum(c["generate"] for c in clips)
    if gen > 0 and used / gen < 0.6:
        notes.append(
            f"You generate {gen:.0f}s to use {used:.1f}s ({used / gen:.0%}). Merge short beats, "
            "or use a model with shorter or flexible durations, to waste fewer credits.")
    if target:
        if used < target - 3:
            notes.append(f"Spoken length {used:.1f}s is under the {target:.0f}s target. Add a beat, hold the product shot longer, or ship it short.")
        elif used > target + 3:
            notes.append(f"Spoken length {used:.1f}s is over the {target:.0f}s target. Cut a beat before generating anything.")
    for k, c in enumerate(clips, 1):
        if model.get("audio") and c["words"] > WORDS_PER_SECOND * c["generate"] + 1:
            notes.append(f"Clip {k}: {c['words']} spoken words do not fit {c['generate']}s of native audio. Shorten the line or move it to voiceover.")
    if not model.get("audio"):
        notes.append(f"{model['label']} makes no speech: record or generate the voiceover separately and lay it over the clips.")
    if clips and clips[0]["use"] > 3.2:
        notes.append("The hook runs past 3s. Show the product working or the problem visible inside the first second of clip 1.")
    return notes


def render(clips, model, notes, out=sys.stdout):
    w = out.write
    w(f"\nCLIP PLAN  ·  {model['label']}  ·  lengths {', '.join(str(d) for d in model['durations'])}s\n")
    w("=" * 78 + "\n")
    w(f"{'clip':<5}{'time':<15}{'gen':>5}{'use':>7}  {'purpose':<14}spoken\n")
    for k, c in enumerate(clips, 1):
        span = f"{tc(c['start'])}-{tc(c['start'] + c['use'])}"
        shots = f" [{c['shots']} shots]" if c["shots"] > 1 else ""
        text = c["text"] if len(c["text"]) <= 60 else c["text"][:57] + "..."
        w(f"{k:<5}{span:<15}{c['generate']:>4}s{c['use']:>6.1f}s  {c['purpose']:<14}{text}{shots}\n")
    w("-" * 78 + "\n")
    w(f"generate {sum(c['generate'] for c in clips):.0f}s  ·  use {sum(c['use'] for c in clips):.1f}s  ·  {len(clips)} generations\n")
    for n in notes:
        w(f"  - {n}\n")
    w("\nTrim each clip to its 'use' length in the edit. Pick the action and camera\n"
      "move for each clip yourself; this only sets the timing.\n")


def skeleton(clips, model, path):
    lines = [f"<!-- clip plan from shotplan.py for {model['label']} -->", ""]
    for k, c in enumerate(clips, 1):
        lines += [
            f"## Clip {k} · {c['generate']}s · {c['purpose']}",
            f"**Covers:** {tc(c['start'])}-{tc(c['start'] + c['use'])} (use {c['use']:.1f}s) · "
            f"**Reference:** <...> · **First frame:** {'new' if k == 1 else f'last frame of clip {k - 1}'}",
            f"**Spoken:** {c['text']}",
            "```",
            "<prompt: shot + angle, camera move. [CHARACTER/PRODUCT lock]. one action. setting. light. [STYLE lock]. audio>",
            "```",
            "**Negative:** `<...>`",
            "",
        ]
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("input", nargs="?", default="-", help="script file, or - for stdin")
    ap.add_argument("--beats-json", help="JSON beat sheet instead of a script (e.g. from a Reel-script tool)")
    ap.add_argument("--model", default="generic", help="key in models.json (default generic)")
    ap.add_argument("--multishot", action="store_true", help="group beats into multi-shot generations")
    ap.add_argument("--target", type=float, help="target length in seconds")
    ap.add_argument("--wpm", type=float, default=165, help="speaking rate for scripts (default 165)")
    ap.add_argument("--skeleton", help="write Markdown clip headers to this file")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    models = load_models()
    if args.model not in models:
        sys.exit(f"Unknown model '{args.model}'. Choose from: {', '.join(models)}")
    model = models[args.model]
    beats, target = load_beats(args)
    target = args.target or target
    if not beats:
        sys.exit("No beats found. Give one spoken line per line of the script.")

    if args.multishot and not model.get("multishot"):
        print(f"note: {model['label']} has no multi-shot; planning one beat per clip.", file=sys.stderr)
    clips = plan_multi(beats, model) if args.multishot and model.get("multishot") else plan_single(beats, model)
    notes = notes_for(clips, model, target)

    if args.skeleton:
        skeleton(clips, model, args.skeleton)
    if args.json:
        json.dump({"model": args.model, "clips": clips, "notes": notes}, sys.stdout, indent=2)
        print()
    else:
        render(clips, model, notes)
        if args.skeleton:
            print(f"Wrote clip headers to {args.skeleton}")


if __name__ == "__main__":
    main()
