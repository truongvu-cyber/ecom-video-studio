"""edit/edit-plan.json -> out/final_<id>.mp4 (+ out/final_<id>_no-music.mp4)

Usage: render.py <project> [--quality draft|looks|delivery]

1. ffmpeg cuts every segment (frame-accurate, scaled to spec) and joins them -> edit/base.mp4 (silent)
2. ffmpeg builds the native-audio track: per-clip loudness matched, short fades at cuts,
   music_only shots muted; then music with ducking under speech; both loudnorm'ed to target
3. HyperFrames draws captions + overlays on top of base.mp4 -> edit/visual.mp4
4. visual.mp4 is muxed with each audio track
"""
from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import subprocess
from pathlib import Path

from common import BRAND, HYPERFRAMES, load_json, loudness, project_dir, run

SR = 48000
CLIP_TARGET_LUFS = {"dialogue": -18.0, "sfx": -24.0}
EDGE_FADE = 0.012
MUSIC_BED_DB = -6.0  # music level relative to its own loudness before ducking


def cut_segments(project: Path, plan: dict, work: Path) -> Path:
    w, h, fps = plan["width"], plan["height"], plan["fps"]
    parts = []
    for i, s in enumerate(plan["segments"]):
        src = project / "clips" / s["take"]
        dur = s["src_out"] - s["src_in"]
        vf = (f"trim=start={s['src_in']}:duration={dur},setpts=(PTS-STARTPTS)/{s['speed']},"
              f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},setsar=1,fps={fps}")
        out = work / f"seg{i:02d}.mp4"
        run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-an", "-vf", vf,
             "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", str(out)])
        parts.append(out)
    lst = work / "segments.txt"
    lst.write_text("".join(f"file '{p.name}'\n" for p in parts))
    base = work / "base.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
         "-c", "copy", str(base)])
    return base


def clip_gains(project: Path, plan: dict) -> dict[str, float]:
    gains = {}
    for s in plan["segments"]:
        kind = s["audio_type"]
        if kind == "music_only" or s["take"] + kind in gains:
            continue
        i = loudness(project / "clips" / s["take"])["input_i"]
        gains[s["take"] + kind] = 0.0 if i is None else max(-15.0, min(15.0, CLIP_TARGET_LUFS[kind] - i))
    return gains


def native_audio(project: Path, plan: dict, work: Path) -> Path:
    gains = clip_gains(project, plan)
    inputs, chains = [], []
    for i, s in enumerate(plan["segments"]):
        dur = (s["src_out"] - s["src_in"]) / s["speed"]
        inputs += ["-i", str(project / "clips" / s["take"])]
        if s["audio_type"] == "music_only" or not plan["audio"].get("keep_native", True):
            chains.append(f"anullsrc=r={SR}:cl=stereo,atrim=duration={dur}[a{i}]")
            continue
        g = gains[s["take"] + s["audio_type"]]
        tempo = f",atempo={s['speed']}" if s["speed"] != 1.0 else ""
        chains.append(
            f"[{i}:a]atrim=start={s['src_in']}:end={s['src_out']},asetpts=PTS-STARTPTS{tempo},"
            f"aresample={SR},aformat=channel_layouts=stereo,volume={g}dB,"
            f"afade=t=in:d={EDGE_FADE},afade=t=out:st={max(0, dur - EDGE_FADE)}:d={EDGE_FADE},"
            f"apad=whole_dur={dur}[a{i}]")
    n = len(plan["segments"])
    graph = ";".join(chains) + ";" + "".join(f"[a{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1[out]"
    out = work / "native.wav"
    run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", graph, "-map", "[out]",
         "-ar", str(SR), str(out)])
    return out


def duck_expr(regions: list[list[float]], duck_db: float, ramp: float = 0.15) -> str:
    if not regions:
        return "1"
    g = 10 ** (duck_db / 20)
    parts = [f"clip(min((t-{a - ramp})/{ramp},({b + ramp}-t)/{ramp}),0,1)" for a, b in regions]
    m = parts[0]
    for p in parts[1:]:
        m = f"max({m},{p})"
    return f"1-({1 - g})*{m}"


def music_track(plan: dict, work: Path) -> Path | None:
    m = plan["music"]
    if not m.get("file"):
        return None
    total = plan["total_sec"]
    play = total - m["delay"]
    level = loudness(Path(m["file"]))["input_i"] or -14.0
    bed = -14.0 + MUSIC_BED_DB - level
    expr = duck_expr(plan["audio"]["duck_regions"], plan["audio"].get("music_duck_db", -12))
    fade_in = 0.25 if m["delay"] > 0 or m["offset"] > 0 else 0.0
    af = (f"atrim=start={m['offset']}:duration={play},asetpts=PTS-STARTPTS,aresample={SR},"
          f"aformat=channel_layouts=stereo,volume={bed}dB,"
          + (f"afade=t=in:d={fade_in}," if fade_in else "")
          + f"afade=t=out:st={max(0, play - 0.8)}:d=0.8,"
          f"adelay={int(m['delay'] * 1000)}:all=1,apad=whole_dur={total},"
          f"volume='{expr}':eval=frame")
    out = work / "music.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", m["file"], "-af", af, "-t", str(total), str(out)])
    return out


def master(inputs: list[Path], plan: dict, out: Path) -> Path:
    a = plan["audio"]
    target, tp = a.get("target_lufs", -14), a.get("true_peak_db", -1)
    pre = out.with_suffix(".pre.wav")
    if len(inputs) == 1:
        shutil.copy(inputs[0], pre)
    else:
        args = sum((["-i", str(p)] for p in inputs), [])
        run(["ffmpeg", "-y", "-v", "error", *args, "-filter_complex",
             f"amix=inputs={len(inputs)}:normalize=0:duration=first[m]", "-map", "[m]", str(pre)])
    meas = loudness(pre)
    ln = f"loudnorm=I={target}:TP={tp}:LRA=11"
    if meas["input_i"] is not None:
        ln += (f":measured_I={meas['input_i']}:measured_TP={meas['input_tp']}"
               f":measured_LRA={meas['input_lra']}:measured_thresh={meas['input_thresh']}"
               f":offset={meas['target_offset']}:linear=true")
    # loudnorm alone lets peaks through on punchy tracks, and AAC adds ~0.5 dB on top
    # limit at 4x sample rate so inter-sample (true) peaks are caught too
    limit = 10 ** ((tp - 1.0) / 20)
    run(["ffmpeg", "-y", "-v", "error", "-i", str(pre), "-af",
         f"{ln},aresample={SR * 4},alimiter=limit={limit:.3f}:level=false:attack=1:release=50,"
         f"aresample={SR}", "-ar", str(SR), str(out)])
    pre.unlink()
    return out


def brand() -> dict:
    p = BRAND / "brand.json"
    return load_json(p) if p.exists() else {}


BOLD_CSS = """
@font-face {{ font-family: Impact; src: local('Impact'); }}
.headline span {{ background:none; padding:0 10px; display:inline-block; transform:rotate(-3deg);
  font-family:Impact,"Arial Black",sans-serif; font-weight:400; font-size:100px; line-height:1.0;
  letter-spacing:1px; text-transform:uppercase; color:{accent};
  -webkit-text-stroke:16px {stroke}; paint-order:stroke fill;
  text-shadow:0 12px 0 rgba(0,0,0,0.55), 0 0 40px rgba(0,0,0,0.45); }}
.headline span em, .cta span em {{ font-style:normal; color:{ink}; }}
.cta span {{ font-family:Impact,"Arial Black",sans-serif; font-weight:400; font-size:76px; letter-spacing:1px;
  text-transform:uppercase; background:{accent}; color:{stroke}; border:7px solid {stroke};
  box-shadow:0 12px 0 {stroke}; padding:18px 46px; display:inline-block; transform:rotate(-2deg); }}
"""


def hype_fx(plan: dict, k: float) -> tuple[list[str], str]:
    """Cut and beat effects drawn on the base video (HyperFrames/GSAP).

    Every cut: white flash, zoom punch from a motion blur, short decaying shake.
    Every other beat inside a shot: a small zoom pulse. The base video stays
    slightly overscaled (BASE) so shake never shows the frame edge.
    """
    BASE = 1.06
    cuts = [s["tl_start"] for s in plan["segments"][1:]]
    js = [f'gsap.set("#base",{{scale:{BASE},transformOrigin:"50% 45%"}});']
    for t in cuts:
        js.append(f'tl.fromTo("#flash",{{opacity:{min(0.85, 0.7 * k):.2f}}},'
                  f'{{opacity:0,duration:0.14,ease:"power2.out",immediateRender:false}},{t:.3f});')
        js.append(f'tl.fromTo("#base",{{scale:{BASE + 0.16 * k:.3f},filter:"blur({8 * k:.1f}px)"}},'
                  f'{{scale:{BASE},filter:"blur(0px)",duration:0.3,ease:"power3.out",immediateRender:false}},{t:.3f});')
        # deterministic shake: alternating offsets that decay over ~0.2 s
        for j, (dx, dy) in enumerate([(14, -10), (-12, 8), (9, -6), (-7, 5), (4, -3), (0, 0)]):
            js.append(f'tl.set("#base",{{x:{dx * k:.1f},y:{dy * k:.1f}}},{t + 0.035 * j:.3f});')
    for b in plan.get("beats_tl", []):
        if b < 0.2 or any(abs(b - t) < 0.15 for t in cuts):
            continue
        js.append(f'tl.fromTo("#base",{{scale:{BASE + 0.045 * k:.3f}}},'
                  f'{{scale:{BASE},duration:0.18,ease:"power2.out",immediateRender:false}},{b:.3f});')
    flash = (f'<div id="flash" class="clip" data-start="0" data-duration="{plan["total_sec"]}" '
             f'style="position:absolute;inset:0;background:#fff;opacity:0;pointer-events:none;"></div>')
    return js, flash


def composition(plan: dict, hf: Path) -> None:
    b = brand()
    colors = b.get("colors", {})
    accent = colors.get("accent", "#FFD60A")
    ink = colors.get("primary", "#FFFFFF")
    stroke = colors.get("text_stroke", "#000000")
    font = b.get("fonts", {}).get("caption", "Inter")
    style = plan.get("text_style") or {}
    bold = style.get("preset") == "bold"
    accent = style.get("color", accent)
    W, H, T = plan["width"], plan["height"], plan["total_sec"]
    top = int(H * plan["safe_zone"].get("top", 0.15))
    bottom = int(H * plan["safe_zone"].get("bottom", 0.20))

    els, js = [], []
    for k, o in enumerate(plan["overlays"]):
        if o["kind"] == "cta":
            cls = f"cta pos-{o['pos']}" if o.get("pos") else "cta"
        else:
            cls = f"headline pos-{o.get('pos', 'top')}"
        d = round(o["end"] - o["start"], 3)
        # *word* in an overlay is drawn in the second colour (white) for contrast
        text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", html.escape(o["text"]))
        els.append(f'<div id="ov{k}" class="clip {cls}" data-start="{o["start"]}" data-duration="{d}">'
                   f'<span>{text}</span></div>')
        if bold:
            js.append(f'tl.fromTo("#ov{k} span",{{opacity:0,scale:2.2,rotation:-9}},'
                      f'{{opacity:1,scale:1,rotation:-3,duration:0.26,ease:"back.out(2.4)"}},{o["start"]});')
            js.append(f'tl.to("#ov{k} span",{{x:7,duration:0.035,yoyo:true,repeat:5,ease:"none"}},{o["start"] + 0.26});')
        else:
            js.append(f'tl.fromTo("#ov{k} span",{{opacity:0,y:24,scale:0.96}},'
                      f'{{opacity:1,y:0,scale:1,duration:0.22,ease:"power3.out"}},{o["start"]});')
        if o["kind"] == "cta":
            js.append(f'tl.to("#ov{k} span",{{scale:1.06,duration:0.3,yoyo:true,repeat:3,ease:"sine.inOut"}},{o["start"] + 0.3});')
    for k, c in enumerate(plan["captions"]):
        d = round(c["end"] - c["start"] + 0.12, 3)
        words = "".join(f'<span id="cw{k}_{j}" class="w">{html.escape(w["w"])}</span> '
                        for j, w in enumerate(c["words"]))
        els.append(f'<div id="cap{k}" class="clip caption" data-start="{c["start"]}" data-duration="{d}">{words}</div>')
        js.append(f'tl.fromTo("#cap{k}",{{opacity:0,scale:0.9}},{{opacity:1,scale:1,duration:0.1,ease:"back.out(2)"}},{c["start"]});')
        for j, w in enumerate(c["words"]):
            js.append(f'tl.set("#cw{k}_{j}",{{color:"{accent}"}},{w["start"]});')
            js.append(f'tl.set("#cw{k}_{j}",{{color:"{ink}"}},{w["end"]});')

    fx = plan.get("fx") or {}
    if fx.get("preset") == "hype":
        js_fx, flash_el = hype_fx(plan, float(fx.get("intensity", 1)))
        els.insert(0, flash_el)
        js = js_fx + js  # effects first so text tweens stay on top
    page = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width={W}, height={H}" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:#000; }}
#root {{ position:relative; width:100%; height:100%; font-family:"{font}","Arial Black",Arial,sans-serif; }}
#base {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }}
.headline, .cta, .caption {{ position:absolute; left:60px; right:60px; display:flex; justify-content:center; text-align:center; }}
.headline.pos-top {{ top:{top + 40}px; }}
.headline.pos-center {{ top:{H // 2 - 60}px; }}
.headline.pos-lower {{ bottom:{bottom + 380}px; }}
.headline.pos-bottom {{ bottom:{bottom + (190 if plan["captions"] else 40)}px; }}
.headline span {{ background:rgba(0,0,0,0.55); color:{ink}; font-size:54px; font-weight:800; line-height:1.15; padding:16px 28px; border-radius:22px; }}
.cta {{ bottom:{bottom + 220}px; }}
.cta.pos-top {{ top:{top + 40}px; bottom:auto; }}
.cta.pos-center {{ top:{H // 2 - 60}px; bottom:auto; }}
.cta.pos-bottom {{ bottom:{bottom + 40}px; }}
.cta span {{ background:{accent}; color:#111; font-size:58px; font-weight:900; padding:22px 44px; white-space:nowrap; border-radius:999px; }}
{BOLD_CSS.format(accent=accent, stroke=stroke, ink=ink) if bold else ""}
.caption {{ bottom:{bottom + 40}px; flex-wrap:wrap; gap:0 18px; color:{ink}; font-size:84px; font-weight:900; line-height:1.1;
  -webkit-text-stroke:10px {stroke}; paint-order:stroke fill; text-transform:uppercase; }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{T}" data-width="{W}" data-height="{H}">
<video id="base" class="clip" src="base.mp4" data-start="0" data-duration="{T}" muted playsinline></video>
{chr(10).join(els)}
</div>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
window.__timelines["main"] = tl;
tl.seek(0);
</script>
</body>
</html>
"""
    (hf / "index.html").write_text(page, encoding="utf-8")
    (hf / "hyperframes.json").write_text(json.dumps({
        "$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",
        "paths": {"blocks": "compositions", "components": "compositions/components", "assets": "assets"},
        "media": {"autoProxy": True}}, indent=2))
    (hf / "meta.json").write_text(json.dumps({"id": plan["project_id"], "name": plan["project_id"]}))


def render_overlay(hf: Path, out: Path, fps: int, quality: str) -> None:
    res = subprocess.run(["npx", "-y", HYPERFRAMES, "render", "-o", str(out), "-f", str(fps),
                          "-q", quality, "--quiet", "--no-best-effort"],
                         cwd=hf, capture_output=True, text=True,
                         env={**__import__("os").environ, "HYPERFRAMES_SKIP_SKILLS": "1"})
    if res.returncode != 0 or not out.exists():
        raise RuntimeError("HyperFrames render lỗi:\n" + "\n".join((res.stderr + res.stdout).splitlines()[-25:]))


def mux(video: Path, audio: Path, out: Path) -> None:
    run(["ffmpeg", "-y", "-v", "error", "-i", str(video), "-i", str(audio),
         "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
         "-ar", str(SR), "-shortest", "-movflags", "+faststart", str(out)])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--quality", default="delivery", choices=["draft", "looks", "delivery"])
    args = ap.parse_args()

    project = project_dir(args.project)
    plan = load_json(project / "edit" / "edit-plan.json")
    work = project / "edit" / "work"
    hf = project / "edit" / "hf"
    for d in (work, hf):
        shutil.rmtree(d, ignore_errors=True)
        d.mkdir(parents=True)
    (project / "out").mkdir(exist_ok=True)

    print("1/4 cắt và ghép hình...")
    base = cut_segments(project, plan, work)
    shutil.move(base, hf / "base.mp4")

    print("2/4 dựng âm thanh...")
    native = native_audio(project, plan, work)
    music = music_track(plan, work)
    pid = plan["project_id"]
    mixes = {}
    if music:
        mixes["final"] = master([native, music], plan, work / "mix_music.wav")
    if (plan["audio"].get("export_no_music", True) and plan["audio"].get("keep_native", True)) or not music:
        mixes["no-music"] = master([native], plan, work / "mix_nomusic.wav")

    print("3/4 vẽ phụ đề và chữ (HyperFrames)...")
    composition(plan, hf)
    visual = project / "edit" / "visual.mp4"
    render_overlay(hf, visual, plan["fps"], args.quality)

    print("4/4 xuất file...")
    outputs = []
    for name, audio in mixes.items():
        out = project / "out" / (f"final_{pid}.mp4" if name == "final" else f"final_{pid}_no-music.mp4")
        mux(visual, audio, out)
        outputs.append(out)
    shutil.rmtree(work, ignore_errors=True)
    for o in outputs:
        print("->", o.relative_to(project))


if __name__ == "__main__":
    main()
