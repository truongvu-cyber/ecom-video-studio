# Đèn chiếu logo cửa xe (Cubs) — prompt tạo ảnh và video

Phần mô tả, hướng dẫn và ghi chú viết bằng tiếng Việt. Phần prompt (trong khung code) và các khóa giữ bằng tiếng Anh: **copy nguyên văn, không dịch**.

| Công cụ video | Công cụ ảnh | Tỉ lệ | Độ dài | Số clip | Phong cách | Thể loại | Âm thanh |
|---|---|---|---|---|---|---|---|
| Veo 3.1 | Nano Banana Pro | 9:16 | ~15 giây, 8 nhát cắt | 4 clip × 8 giây | đêm bãi đỗ xe + garage ban ngày | reveal + hướng dẫn lắp | tắt tiếng gốc, nhạc hip-hop thêm khi dựng |

**Lưu ý chung:**
- **Logo chiếu dưới đất luôn có sẵn trong ảnh khung đầu** (lấy từ ảnh sản phẩm thật), video chỉ làm nó sáng lên, mờ đi hoặc camera di chuyển. Không để Veo tự vẽ logo từ đầu, vì nó sẽ vẽ sai chữ.
- Mỗi clip gồm **2 nửa có hành động khác nhau** (khoảng 0-4 giây và 4-8 giây); khi dựng mỗi nửa thành một nhát cắt.
- Prompt mô tả hình logo, không gọi tên đội. Xe không để lộ logo hãng.

## Các khóa (dán nguyên văn, không sửa chữ nào)

**PRODUCT (sản phẩm):**
a palm-sized matte black square projector unit with a small round lens on its underside, stuck under the inside door panel of a car; when the door is open it projects a round logo onto the ground: a blue outer ring, a thin white ring, and a red letter C wrapping the red block letters UBS on a white field, exactly as in the product photo

**CHARACTER - Mike (nhân vật):**
man in his early 40s, medium build, light skin, short dark-blond hair, light stubble, navy long-sleeve henley, dark jeans, plain navy baseball cap with no logo

**STYLE (phong cách, bối cảnh, ánh sáng — cảnh đêm):**
UGC phone footage, vertical 9:16, a quiet parking lot at night, dark textured asphalt, soft amber streetlights far in the background, a blue coupe with no visible badges or logos, natural contrast, real textures, no color grading

**STYLE - day (cảnh lắp đặt ban ngày):**
UGC phone footage, vertical 9:16, a home driveway in soft afternoon daylight, light grey concrete tiles, the same blue coupe with no visible badges or logos, natural colours, real skin and fabric texture, no color grading

**AUDIO (âm thanh):** quiet ambience, no speech, no music

**NEGATIVE (những thứ cần tránh):** subtitles, captions, on-screen text, watermark, misspelled or redrawn logo, extra logos, car brand badges, distorted hands, extra fingers, beauty filter, cinematic grading, music

## Bước 0 — Ảnh tham chiếu (làm trước mọi cảnh)

1. **Ảnh logo chiếu:** `frames/product_projection.png` — nguồn duy nhất của logo, luôn tải lên khi cảnh có logo.
2. **Ảnh hướng dẫn lắp:** `frames/install_steps_row.png` (4 ảnh thật: lắp pin, lau, bóc keo, dán) — tham chiếu hình dáng hộp đèn và tay thao tác.
3. **Ảnh nhân vật Mike:** gen một lần, dùng cho keyframe 4.
   ```
   Character reference sheet, one image, 16:9: three full-body views (front, side, back) on the left, one chest-up close-up on the right, plain light-grey background, even soft light. Man in his early 40s, medium build, light skin, short dark-blond hair, light stubble, navy long-sleeve henley, dark jeans, plain navy baseball cap with no logo. No text, no logos, no watermark.
   ```
   **Lưu thành:** `mike_sheet.png`

## Ảnh khung đầu (gen và soát xong hết mới sang video)

### Keyframe 1 · cho clip 1 · Nano Banana Pro
**Ảnh tải lên:** ảnh 1 = `product_projection.png` · **Lưu thành:** `keyframe_c1.png`

**Cảnh:** giữ nguyên cảnh trong ảnh sản phẩm (cửa xe mở, logo sáng dưới đất), chỉ mở rộng khung thành dọc 9:16.
```
Image 1 is the product photo: an open car door at night with a small black projector under the door panel shining a round logo onto the asphalt. Keep the projected logo exactly as in image 1: a blue outer ring, a thin white ring, a red letter C wrapping the red block letters UBS on a white field; same shapes, letters, colours and sharpness; do not redraw, retype or restyle it. Keep the door, the projector and the light beam as in image 1.
Extend the scene to a vertical 9:16 frame: more dark textured asphalt below the logo and more of the open door and car body above, the blue interior door light glowing, a faint beam of light from the projector to the logo.
UGC phone footage, vertical 9:16, a quiet parking lot at night, dark textured asphalt, soft amber streetlights far in the background, a blue coupe with no visible badges or logos, natural contrast, real textures, no color grading
Top-down three-quarter view, vertical 9:16, the logo in the centre of the lower half filling about half of the frame width, top 15% and bottom 20% kept clear. No people, no other text, no watermark.
```
**Soát trước khi làm video:** logo đúng hệt ảnh gốc (vòng xanh, viền trắng, chữ C đỏ ôm chữ UBS) · không có logo hãng xe

### Keyframe 2 · cho clip 2 · Nano Banana Pro
**Ảnh tải lên:** ảnh 1 = `install_steps_row.png` · **Lưu thành:** `keyframe_c2.png`

**Cảnh:** cận hai bàn tay cầm hộp đèn đen đang mở khay pin, chuẩn bị lắp viên pin cuối, xe xanh phía sau, ban ngày.
```
Image 1 shows four real install photos; use the first one as the reference for the product and the hands: a palm-sized matte black square projector unit with its battery tray open, three batteries inside. Keep the unit's shape, colour and tray exactly as in image 1; do not add text or brand marks to the unit or the batteries.
Close-up of a man's two hands in a navy long sleeve holding the unit at chest height, the right thumb pressing the last battery into the tray, a blue coupe softly out of focus behind.
UGC phone footage, vertical 9:16, a home driveway in soft afternoon daylight, light grey concrete tiles, the same blue coupe with no visible badges or logos, natural colours, real skin and fabric texture, no color grading
Close-up, vertical 9:16, the unit in the centre third, top 15% and bottom 20% kept clear. No readable brand names on the batteries, no other text, no watermark, natural hands with five fingers.
```
**Soát trước khi làm video:** tay đủ ngón, cầm tự nhiên · không có chữ thương hiệu đọc được trên pin

### Keyframe 3 · cho clip 3 · Nano Banana Pro
**Ảnh tải lên:** ảnh 1 = `install_steps_row.png`, ảnh 2 = `keyframe_c2.png` · **Lưu thành:** `keyframe_c3.png`

**Cảnh:** cận hai bàn tay đang bóc lớp màng đỏ ở mặt sau hộp đèn, cửa xe mở phía sau.
```
Image 1 shows four real install photos; use the third one as the reference: two hands peeling a red film off the adhesive pad on the back of the black projector unit. Keep the unit's shape and the red film exactly as in image 1. Image 2 is the hands, sleeve and daylight to match.
Close-up of the man's two hands holding the unit, the left fingers pinching a corner of the red film just starting to lift, the open driver's door and dark interior door panel softly behind.
UGC phone footage, vertical 9:16, a home driveway in soft afternoon daylight, light grey concrete tiles, the same blue coupe with no visible badges or logos, natural colours, real skin and fabric texture, no color grading
Close-up, vertical 9:16, the unit in the centre third, top 15% and bottom 20% kept clear. No other text, no watermark, natural hands with five fingers.
```
**Soát trước khi làm video:** tay đủ ngón · màng đỏ đang bóc ở một góc

### Keyframe 4 · cho clip 4 · Nano Banana Pro
**Ảnh tải lên:** ảnh 1 = `product_projection.png`, ảnh 2 = `mike_sheet.png`, ảnh 3 = `keyframe_c1.png` · **Lưu thành:** `keyframe_c4.png`

**Cảnh:** bãi đỗ ban đêm, Mike vừa bước ra khỏi xe, cửa mở, logo sáng dưới chân, một người bạn đi tới phía sau (mờ).
```
Image 1 is the product: keep the projected ground logo exactly as in image 1, a blue outer ring, a thin white ring, a red letter C wrapping the red block letters UBS on a white field; do not redraw or retype it. Image 2 is the man; keep his face and outfit. Image 3 is the car, asphalt and light to match.
Man in his early 40s, medium build, light skin, short dark-blond hair, light stubble, navy long-sleeve henley, dark jeans, plain navy baseball cap with no logo, standing beside the open driver's door of the blue coupe, one foot just stepped onto the asphalt, looking down at the glowing logo at his feet with a half smile; a friend walks up from behind, soft and out of focus.
UGC phone footage, vertical 9:16, a quiet parking lot at night, dark textured asphalt, soft amber streetlights far in the background, a blue coupe with no visible badges or logos, natural contrast, real textures, no color grading
Full shot from a low angle near the ground, vertical 9:16, the logo sharp in the lower third, the man and the open door above it, top 15% and bottom 20% kept clear. One person in focus, no other text, no watermark, natural hands with five fingers.
```
**Soát trước khi làm video:** logo đúng hệt ảnh gốc · không có logo hãng xe · người bạn phía sau mờ

## Clip 1 · 8s · Reveal logo
**Khung đầu:** `keyframe_c1.png` · **Lưu video thành:** `c01_a.mp4` (gen lại thì lưu `c01_b.mp4`)

**Cảnh:** nửa đầu cửa xe mở rộng thêm, chùm sáng bừng lên làm logo sáng rực; nửa sau camera đẩy chậm vào logo.
```
Top-down three-quarter view, slow push in. In the first half the open door swings a little wider and the projector beam brightens, so the logo on the asphalt glows stronger and sharper. In the second half the camera keeps moving slowly toward the logo until it fills most of the frame; the logo stays perfectly still and sharp on the ground.
Audio: quiet night ambience, no speech, no music. No subtitles, no on-screen text.
```
**Phủ định (Negative):** `subtitles, captions, on-screen text, watermark, misspelled or redrawn logo, flickering logo, extra logos, car brand badges, music`

## Clip 2 · 8s · Lắp pin → lau bề mặt
**Khung đầu:** `keyframe_c2.png` · **Lưu video thành:** `c02_a.mp4`

**Cảnh:** nửa đầu ấn viên pin cuối vào khay và đóng nắp; nửa sau camera lia sang cửa xe, tay lau mặt trong tấm ốp cửa bằng khăn microfiber xám.
```
Close-up, slow pan right. The man's thumb presses the last battery into the tray and he snaps the tray shut. Around the middle of the clip the camera pans slowly to the open car door as his other hand wipes the bottom of the inner door panel with a grey microfiber cloth in two firm strokes.
Audio: click of the battery tray, cloth on plastic, quiet driveway ambience, no speech, no music. No subtitles, no on-screen text.
```
**Phủ định (Negative):** `subtitles, captions, readable battery brand, extra fingers, distorted hands, fast motion, music`

## Clip 3 · 8s · Bóc keo → dán và đóng cửa
**Khung đầu:** `keyframe_c3.png` · **Lưu video thành:** `c03_a.mp4`

**Cảnh:** nửa đầu bóc hết lớp màng đỏ; nửa sau ấn hộp đèn vào dưới tấm ốp cửa, giữ vài giây rồi buông tay.
```
Close-up, slow tilt up. The man's fingers peel the red film off the adhesive pad in one smooth pull. Around the middle of the clip the camera tilts up to the bottom of the inner door panel as he presses the black unit firmly into place under the panel, holds it for a moment with his palm, then lets go; the unit stays stuck.
Audio: soft peel of the film, a firm press, quiet driveway ambience, no speech, no music. No subtitles, no on-screen text.
```
**Phủ định (Negative):** `subtitles, captions, extra fingers, distorted hands, unit falling, fast motion, music`

## Clip 4 · 8s · Ngoài đời → đóng cửa
**Khung đầu:** `keyframe_c4.png` · **Lưu video thành:** `c04_a.mp4`

**Cảnh:** nửa đầu Mike nhìn logo, bạn đi tới chỉ xuống đất ngạc nhiên; nửa sau Mike đóng cửa xe, logo mờ dần rồi tắt.
```
Low-angle full shot, static. The man looks down at the glowing logo and grins as his friend walks up behind him and points at it, impressed. Around the middle of the clip the man swings the car door shut and the logo on the asphalt fades out smoothly as the door closes, leaving the dark ground.
Audio: footsteps on asphalt, a car door closing, quiet night ambience, no dialogue, no music. No subtitles, no on-screen text.
```
**Phủ định (Negative):** `subtitles, captions, misspelled or redrawn logo, extra logos, car brand badges, distorted faces, extra people in focus, music`

## Thiết lập khi gen video
- Cả 4 clip: chế độ **ảnh làm khung đầu** (first frame), 8 giây, dọc 9:16, **1080p** nếu công cụ cho chọn.
- Có ô Negative thì dán dòng "Phủ định"; không có thì bỏ qua.
- Tiếng clip không dùng: video dùng nhạc hip-hop khi dựng.

Dựng: đưa clip vào `projects/cubs-car-door-light/clips/` (tên `c01_a.mp4`… hoặc để tên Veo đặt, mình tự đổi) rồi nhắn "dựng video đèn cửa xe".
