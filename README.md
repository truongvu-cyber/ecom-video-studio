# ecom-video-studio

Hai agent làm video quảng cáo ecommerce (POD customize, dropshipping), chạy trong tab Code của app Claude desktop.

- **Agent 1 · Creative** (`.claude/skills/ad-creative`): sản phẩm → `product.json` (Product Truth) → concept (dừng chờ duyệt) → prompt ảnh khung đầu (Nano Banana 2.1) + prompt clip (Omni 1.1 Flash, chế độ Thành phần, trong Google Flow) + `production.json`.
- **Agent 2 · Editor** (`.claude/skills/ad-editor`): clip 8 giây từ Flow → chọn take, cắt theo lời thoại + beat, hạ nhạc, phụ đề, CTA → MP4 9:16 (có nhạc + không nhạc) + `edit-report.md`.

## Cấu trúc

```
schemas/        production.schema.json, product.schema.json
scripts/        script Python Agent 2 gọi (chạy bằng .venv/bin/python)
brand/          brand.json, logo, font
music-library/  nhạc tải về CHỈ DÙNG NỘI BỘ (chưa có license đăng quảng cáo) + tags.json
projects/<id>/  refs/ frames/ clips/ edit/ out/ + product.json, brief.md, prompts.md, production.json
```

## Môi trường

- Python 3.12 trong `.venv` (tạo bằng `uv venv --python 3.12 .venv && uv pip install --python .venv/bin/python -r pyproject.toml`)
- FFmpeg 8.1, Node, Chrome (có sẵn)
- HyperFrames: `npx hyperframes@0.8.186`
- `/watch` (bradautomates/claude-video): cài qua Customize → Plugins trong app, chạy chế độ local

## Chạy Agent 1 (Creative)

Trong tab Code, nói với Claude (skill `ad-creative` tự kích hoạt), ví dụ: "Lên ý tưởng video cho sản phẩm này, ảnh ở projects/abc/frames/product.jpg". Agent dừng chờ duyệt story draft trước khi viết prompt.

```bash
.venv/bin/python scripts/analyze_ref.py <project-id> refs/<video>.mp4   # mode C: mổ xẻ video mẫu
.venv/bin/python scripts/creative_check.py <project-id>                 # kiểm tra prompts.md + production.json trước khi gen
```

Ví dụ đầy đủ một lần chạy: `projects/cubs-car-door-light/` trong git (brief.md, product.json, prompts.md, production.json, format `demo_steps`).

## Gen tự động trong Google Flow

```bash
scripts/flow_chrome.sh                                                   # Chrome riêng, đăng nhập Google một lần
.venv/bin/python scripts/gen_queue.py <project-id>                       # hàng đợi gen từ prompts.md
.venv/bin/python scripts/flow_run.py <project-id>                        # (tự chạy creative_check trước, FAIL là dừng) cả hàng đợi: upload 1 lượt, gen song song (4), clip chạy ngay khi keyframe về
.venv/bin/python scripts/flow_run.py <project-id> --stage images         # chỉ ảnh (soát xong mới --stage clips); --serial = từng job một
.venv/bin/python scripts/gen_review.py <project-id>                      # edit/qc/gen_review.jpg + danh sách soát vị trí sản phẩm
.venv/bin/python scripts/gen_review.py <project-id> --mark c03 fail "…"  # ghi kết quả soát; clip chưa 'pass' thì validate chặn
.venv/bin/python scripts/flow_run.py <project-id> --stage clips          # clip Omni 1.1 Flash, tải 1080p vào clips/
```

Chrome riêng phải mở suốt lúc chạy (runner điều khiển cửa sổ đó qua DevTools; đóng là dừng). Quy trình click-by-click và các điều kiện dừng: `.claude/skills/ad-creative/references/flow-runbook.md`.

## Chạy Agent 2 (Editor)

```bash
.venv/bin/python scripts/edit_pipeline.py <project-id>                  # validate → inspect → transcribe → beats → timeline → plan → render → qc
.venv/bin/python scripts/edit_pipeline.py <project-id> --from timeline --to plan  # vài giây: kế hoạch + edit/qc/plan.jpg, chưa render
.venv/bin/python scripts/edit_pipeline.py <project-id> --from timeline  # sau khi sửa production.json: chỉ bản chính (~1 phút)
.venv/bin/python scripts/edit_pipeline.py <project-id> --from timeline --final  # khi chốt: thêm các biến thể hook
.venv/bin/python tests/make_fixtures.py                                 # tạo project giả demo-hoodie để test
.venv/bin/python tests/fake_clips.py <project-id>                       # clip giả theo production.json (test nối Agent 1 → 2)
ALLOW_TEST_MUSIC=1 .venv/bin/python scripts/edit_pipeline.py <id>       # cho phép nhạc test tổng hợp (không dùng cho quảng cáo thật)
.venv/bin/python scripts/fetch_music.py "chill lofi surf" --count 3     # tự tìm + tải nhạc (nội bộ), ghi vào music-library/tags.json
.venv/bin/python scripts/fetch_music.py --url <link> --mood "lofi"     # tải một bài cụ thể
```

Kết quả: `out/final_<id>.mp4`, `out/final_<id>_no-music.mp4`, `out/final_<id>_<variant>.mp4` (biến thể hook), `out/edit-report.md`, ảnh kiểm tra `edit/qc/sheet.jpg`.

Các bước: validate → inspect (chọn take) → takes (ảnh từng giây của mọi clip) → moments (đo chuyển động, tìm lúc đổi hành động) → transcribe → beats → timeline → plan (tấm soát `edit/qc/plan.jpg` trước khi render) → render (tự lưu bản cũ vào `out/vN/`, tự xuất `preview_*`) → qc. Duyệt: `.venv/bin/python scripts/approve.py <project-id>`.

Mỗi project thuộc một `format` cố định (`ugc_dialogue`, `hype_montage`, `calm_lofi`, `demo_steps`, xem `.claude/skills/ad-creative/references/formats.md`); `creative_check.py` kiểm tra các trường dựng khớp preset.

Trường điều khiển dựng trong `production.json` (xem `schemas/production.schema.json`): `shots[].moment` (`a`/`b`/`peak`/`calm`), `shots[].speed` (slow-mo 0.6–0.8), `shots[].overlay_pos` (`auto` tự tránh mặt/sản phẩm), `fx` (`hype` + `sfx`), `music.drop_on`, `variants` (3 hook để A/B).

Tư duy chuyên gia nằm trong `.claude/skills/ad-creative/references/viral-playbook.md` (viết) và `.claude/skills/ad-editor/references/editing-playbook.md` (dựng).

## Quy ước clip

Đặt tên clip theo shot và take: `clips/c01_a.mp4`, `clips/c01_b.mp4`. Lời thoại gom vào một clip 8 giây; nhiều shot có thể dùng chung clip đó.

## Giới hạn hiện tại

- Chỉ chạy trên macOS (font hệ thống, `say`, mlx-whisper cho Apple Silicon), một người dùng, một máy.
- `flow_run.py` điều khiển giao diện web Google Flow; Flow đổi giao diện là runner phải sửa (xem `flow-runbook.md`).
- Test: `.venv/bin/python -m unittest discover tests -v` (khoảng 90 giây; dựng project giả rồi kiểm tra nhát cắt đúng khung, hiệu ứng đúng khung, chọn take, độ to âm thanh, cổng schema và cổng creative_check). Chưa có test cho runner Flow và cho `creative_check` trên prompt thật; chưa có CI.
