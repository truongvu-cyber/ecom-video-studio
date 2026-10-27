"""Copy a project's plan into a new project folder with a different set of clips.

Usage: clone_project.py <src-project> <new-id> [--clips c01=clips/c01_c.mp4,c02=clips/c02_b.mp4,...]
Copies product.json, production.json, brief.md, prompts.md, frames/ and the music choice;
the clips named by --clips are copied in as cNN_a.mp4 (the rest of clips/ is not copied).
Used to cut the same plan from a different generation (e.g. Omni vs Veo) without touching
an approved project.
"""
from __future__ import annotations

import argparse
import shutil

from common import ROOT, load_json, project_dir, save_json


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("new_id")
    ap.add_argument("--clips", default="", help="cNN=<path relative to src project>, comma separated")
    args = ap.parse_args()
    src = project_dir(args.src)
    dst = ROOT / "projects" / args.new_id
    if dst.exists():
        raise SystemExit(f"{dst} đã tồn tại")
    for sub in ("refs", "frames", "clips", "edit", "out"):
        (dst / sub).mkdir(parents=True)
    for f in ("product.json", "brief.md", "prompts.md"):
        if (src / f).exists():
            shutil.copy(src / f, dst / f)
    for f in (src / "frames").iterdir():
        if f.is_file():
            shutil.copy(f, dst / "frames" / f.name)
    prod = load_json(src / "production.json")
    prod["project_id"] = args.new_id
    prod["stage"] = "clips_ready"
    for s in prod["shots"]:
        s.pop("chosen_take", None)
        s["status"] = "pending"
    save_json(dst / "production.json", prod)
    for pair in filter(None, args.clips.split(",")):
        cid, rel = pair.split("=")
        shutil.copy(src / rel, dst / "clips" / f"{cid}_a.mp4")
        print(f"  {rel} -> clips/{cid}_a.mp4")
    print(f"-> projects/{args.new_id}")


if __name__ == "__main__":
    main()
