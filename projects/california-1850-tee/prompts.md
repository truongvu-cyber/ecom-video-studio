# Áo California 1850 — prompt tạo ảnh và video

Phần mô tả, hướng dẫn và ghi chú viết bằng tiếng Việt. Phần prompt (trong khung code) và các khóa giữ bằng tiếng Anh vì model hiểu tiếng Anh tốt nhất: **copy nguyên văn, không dịch**.

| Công cụ video | Công cụ ảnh | Tỉ lệ | Độ dài | Số clip | Phong cách | Thể loại | Âm thanh |
|---|---|---|---|---|---|---|---|
| Veo 3.1 | Nano Banana Pro | 9:16 | 15 giây | 4 clip × 8 giây | UGC hoàng hôn, chậm | lifestyle, lo-fi không lời | tiếng sóng/gió từ Veo, nhạc lo-fi thêm khi dựng |

## Các khóa (dán nguyên văn, không sửa chữ nào)

Khóa là đoạn mô tả cố định được lặp lại trong mọi prompt để sản phẩm, nhân vật và ánh sáng giống nhau giữa các cảnh. Các prompt bên dưới đã dán sẵn; phần này để bạn tra khi cần sửa.

**PRODUCT (sản phẩm):**
black crew-neck short-sleeve t-shirt with a large vintage front print exactly as in the product photo: the arched word CALIFORNIA in sand-cream block letters, the numbers 18 and 50 in teal on either side of an arch-shaped scene with a pale sun, birds, a curling teal wave, a beach, two palm trees and mountains, the word ORIGINAL in sand-cream block letters below, the script words Golden State in teal between two teal lines, and a small sand-cream bear icon, distressed print texture

**CHARACTER - Cole (nhân vật):**
man in his late 20s, lean athletic build, sun-tanned light skin, short messy sandy-brown hair, light stubble, faded olive board shorts, barefoot, thin black cord bracelet on the left wrist

**STYLE (phong cách, bối cảnh, ánh sáng):**
UGC phone footage, vertical 9:16, a quiet California beach at golden hour, low warm sun behind the camera's left shoulder, soft long shadows, pastel sky, gentle sea haze, natural skin texture, real fabric folds, slow calm motion, no color grading

**AUDIO (âm thanh):** gentle waves, light sea breeze, no speech, no music

**NEGATIVE (những thứ cần tránh):** subtitles, captions, on-screen text, watermark, changed or misspelled print text, extra logos, distorted print, ring light, beauty filter, cinematic grading, fast motion, speech, music

## Bước 0 — Ảnh tham chiếu (làm trước mọi cảnh)

1. **Ảnh sản phẩm:** `frames/product.jpg` (ảnh thật, vuông). Không có file thiết kế riêng nên ảnh này là nguồn duy nhất của hình in: **luôn tải lên làm ảnh 1**.
2. **Ảnh nhân vật Cole:** gen một lần, dùng cho keyframe 1, 3 và 4 để giữ khuôn mặt.
   ```
   Character reference sheet, one image, 16:9: three full-body views (front, side, back) on the left, one chest-up close-up on the right, plain light-grey background, even soft light. Man in his late 20s, lean athletic build, sun-tanned light skin, short messy sandy-brown hair, light stubble, faded olive board shorts, barefoot, thin black cord bracelet on the left wrist, wearing a plain black crew-neck t-shirt. No text, no logos, no watermark.
   ```
   **Lưu thành:** `cole_sheet.png`

## Ảnh khung đầu (gen và soát xong hết mới sang video)

### Keyframe 1 · cho clip 1 · Nano Banana Pro
**Ảnh tải lên:** ảnh 1 = `product.jpg`, ảnh 2 = `cole_sheet.png` · **Lưu thành:** `keyframe_c1.png`

**Cảnh:** Cole ngồi ở cửa sau van mở trên bãi cát, mặc áo, hình in thấy rõ trên ngực, nhìn ra biển.
```
Image 1 is the product: a black t-shirt with a vintage California print. Keep the shirt and its print exactly as in image 1: same letters, numbers, artwork, colours, size and placement; do not retype, restyle, simplify or move any part of the print. Image 2 is the man; keep his face, hair and build.
Man in his late 20s, lean athletic build, sun-tanned light skin, short messy sandy-brown hair, light stubble, faded olive board shorts, barefoot, thin black cord bracelet on the left wrist, wearing the shirt from image 1, sitting on the open back edge of a white camper van parked on sand, forearms resting on his knees, facing the camera, gazing past it toward the sea, relaxed.
UGC phone footage, vertical 9:16, a quiet California beach at golden hour, low warm sun behind the camera's left shoulder, soft long shadows, pastel sky, gentle sea haze, natural skin texture, real fabric folds, slow calm motion, no color grading
Medium shot, phone at chest height, vertical 9:16, his head at about one third of the frame height with open sky above, the whole print visible and flat on his chest in the centre of the frame, top 15% and bottom 20% kept clear. One person, no other text, no watermark, natural hands with five fingers.
```
**Soát trước khi làm video:** CALIFORNIA, 18, 50, ORIGINAL, Golden State đúng chính tả và đúng vị trí như ảnh gốc · có biểu tượng gấu · tay đủ 5 ngón · ảnh dọc 9:16

### Keyframe 2 · cho clip 2 · Nano Banana Pro
**Ảnh tải lên:** ảnh 1 = `product.jpg` · **Lưu thành:** `keyframe_c2.png`

**Cảnh:** giữ nguyên ảnh áo trải trên bàn gỗ, chỉ mở rộng khung thành dọc 9:16 và thêm vệt nắng chiều.
```
Image 1 is the product photo: a black t-shirt laid flat on a weathered wooden table with a compass, a smooth stone, a film canister, sunglasses and a bandana around it. Keep the shirt, its print and every object exactly as in image 1: same letters, numbers, artwork, colours and placement; do not retype, restyle or move anything.
Extend the same scene to a vertical 9:16 frame: more of the same wooden table above and below the shirt, the same window light from the top right, a warm golden late-afternoon tone, a soft beam of sunlight falling across the table beside the shirt.
UGC phone footage, vertical 9:16, natural texture of the wood grain and cotton, no color grading
Top-down shot, vertical 9:16, the print centred and filling about 60% of the frame width, top 15% and bottom 20% kept clear. No new objects, no extra text, no watermark.
```
**Soát trước khi làm video:** hình in giống ảnh gốc từng chữ · không có đồ vật mới trên bàn

### Keyframe 3 · cho clip 3 · Nano Banana Pro
**Ảnh tải lên:** ảnh 1 = `product.jpg`, ảnh 2 = `cole_sheet.png`, ảnh 3 = `keyframe_c1.png` · **Lưu thành:** `keyframe_c3.png`

**Cảnh:** Cole đứng ở mép sóng, chuẩn bị bước về phía camera.
```
Image 1 is the product: keep the black t-shirt and its print exactly as in image 1, same letters, numbers, artwork, colours, size and placement; do not retype, restyle or move any part of the print. Image 2 is the man; keep his face, hair and build. Image 3 is the beach and light to match.
Man in his late 20s, lean athletic build, sun-tanned light skin, short messy sandy-brown hair, light stubble, faded olive board shorts, barefoot, thin black cord bracelet on the left wrist, wearing the shirt from image 1, standing barefoot at the wet edge of the shoreline, one foot just lifting to step toward the camera, arms loose, small foam waves around his ankles.
UGC phone footage, vertical 9:16, a quiet California beach at golden hour, low warm sun behind the camera's left shoulder, soft long shadows, pastel sky, gentle sea haze, natural skin texture, real fabric folds, slow calm motion, no color grading
Full shot from slightly below knee height, vertical 9:16, his body in the centre third, print facing the camera, top 15% and bottom 20% kept clear. One person, no other text, no watermark.
```
**Soát trước khi làm video:** hình in đọc được và đúng ở cỡ nhỏ này · bàn chân, bàn tay bình thường · cùng bãi biển với keyframe 1

### Keyframe 4 · cho clip 4 · Nano Banana Pro
**Ảnh tải lên:** ảnh 1 = `product.jpg`, ảnh 2 = `cole_sheet.png`, ảnh 3 = `keyframe_c1.png` · **Lưu thành:** `keyframe_c4.png`

**Cảnh:** Cole tựa vai vào thành van, nhìn ra biển, ngay trước khi quay lại nhìn camera. Nửa dưới khung để trống cho nút CTA.
```
Image 1 is the product: keep the black t-shirt and its print exactly as in image 1, same letters, numbers, artwork, colours, size and placement; do not retype, restyle or move any part of the print. Image 2 is the man; keep his face, hair and build. Image 3 is the van, beach and light to match.
Man in his late 20s, lean athletic build, sun-tanned light skin, short messy sandy-brown hair, light stubble, faded olive board shorts, barefoot, thin black cord bracelet on the left wrist, wearing the shirt from image 1, leaning his shoulder against the side of the white camper van, looking out at the sea in profile, just before he turns to the camera.
UGC phone footage, vertical 9:16, a quiet California beach at golden hour, low warm sun behind the camera's left shoulder, soft long shadows, pastel sky, gentle sea haze, natural skin texture, real fabric folds, slow calm motion, no color grading
Medium shot, vertical 9:16, his head at about one third of the frame height, the print visible on his chest, the lower third of the frame calm and uncluttered for the call-to-action button, top 15% and bottom 20% kept clear. One person, no other text, no watermark, natural hands with five fingers.
```
**Soát trước khi làm video:** hình in đúng · phần dưới khung thoáng · cùng van và ánh sáng với keyframe 1

## Clip 1 · 8s · Mở đầu (hook)
**Khung đầu:** `keyframe_c1.png` · **Lưu video thành:** `c01_a.mp4` (gen lại thì lưu `c01_b.mp4`)

**Cảnh:** Cole từ từ ngả người ra sau, hít một hơi, nhìn biển. Áo luôn phẳng và hướng về camera.
```
Medium shot, static with a gentle handheld drift. The man sitting on the van's open back slowly leans back on his hands, takes a calm breath and lets his gaze rest on the sea; the shirt stays smooth and facing the camera. Warm golden hour light from the left, sea haze in the background.
Audio: gentle waves, light sea breeze, no speech, no music. No subtitles, no on-screen text.
```
**Phủ định (Negative):** `subtitles, captions, on-screen text, watermark, changed or misspelled print text, distorted print, fast motion, speech, music`

## Clip 2 · 8s · Cận hình in
**Khung đầu:** `keyframe_c2.png` · **Lưu video thành:** `c02_a.mp4`

**Cảnh:** camera đẩy rất chậm vào hình in, vệt nắng trôi qua bàn. Hình in đứng yên, không gấp nếp.
```
Top-down shot, very slow push in toward the centre of the print. The beam of warm sunlight drifts slowly across the wooden table and over the edge of the shirt; nothing else moves, the print stays flat and still. Soft window light from the top right.
Audio: distant waves through an open window, light breeze, no speech, no music. No subtitles, no on-screen text.
```
**Phủ định (Negative):** `subtitles, captions, changing letters, extra text, folds over the print, camera rotation, new objects, music`

## Clip 3 · 8s · Lifestyle
**Khung đầu:** `keyframe_c3.png` · **Lưu video thành:** `c03_a.mp4`

**Cảnh:** Cole đi chân trần thong thả dọc mép sóng về phía camera, nắng ngược viền tóc, dừng lại cách ống kính vài bước.
```
Full shot from low height, static, slow motion feel. The man walks barefoot along the wet shoreline toward the camera at an easy, unhurried pace, small waves washing over his feet, his arms swinging loosely; golden backlight rims his hair. He stops a few steps from the lens.
Audio: waves washing in, footsteps in wet sand, light breeze, no speech, no music. No subtitles, no on-screen text.
```
**Phủ định (Negative):** `subtitles, captions, on-screen text, distorted print, misspelled print text, running, fast motion, extra people, music`

## Clip 4 · 8s · Kêu gọi mua (CTA)
**Khung đầu:** `keyframe_c4.png` · **Lưu video thành:** `c04_a.mp4`

**Cảnh:** Cole từ từ quay đầu từ biển sang camera, gật nhẹ, cười. Nắng loé nhẹ ở mép khung. Nút CTA sẽ được thêm khi dựng.
```
Medium shot, static. The man leaning on the van slowly turns his head from the sea to the camera, gives a small relaxed nod and a warm smile, then holds the look. The low sun flares softly at the edge of the frame; the shirt stays facing the camera.
Audio: gentle waves, light sea breeze, no speech, no music. No subtitles, no on-screen text.
```
**Phủ định (Negative):** `subtitles, captions, on-screen text, watermark, changed or misspelled print text, distorted print, fast motion, speech, music`

## Thiết lập khi gen video
- Chế độ: **ảnh làm khung đầu** (first frame / image-to-video), 8 giây, dọc 9:16, 1080p.
- Ô Negative của công cụ: dán dòng "Phủ định" của clip đó. Không có ô Negative thì bỏ qua (prompt đã ghi sẵn các thứ cần tránh).

Dựng: đưa clip vào `projects/california-1850-tee/clips/` rồi nhắn "dựng video cali".
