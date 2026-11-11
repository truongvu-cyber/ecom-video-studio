"""The edit-style library: recipes measured from reference videos and from our own approved cuts.

Usage:
  styles.py list                          every recipe: verdict, format, when to use it
  styles.py show <name>                   one recipe
  styles.py draft <project> refs/<file>   after analyze_ref.py: a draft recipe with the measured
                                          rhythm (shot lengths in beats), saved as styles/_draft-<stem>.json

A recipe (styles/<name>.json) records what makes a cut look the way it does: the rhythm in beats,
where each effect sits and why, the text voice, the character of the music, the pictures it needs.
A new project names its recipe(s) in production.json `style`; the numbers in the recipe (rhythm,
fx.max_effects) are copied into the plan, the pictures and words are new. A draft becomes a recipe
when the agent has filled every TODO from the reference's frames and the user has seen a cut made with it.
"""
from __future__ import annotations

import json
import sys

from common import ROOT, load_json, project_dir, save_json

DIR = ROOT / "styles"
REQUIRED = ["name", "summary", "source", "verdict", "use_when", "format", "music", "rhythm_beats", "effects", "text", "pictures"]


def recipes() -> list[dict]:
    out = []
    for f in sorted(DIR.glob("*.json")):
        d = load_json(f)
        d["_file"] = f.name
        d["_missing"] = [k for k in REQUIRED if k not in d] + (["TODO"] if "TODO" in json.dumps(d, ensure_ascii=False) else [])
        out.append(d)
    return out


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    if cmd == "list":
        for d in recipes():
            flag = f"  [THIẾU: {', '.join(d['_missing'])}]" if d["_missing"] else ""
            print(f"{d.get('name', d['_file']):22} {d.get('verdict', '?'):9} {d.get('format', '?'):13} {d.get('summary', '')}{flag}")
            for u in d.get("use_when", [])[:2]:
                print(f"{'':22} dùng khi: {u}")
        return
    if cmd == "show":
        f = DIR / f"{sys.argv[2]}.json"
        if not f.exists():
            sys.exit(f"Không có phong cách '{sys.argv[2]}': chạy styles.py list")
        print(f.read_text(encoding="utf-8"))
        return
    if cmd == "draft":
        project = project_dir(sys.argv[2], need_production=False)
        stem = sys.argv[3].rsplit("/", 1)[-1].rsplit(".", 1)[0]
        a = load_json(project / "refs" / stem / "analysis.json")
        bpm = a.get("music_bpm")
        beat = 60.0 / bpm if bpm else None
        lengths = [round(s["end"] - s["start"], 2) for s in a["scenes"]]
        draft = {
            "name": f"TODO-{stem}", "summary": "TODO một câu: phong cách này trông như thế nào",
            "source": {"project": project.name, "file": a["file"], "url": "TODO"},
            "verdict": "draft",
            "use_when": ["TODO"], "avoid_when": ["TODO"], "format": "TODO",
            "measured": {"duration_sec": a["duration"], "shots": a["scene_count"], "avg_shot_sec": a["avg_shot_sec"],
                         "speech_share": a["speech_share"], "bpm": bpm, "shot_sec": lengths},
            "music": {"bpm": [round(bpm - 8), round(bpm + 8)] if bpm else "TODO", "character": "TODO nghe/nhìn từ video mẫu", "drop": "TODO"},
            "rhythm_beats": [round(l / beat * 2) / 2 for l in lengths] if beat else "TODO (video mẫu không đo được BPM)",
            "effects": {"max_effects": "TODO", "where": [{"transition": "TODO", "on": "TODO", "why": "TODO"}]},
            "text": {"preset": "TODO", "rule": "TODO"},
            "pictures": ["TODO loại hình ảnh phong cách này cần"],
        }
        out = DIR / f"_draft-{stem}.json"
        save_json(out, draft)
        print(f"-> styles/{out.name}: nhịp đo được {draft['rhythm_beats']}. Điền các TODO từ sheet.jpg của video mẫu.")
        return
    sys.exit(__doc__)


if __name__ == "__main__":
    main()
