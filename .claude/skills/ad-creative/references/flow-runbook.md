# Flow runbook — generating a project's images and clips in Google Flow by script

Everything below was measured on flow.google.com on 2026-10-27 (Vietnamese UI,
Ultra plan). It is the fixed procedure; a step not listed here is not done.

## 0. Browser

- `scripts/flow_chrome.sh` launches a dedicated Chrome profile
  (`~/Library/Application Support/ecom-video-studio-chrome`) with a DevTools
  port (9222) and **no automation flags**. Google refuses sign-in in a Chrome
  launched with automation flags ("Trình duyệt hoặc ứng dụng này có thể không
  an toàn"); this profile signs in normally and stays signed in.
- The user signs in themselves, once. The agent never types credentials.
- `scripts/cdp.py` drives that Chrome (tabs, screenshot, JS, navigate, drop
  files, intercept file chooser, download directory). Prefer `cdp.py` calls
  and the Python `CDP` class over any hand clicking; every step is then a
  logged command.

## 1. Settings fixed by the user (2026-10-27)

| what | setting in Flow | cost shown |
| --- | --- | --- |
| images (character sheet, keyframes) | **Nano Banana 2.1**, mode Hình ảnh, 9:16 (16:9 for the sheet), x1 | — |
| clips | **Omni 1.1 Flash**, mode **Thành phần** (ingredients), 9:16, 8 giây, x1 | 12 tín dụng |
| not used | Veo 3.1 Quality (100 tín dụng/clip, first-frame mode) — tested once on cubs c01 | |
| downloads | image **2K** (upscaled, free), video **1080p** (upscaled, free). **Never pick an option that shows "tín dụng"** (4K video = 50 credits) | |

`scripts/gen_queue.py` writes these into `edit/gen_queue.json`; the runner only
executes what the queue says.

## 2. Job order (from gen_queue.json)

1. Character sheet (if any) → download 2K → `frames/<name>_sheet.png`.
2. Keyframes in order; each is checked against its `checks` list before the
   next job (print letters, no extra badges, hands). A failed check uses the
   retry budget (`retry_budget`, 2 per project); when it is spent, stop and
   report.
3. Clips, one per keyframe, ingredients = keyframe + product photo (+ design
   file) → download 1080p → `clips/cNN_a.mp4` (retry `_b`).
4. Hand over to ad-editor (`edit_pipeline.py`).

## 3. UI facts (Vietnamese labels) and the exact mechanics

| step | how | notes |
| --- | --- | --- |
| new project | home → button text `Dự án mới` (JS click works) | URL becomes `/project/<id>` |
| project title | `input[aria-label="Văn bản có thể chỉnh sửa"]` in the header | this is NOT the prompt box; set it to the project id |
| prompt box | `.ProseMirror` (contenteditable) | the only `textarea` on the page is reCAPTCHA's, never type there. Type with `Input.insertText` after `focus()`; `execCommand('insertText')` also works |
| upload a reference | `cdp.py drop <match> <file>`: synthetic drag events on the page centre, re-aimed at the drop overlay after `dragenter` | the "Tải nội dung" button opens a native file dialog the script cannot drive; `Page.fileChooserOpened` never fires for it |
| attach a reference to the prompt | `+` button (`aria-label` "Thêm thành phần vào ô nhập câu lệnh") → panel → click the tile → button `Thêm vào câu lệnh` | the chip appears as an `img` inside the composer |
| settings popup | the chip `button.settings-trigger…` ("Video · 720p · 8 giây…"): **JS `.click()`** opens it; options are plain buttons with `aria-checked`; the model dropdown is a button containing `arrow_drop_down`, options are `[role=option]` text like "Veo 3.1 - Quality" (strip the leading `volume_up`) | the dropdown is a toggle: read the overlay text first, click it only if the options are not already listed |
| generate | button `aria-label="Bắt đầu tạo"` needs a **real mouse click** (`Input.dispatchMouseEvent` at its rect centre); JS `.click()` does nothing | |
| done detection | a new `https://flow-content.google/image/…` (image, ~30 s) or `/video/…` (video, ~2 min) URL appears among `img`/`video` sources; the `%` text is the upload tile's "100%", not progress | do not wait for a `<video>` tag, it mounts late |
| tile actions | hover the tile (`Input.dispatchMouseEvent mouseMoved`, move away first), then `aria-label="Tuỳ chọn khác"` → menu: `Tạo ảnh động` (animate image = first-frame video composer), `Thêm vào câu lệnh`, `Tải xuống` → submenu `1K Kích thước gốc` / `2K` / `4K` for images, `720p` / `1080p` / `4K · 50 tín dụng` for videos | clicking the tile image itself opens the detail view (`/edit/<id>`), which has `aria-label="Tải nội dung nghe nhìn xuống"` and `Đã chỉnh sửa xong` to close |
| download | `cdp.py downloads <match> <dir>` first (`Page.setDownloadBehavior`), then the menu; file lands as `<prompt title>_<size>_<timestamp>.<ext>`; wait for it, verify size with `sips`/`ffprobe`, then copy to the queue's `save_as` | 2K images ≈ 1536×2752 jpg; 1080p video ≈ 1080×1920 24 fps |

## 3b. Lessons from the first scripted runs (2026-10-27)

- Images cost **0 tín dụng** on Ultra; Omni 1.1 Flash clips 12; Veo 3.1 Quality 100; the 4K video
  download is 50 — the runner only ever picks free download sizes.
- Popovers (settings, media panel) are closed by a **real mouse click in the gutter** between
  the sidebar and the grid (x≈240, y≈480). Escape and JS clicks leave them open, and an open
  popover swallows every later hover/click (menus "do not open").
- The media panel mounts asynchronously: poll for the search box after clicking `+`;
  clear the search box (⌘A) before typing a new name.
- An upload can take over a minute to show up in the panel; the runner waits, then retries.
- Baseline the media URLs ~3 s after the last upload and accept a "new" URL only after a minimum
  wait (15 s images, 40 s videos): freshly uploaded tiles mount late and look like results.
- Never overwrite a clip or keyframe: `cNN_a` taken → `_b`, `_c` …; the Editor's take picker
  decides which one is used.
- Video done-detection goes by **media id**, not URL kind: finished video tiles show a poster
  `/image/<same id>`; a result counts when a new id of the right kind appears and no "NN%" text is
  left in the grid (the earlier `/video/` check generated c01 and c02 twice, 24 credits lost).
- Omni 1.1 Flash in ingredients mode can **swap the print** even with the keyframe attached:
  cubs c04 came back projecting a VW logo instead of the Cubs logo. Every clip with a print is
  checked frame by frame (`takes_sheet.py` / `edit/qc/sheet.jpg`) before it is used; a wrong
  print = retry with the product photo first in the ingredients and the print named in the prompt.
- `scripts/flow_run.py <project> --stage images` then review `frames/`, then `--stage clips`;
  `--only id,id` reruns single jobs, `--dry-run` fills the composer without generating.

## 4. Stop conditions

Stop and report (never retry blindly): a sign-in or captcha page; a refusal
("không thành công", policy text); the retry budget spent; a download that
does not arrive within 3 minutes; any option whose label contains "tín dụng"
being the only way forward.

## 5. Log

Each run appends to `edit/gen_log.jsonl`: job id, attempt, settings, result
URL, downloaded file, check result. The user reads credits spent from this
log, not from memory.
