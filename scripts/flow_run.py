"""Execute edit/gen_queue.json in Google Flow through the dedicated Chrome (scripts/cdp.py).

Usage: flow_run.py <project> [--stage images|clips|all] [--only id,id] [--dry-run]

Follows ad-creative/references/flow-runbook.md step by step:
  upload every reference file -> set the composer (mode, model, ratio, duration, x1)
  -> attach references -> type the prompt -> real-click generate -> wait for the new
  media URL -> download (images 2K, videos 1080p, never a credit-priced option)
  -> save under the queue's name (next free suffix if taken) -> log to edit/gen_log.jsonl.
Stops on: sign-in/captcha page, refusal text, retry budget spent, download timeout.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path

from cdp import CDP, pages, pick
from common import load_json, project_dir, save_json

LABEL = {  # queue value -> Flow label
    "nano-banana-2.1": "Nano Banana 2.1", "nano-banana-pro": "Nano Banana Pro",
    "omni-1.1-flash": "Omni 1.1 Flash", "veo-3.1": "Veo 3.1 - Fast",
    "veo-3.1-fast": "Veo 3.1 - Fast", "veo-3.1-quality": "Veo 3.1 - Quality",
}
WAIT = {"image": 180, "video": 480}
PAUSE_BETWEEN_JOBS = 5   # seconds between two submits (user rule 2026-10-27)
MAX_ACTIVE = 4           # generations running in Flow at the same time
POLL = 8                 # seconds between polls of the grid
REFUSAL = re.compile(r"Không thành công|vi phạm chính sách|không thể tạo|policy", re.I)
# Google flagged the automation itself ("hoạt động bất thường"): stop at once, no retry, and the
# runner is not started again for at least 10 minutes (runbook §4).
ABNORMAL = re.compile(r"hoạt động bất thường|unusual activity", re.I)


class Stop(Exception):
    pass


class Flow:
    def __init__(self, project: Path, dry: bool):
        self.project, self.dry = project, dry
        self.dl = project / "edit" / "downloads"
        self.dl.mkdir(parents=True, exist_ok=True)
        self.state_path = project / "edit" / "flow_project.json"
        self.state = load_json(self.state_path) if self.state_path.exists() else {"url": None, "uploaded": []}
        # the project's own tab first; else any Flow tab that is not the /about page
        self.c = CDP(pick(self.state["url"]) if self.state.get("url") and any(
            self.state["url"] in p["url"] for p in pages()) else pick("flow.google.com/project"))
        self.c.call("Page.enable")
        self.c.downloads(str(self.dl))
        self.pending_dl: list[dict] = []
        log_path = project / "edit" / "gen_log.jsonl"
        # assets generated in this Flow project (renamed to their file stem): usable as inputs at once
        self.made: set[str] = {json.loads(l).get("flow_name") for l in log_path.read_text().splitlines()
                               if l.strip()} - {None} if log_path.exists() else set()

    # ---------- primitives ----------
    def js(self, expr: str):
        return self.c.eval(expr)

    def rect(self, js: str):
        v = self.js("(()=>{const e=(%s); if(!e) return null; const r=e.getBoundingClientRect(); if(!r.width) return null;"
                    "return JSON.stringify({x:r.x+r.width/2,y:r.y+r.height/2,w:r.width})})()" % js)
        return json.loads(v) if v else None

    def click(self, r: dict) -> None:
        for t in ("mousePressed", "mouseReleased"):
            self.c.call("Input.dispatchMouseEvent", type=t, x=r["x"], y=r["y"], button="left", clickCount=1)

    def hover(self, r: dict) -> None:
        self.c.call("Input.dispatchMouseEvent", type="mouseMoved", x=max(5, r["x"] - 60), y=max(5, r["y"] - 60))
        time.sleep(0.3)
        self.c.call("Input.dispatchMouseEvent", type="mouseMoved", x=r["x"], y=r["y"])
        time.sleep(1.0)

    def esc(self) -> None:
        for t in ("keyDown", "keyUp"):
            self.c.call("Input.dispatchKeyEvent", type=t, key="Escape", code="Escape")
        time.sleep(0.4)

    def close_overlays(self) -> None:
        """Settings popup / media panel keep a backdrop that eats mouse events: close them for real."""
        for _ in range(4):
            t = self.overlay()
            # a leftover dialog/toast ("Xong", "Đóng", "Đã sao chép 1 mục") also swallows clicks
            for label in ("Xong", "Đóng"):
                b = self.overlay_btn(label)
                if b:
                    self.click(b)
                    time.sleep(0.5)
                    t = self.overlay()
            if not re.search(r"Khung hình|Hình ảnh \| |Tìm kiếm thành phần|tín dụng", t):
                return
            # a real click in the gutter between the sidebar and the grid closes popovers;
            # Escape and JS clicks do not
            self.click({"x": 240, "y": 480})
            time.sleep(0.6)
            if re.search(r"Khung hình|Hình ảnh \| |Tìm kiếm thành phần|tín dụng", self.overlay()):
                self.esc()
        raise Stop("Không đóng được bảng cài đặt/thư viện")

    def overlay(self) -> str:
        return self.js("(document.querySelector('.cdk-overlay-container')||{innerText:''}).innerText.replace(/\\n+/g,' | ')") or ""

    def overlay_btn(self, label: str):
        """Visible overlay button whose text ends with label (icon ligature text may precede it)."""
        return self.rect("[...document.querySelectorAll('.cdk-overlay-container button')].find(b=>b.getBoundingClientRect().width>0"
                         "&&b.textContent.replace(/\\s+/g,' ').trim().endsWith(%s))" % json.dumps(label))

    def menu_items(self) -> list[str]:
        return json.loads(self.js("JSON.stringify([...document.querySelectorAll('[role=menuitem],.mat-mdc-menu-content button')]"
                                  ".filter(m=>m.getBoundingClientRect().width>0).map(m=>m.innerText.replace(/\\n+/g,' ').trim()))"))

    def menu_item(self, pattern: str):
        return self.rect("[...document.querySelectorAll('[role=menuitem],.mat-mdc-menu-content button')]"
                         ".find(m=>m.getBoundingClientRect().width>0&&new RegExp(%s).test(m.innerText))" % json.dumps(pattern))

    def guard(self) -> None:
        url = self.js("location.href")
        txt = self.js("document.body.innerText.slice(0,4000)")
        if "accounts.google" in url or "Đăng nhập" in txt[:300]:
            raise Stop("Flow yêu cầu đăng nhập lại")
        if re.search(r"captcha|xác minh bạn không phải", txt, re.I):
            raise Stop("Gặp captcha/xác minh — cần bạn giải tay")

    # ---------- project ----------
    def ensure_project(self) -> None:
        if self.state.get("url"):
            if self.js("location.href") != self.state["url"]:
                self.c.nav(self.state["url"])
            self.guard()
            return
        self.c.nav("https://flow.google.com/")
        time.sleep(2)
        self.guard()
        self.js("[...document.querySelectorAll('button,a,[role=button]')].find(e=>/Dự án mới/.test(e.textContent)).click()")
        for _ in range(20):
            time.sleep(1)
            url = self.js("location.href")
            if "/project/" in url:
                break
        else:
            raise Stop("Không tạo được project mới")
        self.js("""(()=>{const t=document.querySelector('input[aria-label="Văn bản có thể chỉnh sửa"]'); if(!t) return;
            t.focus(); Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(t, %s);
            t.dispatchEvent(new Event('input',{bubbles:true})); t.dispatchEvent(new Event('change',{bubbles:true}));
            t.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',bubbles:true})); t.blur();})()""" % json.dumps(self.project.name))
        self.state["url"] = url
        save_json(self.state_path, self.state)
        print(f"   project Flow mới: {url}")

    # ---------- references ----------
    def panel_open(self) -> None:
        self.close_overlays()
        plus = None
        for _ in range(30):  # a freshly created project mounts the composer late
            plus = self.rect("[...document.querySelectorAll('button')].find(b=>/Thêm thành phần/.test(b.getAttribute('aria-label')||'')&&b.getBoundingClientRect().width>0)")
            if plus:
                break
            time.sleep(0.5)
        if not plus:
            self.c.shot(self.project / "edit" / "qc" / "flow_fail_plus.jpg")
            raise Stop(f"Không thấy nút + (Thêm thành phần) trên {self.js('location.href')}")
        self.click(plus)
        for i in range(16):  # the panel mounts asynchronously
            time.sleep(0.5)
            if self.rect("document.querySelector('input[placeholder*=\"Tìm kiếm thành phần\"]')"):
                return
            if i == 7:  # the first click may have been eaten by a closing toast: once more
                self.close_overlays()
                self.click(plus)
        self.c.shot(self.project / "edit" / "qc" / "flow_fail_panel.jpg")
        raise Stop(f"Thư viện thành phần không mở (overlay: {self.overlay()[:80]!r}, +: {plus})")

    def panel_find(self, name: str):
        """Search the add-media panel for an asset tile by file name; returns its rect or None."""
        box = self.rect("document.querySelector('input[placeholder*=\"Tìm kiếm thành phần\"]')")
        if not box:
            return None
        self.click(box)
        # cmd+A only selects with the editing command attached; without it the new name was
        # appended to the previous search ("keyframe_c1keyframe_c2") and uploads looked missing
        self.c.call("Input.dispatchKeyEvent", type="keyDown", key="a", code="KeyA", modifiers=4, commands=["selectAll"])
        self.c.call("Input.dispatchKeyEvent", type="keyUp", key="a", code="KeyA", modifiers=4)
        self.c.call("Input.insertText", text=Path(name).stem)
        if self.js("document.querySelector('input[placeholder*=\"Tìm kiếm thành phần\"]').value") != Path(name).stem:
            self.js("(()=>{const i=document.querySelector('input[placeholder*=\"Tìm kiếm thành phần\"]');"
                    "i.value=%s;i.dispatchEvent(new Event('input',{bubbles:true}));})()" % json.dumps(Path(name).stem))
        for _ in range(8):
            time.sleep(0.6)
            hit = self.rect("[...document.querySelectorAll('.cdk-overlay-container *')].find(e=>e.children.length<=3"
                            "&&e.getBoundingClientRect().width>0&&(e.innerText||'').trim().startsWith(%s))" % json.dumps(name))
            if hit:
                return hit
        return None

    def upload(self, rel: str) -> None:
        name = Path(rel).name
        if name in self.state["uploaded"]:
            return
        self.panel_open()
        if self.panel_find(name):
            self.esc()
            self.state["uploaded"].append(name)
            save_json(self.state_path, self.state)
            return
        self.esc()
        src = self.project / rel
        if not src.exists():
            raise Stop(f"Thiếu file tham chiếu {rel}")
        print(f"   upload {name}")
        self.c.drop([str(src)])
        for _ in range(30):
            time.sleep(2)
            self.panel_open()
            if self.panel_find(name):
                self.esc()
                self.state["uploaded"].append(name)
                save_json(self.state_path, self.state)
                return
            self.esc()
        raise Stop(f"Upload {name} không thấy trong thư viện sau 60 s")

    def attach(self, rel: str) -> None:
        name = Path(rel).name
        self.panel_open()
        tile = self.panel_find(name) or self.panel_find(Path(name).stem)
        if not tile:
            raise Stop(f"Không tìm thấy {name} trong thư viện để gắn vào prompt")
        self.click(tile)
        time.sleep(0.8)
        add = self.rect("[...document.querySelectorAll('button')].find(b=>/Thêm vào câu lệnh/.test(b.textContent)&&b.getBoundingClientRect().width>0)")
        if not add:
            raise Stop("Không thấy nút 'Thêm vào câu lệnh'")
        self.click(add)
        time.sleep(0.8)
        self.close_overlays()

    # ---------- composer ----------
    def clear_composer(self) -> None:
        self.esc()
        x = self.rect("[...document.querySelectorAll('button')].find(b=>/Xoá câu lệnh|Xóa câu lệnh/.test(b.getAttribute('aria-label')||b.textContent)&&b.getBoundingClientRect().width>0)")
        if x:
            self.click(x)
            time.sleep(0.5)
        self.js("(()=>{const f=document.querySelector('.ProseMirror'); if(!f) return; f.focus();"
                "document.execCommand('selectAll',false,null); document.execCommand('delete',false,null);})()")
        # chips left in the composer have a close icon next to them
        self.js("[...document.querySelectorAll('form button, [class*=composer] button')].filter(b=>/cancel|close/.test(b.textContent)&&b.getBoundingClientRect().width>0&&b.getBoundingClientRect().width<40).forEach(b=>b.click())")
        time.sleep(0.4)

    def settings(self, kind: str, job: dict) -> None:
        self.js("[...document.querySelectorAll('button')].find(b=>/settings-trigger/.test(b.className)&&b.getBoundingClientRect().width>0).click()")
        time.sleep(1.2)
        if "Khung hình" not in self.overlay() and "Hình ảnh" not in self.overlay():
            raise Stop("Không mở được bảng cài đặt")
        want = ["Video" if kind == "video" else "Hình ảnh"]
        if kind == "video":
            want.append("Thành phần" if job.get("mode", "ingredients") == "ingredients" else "Khung hình")
        want.append(job.get("ratio", "9:16"))
        for label in want:
            b = self.overlay_btn(label)
            if not b:
                raise Stop(f"Không thấy lựa chọn '{label}' trong cài đặt")
            self.click(b)
            time.sleep(0.6)
        model = LABEL.get(job["tool"], job["tool"])
        if model not in self.overlay():
            dd = self.rect("[...document.querySelectorAll('.cdk-overlay-container button')].find(b=>/arrow_drop_down/.test(b.textContent)&&b.getBoundingClientRect().width>0)")
            if dd:
                self.click(dd)
                time.sleep(1.0)
        if model + " | arrow_drop_down" not in self.overlay():
            o = self.rect("[...document.querySelectorAll('.cdk-overlay-container [role=option], .cdk-overlay-container mat-option')]"
                          ".find(e=>e.getBoundingClientRect().width>0&&e.textContent.replace(/\\s+/g,' ').trim().replace(/^volume_up /,'')===%s)" % json.dumps(model))
            if not o:
                raise Stop(f"Model '{model}' không có trong danh sách")
            self.click(o)
            time.sleep(1.2)
        if kind == "video":
            d = self.overlay_btn(f"{job.get('duration', 8)} giây")
            if d:
                self.click(d)
                time.sleep(0.4)
        x1 = self.overlay_btn("x1")
        if x1:
            self.click(x1)
            time.sleep(0.4)
        cost = re.search(r"tốn ([^|]+)", self.overlay())
        checked = json.loads(self.js("JSON.stringify([...document.querySelectorAll('.cdk-overlay-container button')]"
                                     ".filter(e=>e.getBoundingClientRect().width>0&&e.getAttribute('aria-checked')==='true')"
                                     ".map(e=>e.textContent.replace(/\\s+/g,' ').trim()))"))
        print(f"   cài đặt: {model} · {' · '.join(checked)}" + (f" · {cost.group(1).strip()}" if cost else ""))
        self.close_overlays()

    def prompt(self, text: str) -> None:
        self.js("(()=>{const f=document.querySelector('.ProseMirror'); f.focus(); document.execCommand('selectAll',false,null); document.execCommand('delete',false,null);})()")
        self.c.call("Input.insertText", text=text)
        time.sleep(0.6)
        got = self.js("document.querySelector('.ProseMirror').innerText.length")
        if abs(got - len(text)) > 5:
            raise Stop(f"Prompt nhập thiếu ({got}/{len(text)} ký tự)")

    def media_ids(self) -> dict[str, str]:
        """{media id: kind} for every tile. A video tile shows a poster under /image/<same id>,
        so ids are compared (signed URLs change) and the kind comes from the play icon."""
        return json.loads(self.js("""JSON.stringify(Object.fromEntries([...document.querySelectorAll('img,video,source')]
            .map(e=>[(e.src||e.currentSrc||'').match(/flow-content\\.google\\/(?:image|video)\\/([0-9a-f-]{36})/)||[], e])
            .filter(([m])=>m.length).map(([m,e])=>{const t=e.closest('[class*=tile], [class*=virtual-item]')||e.parentElement;
            const isVideo=e.tagName==='VIDEO'||/play_circle/.test(t.innerText||'')||/\\/video\\//.test(e.src||'');
            return [m[1], isVideo?'video':'image'];})))"""))

    def generate(self, kind: str) -> str:
        time.sleep(3)  # let lazily mounted tiles (fresh uploads) appear before the baseline
        before = set(self.media_ids())
        min_wait = 15 if kind == "image" else 40  # nothing real finishes faster than this
        gen = self.rect("[...document.querySelectorAll('button')].find(b=>/Bắt đầu tạo/.test(b.getAttribute('aria-label')||'')&&b.getBoundingClientRect().width>0)")
        if not gen:
            raise Stop("Không thấy nút 'Bắt đầu tạo'")
        self.click(gen)
        t0 = time.time()
        while time.time() - t0 < WAIT[kind]:
            time.sleep(10)
            txt = self.js("document.body.innerText.slice(0,3000)")
            if ABNORMAL.search(txt):
                raise Stop("Flow báo hoạt động bất thường — dừng hẳn, chờ ít nhất 10 phút rồi mới chạy lại")
            if REFUSAL.search(txt):
                raise Stop("Flow từ chối prompt này (chính sách)")
            ids = self.media_ids()
            new = [i for i, k in ids.items() if i not in before and k == kind]
            # a tile still rendering shows a percentage; wait until none is left for this tile
            if new and time.time() - t0 >= min_wait and not re.search(r"\b\d{1,2}%", self.js("document.body.innerText.slice(0,2000)") or ""):
                print(f"   xong sau {int(time.time() - t0)} s")
                return f"https://flow-content.google/{kind}/{new[0]}"
        raise Stop(f"Hết {WAIT[kind]} s mà chưa thấy kết quả")

    def leave_detail(self) -> bool:
        """Clicking a tile image opens /project/<id>/edit/<media>; the grid (and its menus) live
        on /project/<id>. Returns True if it had to navigate back."""
        if "/edit/" in (self.js("location.href") or ""):
            self.c.nav(self.state["url"])
            time.sleep(3)
            self.guard()
            return True
        return False

    # ---------- tile menu ----------
    def tile_menu(self, mid: str | None, item: str, rect: dict | None = None) -> list[str]:
        """Hover the tile with media id `mid` (newest tile if not found), open 'Tuỳ chọn khác',
        click the menu item matching `item`; returns the menu as it was before the click."""
        self.leave_detail()
        tile = rect
        for _ in range(0 if rect else 12):
            tile = self.rect("(()=>{const e=[...document.querySelectorAll('img,video,source')].find(e=>(e.src||e.currentSrc||'').includes(%s));"
                             "return e&&(e.closest('flow-grid-tile-container')||e)})()" % json.dumps(mid))
            if tile:
                break
            time.sleep(5)
        if not tile:  # newest tile is top-left
            t = self.grid_tiles(1)
            if not t:
                raise Stop("Không có tile nào trong lưới")
            tile = {"x": t[0]["x"], "y": t[0]["y"], "w": t[0]["w"], "h": t[0].get("h", 260)}
        h = tile.get("h", 260)
        items: list[str] = []
        self.close_overlays()
        for _ in range(3):
            self.esc()
            if self.leave_detail():  # a stray click opened the detail view: back to the grid
                time.sleep(2)
                self.close_overlays()
            self.hover(tile)
            # every tile has its own 'Tuỳ chọn khác' (top-right corner of the tile): take the one inside this tile
            more = self.rect("[...document.querySelectorAll('button')].find(b=>{if(!/Tuỳ chọn khác/.test(b.getAttribute('aria-label')||''))return false;"
                             "const r=b.getBoundingClientRect();return r.width>0&&Math.abs(r.x+r.width/2-%f)<%f&&Math.abs(r.y+r.height/2-%f)<%f})"
                             % (tile["x"], tile["w"] / 2 + 2, tile["y"], h / 2 + 2))
            if more:
                self.click(more)
                time.sleep(1.2)
                items = self.menu_items()
                if any(item in i for i in items):
                    break
        else:
            raise Stop(f"Không mở được menu của tile ({item})")
        self.js("[...document.querySelectorAll('[role=menuitem],.mat-mdc-menu-content button')].find(m=>new RegExp(%s).test(m.innerText))?.scrollIntoView({block:'center'})" % json.dumps(item))
        time.sleep(0.3)
        self.click(self.menu_item(item))
        time.sleep(1.2)
        return items

    def rename(self, url: str | None, name: str, rect: dict | None = None) -> None:
        """Flow names a result after its prompt ("Man stepping out of car"); the user's rule
        (2026-10-27) is that every generated asset carries the name it is saved under
        (keyframe_c3, c04_a) so the library and the project files match. Menu 'Đổi tên' opens a
        dialog with one input (aria-label "Văn bản có thể chỉnh sửa") and buttons Xong / Huỷ."""
        mid = re.search(r"/(?:image|video)/([0-9a-f-]+)", url).group(1) if url else None
        self.tile_menu(mid, "Đổi tên", rect)
        box = self.rect("document.querySelector('.cdk-overlay-container input[aria-label=\"Văn bản có thể chỉnh sửa\"]')")
        if not box:
            self.esc()
            raise Stop("Hộp thoại Đổi tên không mở")
        self.click(box)
        self.c.call("Input.dispatchKeyEvent", type="keyDown", key="a", code="KeyA", modifiers=4, commands=["selectAll"])
        self.c.call("Input.dispatchKeyEvent", type="keyUp", key="a", code="KeyA", modifiers=4)
        self.c.call("Input.insertText", text=name)
        time.sleep(0.3)
        ok = self.rect("[...document.querySelectorAll('.cdk-overlay-container button')].find(b=>b.getBoundingClientRect().width>0"
                       "&&((b.getAttribute('aria-label')||'')==='Xong'||b.textContent.trim()==='done'))")
        if not ok:
            self.esc()
            raise Stop("Không thấy nút Xong trong hộp thoại Đổi tên")
        self.click(ok)
        time.sleep(1.0)
        if mid:
            got = self.js("(()=>{const e=[...document.querySelectorAll('img,video')].find(e=>(e.src||e.currentSrc||'').includes(%s));"
                          "const t=e&&e.closest('flow-grid-tile-container');return t?t.innerText:''})()" % json.dumps(mid)) or ""
            if name not in got:
                print(f"   (cảnh báo: tile chưa hiện tên {name}: {got[:60]!r})")

    # ---------- download ----------
    def download(self, url: str | None, kind: str, size: str, rect: dict | None = None, wait: bool = True) -> Path | None:
        mid = re.search(r"/(?:image|video)/([0-9a-f-]+)", url).group(1) if url else None
        self.tile_menu(mid, "Tải xuống", rect)
        sub = self.menu_items()
        choice = next((s for s in sub if s.startswith(size) and "tín dụng" not in s), None)
        if not choice:
            self.esc()
            raise Stop(f"Không có lựa chọn tải {size} miễn phí: {sub}")
        before = set(os.listdir(self.dl))
        self.click(self.menu_item("^" + re.escape(choice.split(" ")[0])))
        if not wait:  # batch mode: the file is collected later (collect_downloads), work goes on
            self.esc()
            return None
        for _ in range(90):
            time.sleep(2)
            new = [f for f in os.listdir(self.dl) if f not in before and not f.endswith(".crdownload")]
            if new:
                self.esc()
                return self.dl / new[0]
        raise Stop("Tải về không xong sau 3 phút")

    # ---------- one job ----------
    def run_job(self, job: dict, log) -> Path:
        kind = job["kind"]
        self.ensure_project()
        for ref in job.get("refs", []):
            self.upload(f"frames/{ref}")
        self.clear_composer()
        for ref in job.get("refs", []):
            self.attach(ref)
        self.settings(kind, job)
        self.prompt(job["prompt"])
        if self.dry:
            print("   (dry-run: không bấm tạo)")
            return Path()
        url = self.generate(kind)
        f = self.download(url, kind, job.get("download", "2K" if kind == "image" else "1080p"))
        dest = self.project / job["save_as"]
        while dest.exists():  # never overwrite: next free suffix
            stem, suf = dest.stem, dest.suffix
            m = re.match(r"(.*)_([a-z])$", stem)
            dest = dest.with_name(f"{m.group(1)}_{chr(ord(m.group(2)) + 1)}{suf}" if m else f"{stem}_b{suf}")
        if kind == "image" and f.suffix.lower() != dest.suffix.lower():
            os.system(f'sips -s format png "{f}" --out "{dest}" >/dev/null')
        else:
            shutil.copy(f, dest)
        self.rename(url, dest.stem)  # the Flow asset carries the saved file's name
        print(f"   đổi tên trong Flow -> {dest.stem}")
        log({"job": job["id"], "url": url.split("?")[0], "file": str(dest.relative_to(self.project)), "flow_name": dest.stem, "settings": {
            "tool": job["tool"], "mode": job.get("mode"), "download": job.get("download")}})
        return dest

    # ---------- batch mode: upload once, submit independent jobs together ----------
    def upload_all(self, names: list[str]) -> None:
        """One drop for every reference file not yet in the library, then verify each."""
        missing = [n for n in dict.fromkeys(names) if n not in self.state["uploaded"]
                   and Path(n).stem not in self.made and (self.project / "frames" / n).exists()]
        if not missing:
            return
        self.panel_open()
        for n in list(missing):
            if self.panel_find(n):
                self.state["uploaded"].append(n)
                missing.remove(n)
        self.esc()
        save_json(self.state_path, self.state)
        if not missing:
            return
        print(f"   upload 1 lượt: {', '.join(missing)}")
        self.c.drop([str(self.project / "frames" / n) for n in missing])
        for _ in range(40):
            time.sleep(2)
            self.panel_open()
            for n in list(missing):
                if self.panel_find(n):
                    self.state["uploaded"].append(n)
                    missing.remove(n)
            self.esc()
            save_json(self.state_path, self.state)
            if not missing:
                return
        raise Stop(f"Upload không thấy trong thư viện sau 80 s: {missing}")

    def submit(self, job: dict) -> str:
        """Compose and press 'Bắt đầu tạo' without waiting. Returns the prompt key used to
        find this job's tile later (a rendering tile shows the prompt text and a percentage)."""
        self.clear_composer()
        for ref in job.get("refs", []):
            self.attach(ref)
        self.settings(job["kind"], job)
        self.prompt(job["prompt"])
        key = job["id"]
        if self.dry:
            print("   (dry-run: không bấm tạo)")
            return key
        gen = self.rect("[...document.querySelectorAll('button')].find(b=>/Bắt đầu tạo/.test(b.getAttribute('aria-label')||'')&&b.getBoundingClientRect().width>0)")
        if not gen:
            raise Stop("Không thấy nút 'Bắt đầu tạo'")
        self.click(gen)
        return key

    def grid_tiles(self, n: int = 16) -> list[dict]:
        """The newest n tiles of the project grid, newest first. Flow renders one
        <flow-grid-tile-container> per asset in creation order (row by row); a rendering one
        shows a percentage, a finished one holds an <img>/<video> under flow-content.google
        with the media id (video tiles carry a poster under /image/<same id>).
        Each: {kind, pct, ids, text}."""
        v = self.js("""(()=>{const norm=t=>(t||'').replace(/\\s+/g,' ').trim();
            const tiles=[...document.querySelectorAll('flow-grid-tile-container')]
              .map(t=>({t,r:t.getBoundingClientRect()})).filter(({r})=>r.width>80)
              .sort((a,b)=>(a.r.y-b.r.y)||(a.r.x-b.r.x)).slice(0,%d);
            return JSON.stringify(tiles.map(({t})=>{const txt=norm(t.innerText);
              const pct=(txt.match(/\\b(\\d{1,3})%%/)||[])[1]||null;
              const kind=t.querySelector('flow-video-tile')?'video':(t.querySelector('flow-image-tile')?'image':null);
              const ids=[...t.querySelectorAll('img,video,source')].map(e=>((e.src||e.currentSrc||'').match(/flow-content\\.google\\/(?:image|video)\\/([0-9a-f-]{36})/)||[])[1]).filter(Boolean);
              const r=t.getBoundingClientRect();
              return {kind, pct, ids:[...new Set(ids)], text:txt.slice(0,60), x:r.x+r.width/2, y:r.y+r.height/2, w:r.width, h:r.height};}));})()""" % n)
        return json.loads(v or "[]")

    def tile_status(self, index: int, kind: str, taken: set[str]) -> tuple[str | None, str | None]:
        """(percent, media id) of the tile at position `index` from the newest."""
        tiles = self.grid_tiles()
        if index >= len(tiles):
            return None, None
        t = tiles[index]
        if REFUSAL.search(t.get("text") or ""):
            return "refused", None
        if t["pct"] is not None:
            return t["pct"], None
        ids = [i for i in t["ids"] if i not in taken]
        return None, (ids[0] if ids and t.get("kind") == kind else None)

    def finish(self, job: dict, mid: str | None, log, rect: dict | None = None) -> Path:
        """Rename the Flow asset to its file name, start the download without waiting for it
        (collect_downloads picks the file up later: Flow names it after the asset title), log."""
        kind = job["kind"]
        url = f"https://flow-content.google/{kind}/{mid}" if mid else None
        dest = self.project / job["save_as"]
        claimed = {d["dest"] for d in self.pending_dl}
        while dest.exists() or dest in claimed:  # never overwrite: next free suffix
            stem, suf = dest.stem, dest.suffix
            m = re.match(r"(.*)_([a-z])$", stem)
            dest = dest.with_name(f"{m.group(1)}_{chr(ord(m.group(2)) + 1)}{suf}" if m else f"{stem}_b{suf}")
        self.rename(url, dest.stem, rect)
        self.download(url, kind, job.get("download", "1K" if kind == "image" else "1080p"), rect, wait=False)
        self.pending_dl.append({"stem": dest.stem, "dest": dest, "kind": kind, "t": time.time()})
        self.made.add(dest.stem)
        print(f"   {job['id']}: đổi tên trong Flow -> {dest.stem}, đang tải nền -> {dest.relative_to(self.project)}")
        log({"job": job["id"], "url": url, "file": str(dest.relative_to(self.project)), "flow_name": dest.stem,
             "settings": {"tool": job["tool"], "mode": job.get("mode"), "download": job.get("download")}})
        return dest

    def collect_downloads(self, wait: float = 0) -> None:
        """Move finished downloads (named '<asset title>_<size>_<time>.<ext>') to their dest."""
        t_end = time.time() + wait
        while self.pending_dl:
            files = [f for f in os.listdir(self.dl) if not f.endswith(".crdownload")]
            for d in list(self.pending_dl):
                hit = sorted((f for f in files if f.startswith(d["stem"] + "_") or f.startswith(d["stem"] + ".")),
                             key=lambda f: os.path.getmtime(self.dl / f))
                hit = [f for f in hit if os.path.getmtime(self.dl / f) >= d["t"] - 5]
                if not hit:
                    if time.time() - d["t"] > 600:
                        print(f"   (tải {d['stem']} quá 10 phút, bỏ — tải tay trong Flow)")
                        self.pending_dl.remove(d)
                    continue
                src = self.dl / hit[-1]
                if d["kind"] == "image" and src.suffix.lower() != d["dest"].suffix.lower():
                    os.system(f'sips -s format png "{src}" --out "{d["dest"]}" >/dev/null')
                else:
                    shutil.copy(src, d["dest"])
                print(f"   tải xong -> {d['dest'].relative_to(self.project)}")
                self.pending_dl.remove(d)
            if not self.pending_dl or time.time() >= t_end:
                return
            time.sleep(3)

    def retry_tile(self, index: int) -> bool:
        """Press the failed tile's own retry button (no recomposing). True if it was pressed."""
        tiles = self.grid_tiles(index + 1)
        if index >= len(tiles):
            return False
        t = tiles[index]
        self.hover({"x": t["x"], "y": t["y"], "w": t["w"]})
        b = self.rect("[...document.querySelectorAll('button')].find(b=>{const r=b.getBoundingClientRect();"
                      "if(!r.width||Math.abs(r.x+r.width/2-%f)>%f||Math.abs(r.y+r.height/2-%f)>%f)return false;"
                      "const s=(b.getAttribute('aria-label')||'')+' '+b.textContent;return /Thử lại|Tạo lại|retry|refresh/i.test(s);})"
                      % (t["x"], t["w"] / 2 + 2, t["y"], t["h"] / 2 + 2))
        if not b:
            return False
        self.click(b)
        return True

    def upload_tracked(self, refs: list[str], events: list) -> None:
        """Upload refs during a batch run and account for the grid tiles they add (one per file),
        so later tile positions stay correct."""
        missing = [n for n in dict.fromkeys(refs) if n not in self.state["uploaded"]
                   and Path(n).stem not in self.made and (self.project / "frames" / n).exists()]
        if not missing:
            return
        before = len(self.grid_tiles(40))
        self.upload_all(missing)
        for _ in range(30):  # the new tiles mount late
            if len(self.grid_tiles(40)) >= before + len(missing):
                break
            time.sleep(2)
        for n in missing:
            events.append({"type": "upload", "name": n})

    def run_queue(self, jobs: list[dict], budget: int, log) -> None:
        """Submit every job whose inputs exist (up to MAX_ACTIVE at once), poll the grid, and
        finish each result the moment it lands; a finished keyframe unlocks its clip.
        Tiles are matched by position: Flow keeps tiles in creation order, newest first, so the
        k-th event of this run (a submit or an upload) owns tile index len(events)-1-k."""
        self.ensure_project()
        taken = {(json.loads(l).get("url") or "").split("/")[-1] for l in
                 (self.project / "edit" / "gen_log.jsonl").read_text().splitlines() if l.strip()} \
            if (self.project / "edit" / "gen_log.jsonl").exists() else set()
        pending = list(jobs)
        active: dict[str, dict] = {}   # job id -> {job, event, t0}
        attempts: dict[str, int] = {}
        events: list = []
        self.upload_all([r for j in jobs for r in j.get("refs", [])])  # before any submit: no tracking needed
        last_submit = 0.0
        while pending or active:
            for job in list(pending):
                if len(active) >= MAX_ACTIVE:
                    break
                refs = job.get("refs", [])
                if not all((self.project / "frames" / r).exists() or Path(r).stem in self.made for r in refs):
                    continue  # waits for its keyframe to finish in Flow (not for the download)
                if time.time() - last_submit < PAUSE_BETWEEN_JOBS:
                    time.sleep(PAUSE_BETWEEN_JOBS - (time.time() - last_submit))
                self.upload_tracked(refs, events)
                attempts[job["id"]] = attempts.get(job["id"], 0) + 1
                try:
                    self.submit(job)
                except Stop as e:
                    log({"job": job["id"], "attempt": attempts[job["id"]], "error": str(e)})
                    print(f"   {job['id']}: DỪNG: {e}")
                    if "bất thường" in str(e) or "đăng nhập" in str(e) or "captcha" in str(e).lower():
                        sys.exit(1)
                    if budget <= 0:  # give this job up, keep collecting the ones already running
                        pending.remove(job)
                        print(f"   {job['id']}: bỏ qua (hết hạn mức gen lại)")
                        continue
                    budget -= 1
                    continue
                last_submit = time.time()
                pending.remove(job)
                events.append({"type": "job", "id": job["id"]})
                active[job["id"]] = {"job": job, "event": len(events) - 1, "t0": time.time()}
                print(f"== {job['kind']} {job['id']} đã gửi ({len(active)} đang chạy)")
                if self.dry:
                    active.pop(job["id"])
            if not active:
                if pending and not self.dry:
                    time.sleep(POLL)
                    continue
                break
            time.sleep(POLL)
            self.collect_downloads()
            txt = self.js("document.body.innerText.slice(0,4000)") or ""
            if ABNORMAL.search(txt):
                sys.exit("Flow báo hoạt động bất thường — dừng hẳn, chờ ít nhất 10 phút rồi mới chạy lại")
            self.guard()
            for jid, a in list(active.items()):
                job = a["job"]
                pct, mid = self.tile_status(len(events) - 1 - a["event"], job["kind"], taken)
                elapsed = time.time() - a["t0"]
                if mid and elapsed >= (15 if job["kind"] == "image" else 40):
                    taken.add(mid)
                    print(f"   {jid}: xong sau {int(elapsed)} s")
                    try:
                        self.finish(job, mid, log)
                    except Stop as e:
                        log({"job": jid, "attempt": attempts[jid], "error": str(e), "media": mid})
                        print(f"   {jid}: DỪNG khi tải/đổi tên: {e}")
                        if budget > 0:
                            budget -= 1
                            pending.insert(0, job)
                    active.pop(jid)
                elif pct == "refused":  # this job's own tile says it failed (page-wide text is not evidence)
                    log({"job": jid, "attempt": attempts[jid], "error": "Flow từ chối prompt này (chính sách)"})
                    idx = len(events) - 1 - a["event"]
                    n_before = len(self.grid_tiles(60))
                    if budget > 0 and attempts[jid] < 3 and self.retry_tile(idx):
                        budget -= 1
                        attempts[jid] += 1
                        time.sleep(3)
                        if len(self.grid_tiles(60)) > n_before:  # retry made a new tile at the top
                            events.append({"type": "job", "id": jid})
                            a["event"] = len(events) - 1
                        a["t0"] = time.time()
                        print(f"   {jid}: Flow từ chối — đã bấm Thử lại trên tile")
                        continue
                    print(f"   {jid}: Flow từ chối (chính sách)")
                    active.pop(jid)
                    if budget > 0 and attempts[jid] < 3:
                        budget -= 1
                        pending.insert(0, job)
                elif elapsed > WAIT[job["kind"]]:
                    log({"job": jid, "attempt": attempts[jid], "error": f"Hết {WAIT[job['kind']]} s mà chưa thấy kết quả"})
                    print(f"   {jid}: hết giờ chờ (tile {len(events) - 1 - a['event']}: {self.grid_tiles()[:1]})")
                    active.pop(jid)
                    if budget > 0 and attempts[jid] < 2:
                        budget -= 1
                        pending.insert(0, job)
        if self.pending_dl:
            print(f"   chờ {len(self.pending_dl)} file tải nền...")
            self.collect_downloads(wait=300)
        print("Hàng đợi xong.")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--stage", default="all", choices=["images", "clips", "all"])
    ap.add_argument("--only", default="", help="job ids, comma separated")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--serial", action="store_true", help="một job một lúc (chế độ cũ)")
    args = ap.parse_args()

    project = project_dir(args.project)
    queue = load_json(project / "edit" / "gen_queue.json")
    only = {s.strip() for s in args.only.split(",") if s.strip()}
    jobs = [j for j in queue["jobs"] if (not only or j["id"] in only)
            and (args.stage == "all" or (args.stage == "images") == (j["kind"] == "image"))]
    if not jobs:
        sys.exit("Không có job nào khớp")
    try:
        pages()
    except Exception:
        sys.exit("Flow Chrome chưa chạy: scripts/flow_chrome.sh")
    logf = (project / "edit" / "gen_log.jsonl").open("a", encoding="utf-8")

    def log(d: dict) -> None:
        logf.write(json.dumps({"t": datetime.now().isoformat(timespec="seconds"), **d}, ensure_ascii=False) + "\n")
        logf.flush()

    flow = Flow(project, args.dry_run)
    budget = int(queue.get("retry_budget", 2))
    if not args.serial:
        flow.run_queue(jobs, budget, log)
        return
    for k, job in enumerate(jobs):
        if k:
            time.sleep(PAUSE_BETWEEN_JOBS)
        print(f"== {job['kind']} {job['id']} -> {job['save_as']}")
        attempt = 0
        while True:
            attempt += 1
            try:
                dest = flow.run_job(job, log)
                print(f"   -> {dest.relative_to(project) if dest != Path() else '(dry)'}")
                break
            except Stop as e:
                log({"job": job["id"], "attempt": attempt, "error": str(e)})
                print(f"   DỪNG: {e}")
                if budget <= 0 or "đăng nhập" in str(e) or "captcha" in str(e).lower() or "bất thường" in str(e):
                    sys.exit(1)
                budget -= 1
                print(f"   thử lại ({budget} lần còn lại)")
    print("Hàng đợi xong.")


if __name__ == "__main__":
    main()
