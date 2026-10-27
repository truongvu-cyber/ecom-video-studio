"""Tiny Chrome DevTools client for the Flow Chrome (scripts/flow_chrome.sh, port 9222).

Usage:
  cdp.py pages                               list open tabs
  cdp.py shot <match> <out.jpg>              screenshot the tab whose url/title contains <match>
  cdp.py eval <match> '<js expression>'      evaluate JS (awaits promises), prints JSON
  cdp.py nav <match> <url>                   navigate that tab
  cdp.py new <url>                           open a new tab
  cdp.py upload <match> <css selector> <file> [file...]   set files on an <input type=file>
  cdp.py drop <match> <file> [file...]       drop files onto the page centre (no native dialog)
  cdp.py pick <match> '<js that clicks the upload button>' <file> [file...]   intercept the file chooser
  cdp.py downloads <match> <dir>             send this tab's downloads to <dir>
Used by the Flow runbook so every browser step is a logged command, not a hand click.
"""
from __future__ import annotations

import base64
import json
import sys
import time
import urllib.request
from pathlib import Path

import websocket

PORT = 9222


def pages() -> list[dict]:
    with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json") as r:
        return [p for p in json.load(r) if p["type"] == "page"]


def pick(match: str) -> dict:
    for p in pages():
        if match in p["url"] or match in p.get("title", ""):
            return p
    sys.exit(f"Không có tab nào khớp '{match}'. Tab đang mở: " + "; ".join(p["url"][:60] for p in pages()))


class CDP:
    def __init__(self, page: dict):
        self.ws = websocket.create_connection(page["webSocketDebuggerUrl"], suppress_origin=True, timeout=120)
        self.n = 0

        self.events: list[dict] = []

    def call(self, method: str, **params):
        self.n += 1
        self.ws.send(json.dumps({"id": self.n, "method": method, "params": params}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == self.n:
                if "error" in msg:
                    raise RuntimeError(f"{method}: {msg['error']}")
                return msg.get("result", {})
            if "method" in msg:
                self.events.append(msg)

    def wait_event(self, name: str, timeout: float = 15.0) -> dict:
        for e in self.events:
            if e["method"] == name:
                self.events.remove(e)
                return e["params"]
        self.ws.settimeout(timeout)
        try:
            while True:
                msg = json.loads(self.ws.recv())
                if msg.get("method") == name:
                    return msg["params"]
                if "method" in msg:
                    self.events.append(msg)
        finally:
            self.ws.settimeout(120)

    def pick(self, click_js: str, files: list[str]) -> str:
        """Click something that opens a file chooser (input or showOpenFilePicker) and feed it files."""
        self.call("Page.enable")
        self.call("Page.setInterceptFileChooserDialog", enabled=True)
        try:
            self.eval(click_js)
            ev = self.wait_event("Page.fileChooserOpened")
            paths = [str(Path(f).resolve()) for f in files]
            if ev.get("backendNodeId"):
                self.call("DOM.setFileInputFiles", files=paths, backendNodeId=ev["backendNodeId"])
            else:
                self.call("DOM.setFileInputFiles", files=paths, frameId=ev.get("frameId"))
            return f"chooser {ev.get('mode')} <- {len(paths)} file"
        finally:
            self.call("Page.setInterceptFileChooserDialog", enabled=False)

    def eval(self, expr: str):
        r = self.call("Runtime.evaluate", expression=expr, awaitPromise=True, returnByValue=True)
        if "exceptionDetails" in r:
            raise RuntimeError(r["exceptionDetails"].get("exception", {}).get("description", "JS error"))
        return r.get("result", {}).get("value")

    def shot(self, out: Path, quality: int = 60) -> None:
        d = self.call("Page.captureScreenshot", format="jpeg", quality=quality)
        out.write_bytes(base64.b64decode(d["data"]))

    def nav(self, url: str) -> None:
        self.call("Page.navigate", url=url)
        time.sleep(2.5)

    def upload(self, selector: str, files: list[str]) -> None:
        doc = self.call("DOM.getDocument", depth=1)
        node = self.call("DOM.querySelector", nodeId=doc["root"]["nodeId"], selector=selector)
        if not node.get("nodeId"):
            raise RuntimeError(f"Không thấy phần tử '{selector}'")
        self.call("DOM.setFileInputFiles", files=[str(Path(f).resolve()) for f in files], nodeId=node["nodeId"])

    def drop(self, files: list[str], x_frac: float = 0.5, y_frac: float = 0.5) -> str:
        """Drop files onto the page (synthetic drag events): the only upload path that
        never opens a native file dialog. Files travel as base64 inside the script."""
        import mimetypes

        parts = []
        for f in files:
            pth = Path(f)
            mime = mimetypes.guess_type(pth.name)[0] or "application/octet-stream"
            parts.append({"name": pth.name, "type": mime, "b64": base64.b64encode(pth.read_bytes()).decode()})
        js = """(async (files, xf, yf) => {
          const sleep = ms => new Promise(r => setTimeout(r, ms));
          const dt = new DataTransfer();
          for (const f of files) {
            const bin = atob(f.b64); const u8 = new Uint8Array(bin.length);
            for (let i = 0; i < bin.length; i++) u8[i] = bin.charCodeAt(i);
            dt.items.add(new File([u8], f.name, {type: f.type}));
          }
          const x = innerWidth * xf, y = innerHeight * yf;
          let el = document.elementFromPoint(x, y) || document.body;
          let consumed = false, targets = [];
          for (const type of ["dragenter", "dragover", "dragover", "drop"]) {
            // the drop overlay only exists after dragenter: re-aim at whatever is under the pointer now
            el = document.elementFromPoint(x, y) || el;
            targets.push(el.tagName + "." + (el.className || "").toString().slice(0, 30));
            const ev = new DragEvent(type, {bubbles: true, cancelable: true, dataTransfer: dt, clientX: x, clientY: y});
            const r = el.dispatchEvent(ev);
            if (type === "drop") consumed = !r;
            await sleep(250);
          }
          return JSON.stringify({targets, consumed});
        })(%s, %s, %s)""" % (json.dumps(parts), x_frac, y_frac)
        return self.eval(js)

    def downloads(self, directory: str) -> None:
        Path(directory).mkdir(parents=True, exist_ok=True)
        self.call("Page.setDownloadBehavior", behavior="allow", downloadPath=str(Path(directory).resolve()))


def main() -> None:
    a = sys.argv[1:]
    if not a or a[0] == "pages":
        for p in pages():
            print(f"{p['title'][:50]!r:54} {p['url'][:90]}")
        return
    cmd = a[0]
    if cmd == "new":
        req = urllib.request.Request(f"http://127.0.0.1:{PORT}/json/new?{a[1]}", method="PUT")
        with urllib.request.urlopen(req) as r:
            print(json.load(r)["url"])
        return
    c = CDP(pick(a[1]))
    if cmd == "shot":
        c.shot(Path(a[2]))
        print(a[2])
    elif cmd == "eval":
        print(json.dumps(c.eval(a[2]), ensure_ascii=False))
    elif cmd == "nav":
        c.nav(a[2])
        print(c.eval("location.href"))
    elif cmd == "upload":
        c.upload(a[2], a[3:])
        print(f"đã gắn {len(a[3:])} file vào {a[2]}")
    elif cmd == "drop":
        print(c.drop(a[2:]))
    elif cmd == "pick":
        print(c.pick(a[2], a[3:]))
    elif cmd == "downloads":
        c.downloads(a[2])
        print(f"tải về -> {a[2]}")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
