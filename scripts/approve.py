"""Mark a project approved once the user says so.

Usage: approve.py <project> ["<lời duyệt nguyên văn của người dùng>"]
Refuses when the last QC verdict is REJECT or no render exists; records the
approval in production.json (stage) and in out/edit-report.md.
"""
from __future__ import annotations

import sys
from datetime import date

from common import load_json, project_dir, save_json


def main() -> None:
    project = project_dir(sys.argv[1])
    prod = load_json(project / "production.json")
    qc = project / "edit" / "qc" / "qc.json"
    if not qc.exists():
        sys.exit("Chưa có QC: chạy edit_pipeline.py trước")
    verdict = load_json(qc)["verdict"]
    if verdict == "REJECT":
        sys.exit("QC đang REJECT: sửa rồi render lại trước khi duyệt")
    final = project / "out" / f"final_{prod['project_id']}.mp4"
    if not final.exists():
        sys.exit("Không thấy out/final_*.mp4")
    missing = [v["id"] for v in prod.get("variants") or [] if v.get("overlay_overrides")
               and not (project / "out" / f"final_{prod['project_id']}_{v['id']}.mp4").exists()]
    if missing:
        sys.exit(f"Chưa xuất biến thể hook {missing}: chạy edit_pipeline.py <project> --from timeline --final")
    prod["stage"] = "approved"
    save_json(project / "production.json", prod)
    from taste import add as taste_add
    style = prod.get("style")
    taste_add({"date": date.today().isoformat(), "about": "style", "verdict": "approved",
               "quote": sys.argv[2] if len(sys.argv) > 2 else "(duyệt bằng approve.py, không kèm lời)",
               "project": prod["project_id"], "style": style[0] if isinstance(style, list) else style})
    report = project / "out" / "edit-report.md"
    if report.exists():
        report.write_text(report.read_text(encoding="utf-8").rstrip() +
                          f"\n\n**Đã duyệt** ngày {date.today().isoformat()} (QC {verdict}).\n", encoding="utf-8")
    print(f"{prod['project_id']}: approved (QC {verdict})")


if __name__ == "__main__":
    main()
