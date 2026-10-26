"""Mark a project approved once the user says so.

Usage: approve.py <project>
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
    prod["stage"] = "approved"
    save_json(project / "production.json", prod)
    report = project / "out" / "edit-report.md"
    if report.exists():
        report.write_text(report.read_text(encoding="utf-8").rstrip() +
                          f"\n\n**Đã duyệt** ngày {date.today().isoformat()} (QC {verdict}).\n", encoding="utf-8")
    print(f"{prod['project_id']}: approved (QC {verdict})")


if __name__ == "__main__":
    main()
