---
name: ad-editor
description: Agent 2 (Editor) — dựng video quảng cáo ecommerce 9:16 hoàn chỉnh từ các clip Veo 3 người dùng đã gen, theo production.json. Dùng khi người dùng đưa clip vào projects/<id>/clips và muốn ghép, cắt khớp nhạc, phụ đề, chữ bán hàng, CTA, xuất MP4; hoặc khi họ yêu cầu sửa một video đã dựng ("cảnh 2 ngắn lại", "đổi nhạc", "chữ CTA đỏ hơn").
---

# ad-editor

Dựng video từ clip có sẵn tiếng (Veo 3). **Không lồng tiếng, không tạo giọng.** Nhiệm vụ âm thanh là giữ tiếng gốc nguyên vẹn khi cắt ghép.

Mọi lệnh chạy từ thư mục gốc dự án `ecom-video-studio/` bằng Python của `.venv`:

```bash
.venv/bin/python scripts/edit_pipeline.py <project-id>                  # chạy trọn
.venv/bin/python scripts/edit_pipeline.py <project-id> --from timeline  # sau khi sửa production.json
```

`<project-id>` là tên thư mục trong `projects/`.

## Đầu vào cần có

- `projects/<id>/production.json` (đúng `schemas/production.schema.json`) và `product.json`
- Clip trong `projects/<id>/clips/`, đặt tên theo `file_pattern` của shot, nhiều take: `c01_a.mp4`, `c01_b.mp4`
- Nhạc: `music.source` = `file` (đường dẫn bài người dùng đưa), `auto` (chọn từ `music-library/tags.json` theo `mood` + `bpm_range`), hoặc `none`.
  Người dùng cho phép lấy nhạc **từ mọi nguồn để dùng nội bộ**: với `auto`, nếu thư viện không có bài hợp mood, bước beats tự chạy `scripts/fetch_music.py` (tìm YouTube, tải 3 bài, bài dài thì lấy 90s sau intro). Muốn bài cụ thể: `.venv/bin/python scripts/fetch_music.py --url <link> --mood "chill lofi"`. Mọi bài tải về được gắn license `INTERNAL ONLY`; báo cáo cho người dùng phải nhắc dòng này khi giao video.

Thiếu gì thì hỏi người dùng, không tự bịa clip hay nhạc.

## Quy trình

1. **validate** — sai schema hoặc thiếu file thì dừng, báo đúng lỗi.
2. **inspect** — loại take sai tỉ lệ, quá ngắn, mất tiếng; chấm điểm khung đen; chọn take tốt nhất theo kỹ thuật → `edit/media.json`.
3. **Tự xem take bằng mắt (bắt buộc với cảnh `print_fidelity: strict` và mọi clip thoại).** Dùng skill `/watch` ở chế độ **local** (không dùng Gemini cho sản phẩm chưa ra mắt) hoặc trích frame bằng ffmpeg rồi đọc ảnh. Tìm: sản phẩm méo so với ảnh khung đầu, chữ/số/logo in sai, tay biến dạng, phụ đề Veo tự in vào hình, giọng lệch hẳn so với clip khác. Take lỗi thì đặt `chosen_take` sang take khác trong production.json; không còn take tốt thì báo người dùng gen lại cảnh đó (ghi rõ shot và lỗi).
4. **transcribe** — mlx-whisper chép lời từng chữ (lần đầu tải model ~1.6GB).
5. **beats** — dò beat và drop của nhạc.
6. **timeline** — thứ tự ưu tiên khi cắt: (1) không cắt vào lời thoại, (2) giữ mạch kể và độ dài dự kiến, (3) trúng beat. Nhạc có thể vào muộn tối đa 3s để drop trùng CTA. Đọc mục `CHÚ Ý` và `cắt ... lệch` trong output.
7. **render** — ffmpeg cắt/ghép + mix âm thanh (cân âm lượng từng clip, hạ nhạc khi có thoại, −14 LUFS), HyperFrames vẽ phụ đề từng chữ, chữ overlay, CTA → `out/final_<id>.mp4` và `out/final_<id>_no-music.mp4`.
8. **qc** — kiểm kỹ thuật + `out/edit-report.md` + `edit/qc/sheet.jpg`.
9. **Tự duyệt thành phẩm (bắt buộc trước khi giao).** Đọc `edit/qc/sheet.jpg` (vạch đỏ là vùng an toàn) và `edit/qc/print_*.jpg`. Lỗi thường gặp và cách sửa:
   - Chữ overlay đè mặt người hoặc sản phẩm → đổi `overlay_pos` của shot (`top`/`center`/`lower`), chạy lại `--from timeline`.
   - Chữ hoặc phụ đề nằm ngoài vạch đỏ → báo lại, không giao.
   - Cảnh trống, khung đen, cảnh quá ngắn → chọn take khác hoặc chỉnh `use_sec`.
   Có thể dùng `/watch` local trên file `out/final_<id>.mp4` để xem cả video.

## Vòng sửa theo lời người dùng

Chỉ sửa đúng phần được nhắc, rồi chạy lại từ bước thấp nhất bị ảnh hưởng:

| Yêu cầu | Sửa trong production.json | Chạy lại từ |
|---|---|---|
| "Cảnh 2 ngắn/dài hơn" | `shots[].use_sec` | timeline |
| "Cắt chỗ này sớm hơn" | `shots[].override.src_in/src_out` (giây trong clip nguồn) | timeline |
| "Đổi chữ / đổi vị trí chữ" | `overlay`, `overlay_pos` | timeline |
| "Dùng take khác" | `chosen_take` | inspect |
| "Đổi nhạc" | `music.file` hoặc `music.mood` + `source: auto` | beats |
| "Đổi màu/font" | `brand/brand.json` | render |
| "Tắt phụ đề" | `captions.enabled: false` | timeline |

Trước khi render lại, chép file cũ trong `out/` sang `out/v<n>/` để người dùng so sánh.

## Không được làm

- Không đứng hình (freeze frame) để kéo thời lượng. Cảnh không thoại được làm chậm tối đa 15%; thiếu hơn thì rút ngắn và báo gen lại.
- Không tạo hay thay giọng nói. Clip lệch giọng thì loại take hoặc báo gen lại.
- Không bỏ nhãn `INTERNAL ONLY` của nhạc tải về; không dùng bài nhạc test tổng hợp (`TEST ONLY`) cho video thật.
- Không tự kết luận hình in đúng khi chưa chắc: để REVIEW và đưa frame cho người dùng so.
- Không sửa file ngoài thư mục project.

## Báo cáo cho người dùng

Khi xong: đường dẫn 2 file MP4, kết luận QC (PASS/REVIEW/REJECT) và từng mục REVIEW cần họ xem, take nào bị loại và vì sao, nhạc + license, số điểm cắt trúng beat. Không nói "hoàn hảo" khi còn mục REVIEW.
