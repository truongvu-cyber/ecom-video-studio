"""The user's taste, in their own words: every verdict is written down and read before the next job.

Usage:
  taste.py add --about edit|music|hook|script|product|model|scene|style|process
               --verdict approved|rejected|change|preference
               --quote "<nguyên văn lời người dùng>" [--lesson "<điều rút ra>"]
               [--project <id>] [--style <name>] [--date YYYY-MM-DD]
               [--metrics views=12000,watch_through=0.31]
  taste.py show [--about <topic>] [--style <name>]

taste/log.jsonl is local (not in git). Rules: the quote is what the user wrote, never a paraphrase;
the lesson is the agent's reading and says so; one entry per verdict; nothing is edited afterwards
(a changed mind is a new entry). Both agents run `taste.py show` before a concept or a cut.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import date

import os
from pathlib import Path

from common import ROOT

LOG = Path(os.environ.get("TASTE_LOG") or ROOT / "taste" / "log.jsonl")  # TASTE_LOG: tests only
ABOUT = ["edit", "music", "hook", "script", "product", "model", "scene", "style", "process"]
VERDICTS = ["approved", "rejected", "change", "preference"]


def entries() -> list[dict]:
    if not LOG.exists():
        return []
    return [json.loads(l) for l in LOG.read_text(encoding="utf-8").splitlines() if l.strip()]


def add(e: dict) -> None:
    LOG.parent.mkdir(exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps({k: v for k, v in e.items() if v not in (None, "", {})}, ensure_ascii=False) + "\n")


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("--about", required=True, choices=ABOUT)
    a.add_argument("--verdict", required=True, choices=VERDICTS)
    a.add_argument("--quote", required=True)
    a.add_argument("--lesson", default="")
    a.add_argument("--project", default="")
    a.add_argument("--style", default="")
    a.add_argument("--date", default=date.today().isoformat())
    a.add_argument("--metrics", default="")
    s = sub.add_parser("show")
    s.add_argument("--about", choices=ABOUT)
    s.add_argument("--style")
    args = ap.parse_args()

    if args.cmd == "add":
        metrics = {k: float(v) for k, v in (p.split("=") for p in args.metrics.split(",") if "=" in p)}
        add({"date": args.date, "about": args.about, "verdict": args.verdict, "quote": args.quote.strip(),
             "lesson": args.lesson.strip(), "project": args.project, "style": args.style, "metrics": metrics})
        print(f"đã ghi: [{args.about}/{args.verdict}] {args.quote[:70]}")
        return

    rows = [e for e in entries() if (not args.about or e["about"] == args.about)
            and (not args.style or e.get("style") == args.style)]
    if not rows:
        print("Sổ gu chưa có mục nào khớp.")
        return
    by = defaultdict(list)
    for e in rows:
        by[e["about"]].append(e)
    for topic in ABOUT:
        if topic not in by:
            continue
        print(f"\n== {topic} ({len(by[topic])})")
        for e in sorted(by[topic], key=lambda x: x["date"], reverse=True):
            tag = " · ".join(x for x in (e.get("project"), e.get("style")) if x)
            print(f"- {e['date']} [{e['verdict']}] \"{e['quote']}\"" + (f"  ({tag})" if tag else ""))
            if e.get("lesson"):
                print(f"    → {e['lesson']}")
            if e.get("metrics"):
                print(f"    số liệu: {e['metrics']}")
    styles = defaultdict(lambda: defaultdict(int))
    for e in entries():
        if e.get("style"):
            styles[e["style"]][e["verdict"]] += 1
    if styles and not args.about:
        print("\n== theo phong cách")
        for name, c in sorted(styles.items()):
            print(f"- {name}: " + ", ".join(f"{k} {v}" for k, v in sorted(c.items())))


if __name__ == "__main__":
    main()
