"""Shared helpers for the ad-editor pipeline.

Every script takes a project directory (projects/<id>) and reads/writes inside it only.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMAS = ROOT / "schemas"
MUSIC_LIBRARY = ROOT / "music-library"
BRAND = ROOT / "brand"
HYPERFRAMES = "hyperframes@0.8.186"


def project_dir(arg: str, need_production: bool = True) -> Path:
    p = Path(arg).expanduser()
    if not p.is_absolute():
        candidate = ROOT / "projects" / arg
        p = candidate if candidate.exists() else (Path.cwd() / p)
    p = p.resolve()
    if not p.is_dir():
        sys.exit(f"Không thấy project {p}")
    if need_production and not (p / "production.json").exists():
        sys.exit(f"Không thấy production.json trong {p}")
    return p


def inside(project: Path, rel: str) -> Path:
    """Resolve a project-relative path and refuse anything that escapes the project."""
    p = (project / rel).resolve()
    if project not in p.parents and p != project:
        sys.exit(f"Đường dẫn nằm ngoài project: {rel}")
    return p


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    kw.setdefault("text", True)
    res = subprocess.run(cmd, capture_output=True, **kw)
    if res.returncode != 0:
        err = res.stderr if kw["text"] else res.stderr.decode(errors="replace")
        tail = "\n".join(err.strip().splitlines()[-15:])
        raise RuntimeError(f"Lệnh lỗi ({cmd[0]}):\n{tail}")
    return res


def ffprobe(path: Path) -> dict:
    out = run(["ffprobe", "-v", "error", "-print_format", "json",
               "-show_format", "-show_streams", str(path)]).stdout
    return json.loads(out)


def media_info(path: Path) -> dict:
    data = ffprobe(path)
    v = next((s for s in data["streams"] if s["codec_type"] == "video"), None)
    a = next((s for s in data["streams"] if s["codec_type"] == "audio"), None)
    info = {"duration": float(data["format"].get("duration", 0.0)), "has_audio": a is not None}
    if v:
        num, den = (v.get("avg_frame_rate") or "0/1").split("/")
        info.update({
            "width": int(v["width"]), "height": int(v["height"]),
            "fps": round(float(num) / float(den), 3) if float(den) else 0.0,
            "vcodec": v.get("codec_name"), "pix_fmt": v.get("pix_fmt"),
        })
    if a:
        info.update({"acodec": a.get("codec_name"), "sample_rate": int(a.get("sample_rate", 0))})
    return info


def loudness(path: Path) -> dict:
    """Integrated loudness / true peak via loudnorm's analysis pass."""
    res = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-vn",
                          "-af", "loudnorm=I=-14:TP=-1:LRA=11:print_format=json",
                          "-f", "null", "-"], capture_output=True, text=True)
    text = res.stderr
    start = text.rfind("{")
    if start < 0:
        return {"input_i": None, "input_tp": None}
    d = json.loads(text[start:text.rfind("}") + 1])
    def num(k):
        try:
            v = float(d[k])
            return None if v in (float("inf"), float("-inf")) else v
        except (KeyError, ValueError):
            return None
    return {"input_i": num("input_i"), "input_tp": num("input_tp"), "input_lra": num("input_lra"),
            "input_thresh": num("input_thresh"), "target_offset": num("target_offset")}


def ratio_of(w: int, h: int) -> str:
    from math import gcd
    g = gcd(w, h)
    return f"{w // g}:{h // g}"


def spec_size(prod: dict) -> tuple[int, int]:
    w, h = prod["spec"].get("resolution", "1080x1920").split("x")
    return int(w), int(h)
