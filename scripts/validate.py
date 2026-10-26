"""Validate production.json (+ product.json) against the schemas and check referenced files.

Usage: validate.py <project> [--no-clips]
--no-clips: Creative stage, clips are not generated yet.
Exit 1 on any error so the agent stops before touching media.
"""
from __future__ import annotations

import argparse
import sys

from jsonschema import Draft202012Validator

from common import ROOT, SCHEMAS, inside, load_json, project_dir


def check(schema_name: str, data: dict) -> list[str]:
    schema = load_json(SCHEMAS / schema_name)
    v = Draft202012Validator(schema)
    return [f"{schema_name}: {'/'.join(map(str, e.path)) or '(root)'}: {e.message}"
            for e in sorted(v.iter_errors(data), key=lambda e: list(e.path))]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--no-clips", action="store_true")
    args = ap.parse_args()
    project = project_dir(args.project)
    prod = load_json(project / "production.json")
    errors = check("production.schema.json", prod)

    product_path = inside(project, prod.get("product_ref", "product.json"))
    if product_path.exists():
        errors += check("product.schema.json", load_json(product_path))
        product = load_json(product_path)
        blocked = [c["text"] for c in product.get("claims", []) if not c.get("evidence")]
        if blocked:
            errors.append(f"product.json: claim chưa có bằng chứng, không được dùng: {blocked}")
    else:
        errors.append(f"Thiếu {product_path.name}")

    ids = [s["id"] for s in prod.get("shots", [])]
    if len(ids) != len(set(ids)):
        errors.append("shots: trùng id")
    for s in prod.get("shots", []):
        if s.get("audio_type") == "dialogue" and not s.get("dialogue"):
            errors.append(f"{s['id']}: audio_type=dialogue nhưng thiếu dialogue")
        if not args.no_clips and not list((project / "clips").glob(s.get("file_pattern", "__none__"))):
            errors.append(f"{s['id']}: không có clip khớp clips/{s.get('file_pattern')}")
        ov = s.get("override") or {}
        if "src_in" in ov and "src_out" in ov and ov["src_out"] <= ov["src_in"]:
            errors.append(f"{s['id']}: override.src_out phải lớn hơn src_in")

    music = prod.get("music", {})
    if music.get("source") == "file":
        f = music.get("file")
        if not f or not ((ROOT / f).exists() or (project / f).exists()):
            errors.append(f"music.file không tồn tại: {f}")

    if errors:
        print("INVALID")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    print(f"OK: {len(ids)} shots, schema {prod['schema_version']}")


if __name__ == "__main__":
    main()
