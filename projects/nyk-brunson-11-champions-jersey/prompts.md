# Áo jersey New York Brunson #11 Champions — prompt tạo ảnh và video

Phần mô tả, hướng dẫn và ghi chú viết bằng tiếng Việt. Phần prompt (trong khung code) và các khóa giữ bằng tiếng Anh: **copy nguyên văn, không dịch**.

| Công cụ video | Công cụ ảnh | Tỉ lệ | Độ dài | Số clip | Phong cách | Thể loại | Âm thanh |
|---|---|---|---|---|---|---|---|
| Veo 3.1 | Nano Banana Pro | 9:16 | ~15 giây, 8 nhát cắt | 4 clip × 8 giây | phố New York đêm, neon, ánh vàng | hype montage | tắt tiếng gốc, nhạc rap thêm khi dựng |

**Lưu ý chung:**
- **Bản sửa 26/10:** lần gen đầu Veo từ chối clip 1 vì "có thể liên quan đến người nổi tiếng". Nguyên nhân khả dĩ: nhân vật nam cao, thể hình vận động viên, mặc áo số 11 có tên cầu thủ trông giống chính cầu thủ đó. Đã đổi nhân vật thành **Maya — một nữ fan mặc áo oversize kiểu streetwear**, và bỏ cảnh úp rổ (thay bằng ném rổ thường). Cần gen lại ảnh nhân vật, keyframe 1, 2, 4 và clip 1, 2, 4.
- Mỗi clip được viết thành **2 nửa có hành động khác nhau** (khoảng 0-4 giây và 4-8 giây). Khi dựng, mỗi nửa thành một nhát cắt riêng. Nếu clip gen ra làm hành động đổi muộn hoặc sớm hơn, không sao: Agent 2 sẽ xem và chọn lại điểm cắt.
- Prompt mô tả hình dáng logo, không gọi tên thương hiệu. Logo thật đi vào hình qua ảnh sản phẩm.
- Cúp vàng và huy hiệu "2025-26 Champions" lớn ở góc dưới ảnh sản phẩm là **hình minh hoạ**, không gắn trên áo. Khi soát keyframe, xem kỹ không có huy hiệu lớn nào bị gắn lên vạt áo.

## Các khóa (dán nguyên văn, không sửa chữ nào)

**PRODUCT (sản phẩm):**
white sleeveless basketball jersey with blue and orange striped trim at the neck and armholes, the words NEW YORK in gold block letters with a thin blue outline across the chest, a large gold number 11 below, a small blue check-shaped logo on the wearer's right chest, a small gold trophy patch on the wearer's left chest, and on the back the name BRUNSON in gold letters arched above a large gold number 11 with a small round gold patch below the collar

**CHARACTER - Maya (nhân vật):**
woman in her early 20s, slim build, light tan skin, long straight black hair in a high ponytail, small gold hoop earrings, the jersey worn oversized as a dress over black bike shorts, white high-top sneakers

**STYLE (phong cách, bối cảnh, ánh sáng):**
UGC phone footage, vertical 9:16, a New York street at night, wet asphalt reflecting red and blue neon signs, steam rising from a street vent, warm sodium streetlights, high contrast, natural skin texture, real fabric folds, no color grading

**AUDIO (âm thanh):** city street ambience, distant traffic, no speech, no music

**NEGATIVE (những thứ cần tránh):** subtitles, captions, on-screen text, watermark, misspelled name or numbers, large badges sewn on the front panel, floating patches, distorted logos, readable store signs, extra people in focus, beauty filter, slow motion blur on the lettering, music

## Bước 0 — Ảnh tham chiếu (làm trước mọi cảnh)

1. **Ảnh sản phẩm:** `frames/product.png`. Có cả mặt sau (bên trái) và mặt trước (bên phải): **luôn tải lên làm ảnh 1**.
2. **Ảnh nhân vật Maya:** gen một lần, dùng cho keyframe 1, 2 và 4.
   ```
   Character reference sheet, one image, 16:9: three full-body views (front, side, back) on the left, one chest-up close-up on the right, plain light-grey background, even soft light. Woman in her early 20s, slim build, light tan skin, long straight black hair in a high ponytail, small gold hoop earrings, black bike shorts, white high-top sneakers, wearing a plain oversized white tank dress. No text, no logos, no watermark.
   ```
   **Lưu thành:** `maya_sheet.png`

## Ảnh khung đầu (gen và soát xong hết mới sang video)

### Keyframe 1 · cho clip 1 · Nano Banana Pro
**Ảnh tải lên:** ảnh 1 = `product.png`, ảnh 2 = `maya_sheet.png` · **Lưu thành:** `keyframe_c1.png`

**Cảnh:** Maya mặc áo (kiểu váy oversize) đứng giữa phố New York đêm, đèn neon phản chiếu mặt đường ướt, chuẩn bị bước về phía camera, góc máy thấp.
```
Image 1 is the product: a white basketball jersey, shown from the back on the left and the front on the right. The large gold trophy and round champions badge at the bottom of image 1 are only reference callouts; do not place them on the jersey. Keep the jersey exactly as in image 1: same gold lettering, numbers, trim, patches and placement; do not retype, restyle or move anything. Image 2 is the woman; keep her face, hair and build.
Woman in her early 20s, slim build, light tan skin, long straight black hair in a high ponytail, small gold hoop earrings, the jersey worn oversized as a dress over black bike shorts, white high-top sneakers, wearing the jersey from image 1, standing in the middle of the street facing the camera, one foot forward about to walk, arms loose, confident look.
UGC phone footage, vertical 9:16, a New York street at night, wet asphalt reflecting red and blue neon signs, steam rising from a street vent, warm sodium streetlights, high contrast, natural skin texture, real fabric folds, no color grading
Full shot from a low angle at knee height, vertical 9:16, her head at about one quarter of the frame height, the whole front of the jersey visible, top 15% and bottom 20% kept clear. One person in focus, no readable signs, no other text, no watermark, natural hands with five fingers.
```
**Soát trước khi làm video:** chữ NEW YORK, số 11 vàng viền xanh đúng · patch cúp nhỏ ở ngực trái · không có huy hiệu lớn trên vạt áo · tay đủ 5 ngón

### Keyframe 2 · cho clip 2 · Nano Banana Pro
**Ảnh tải lên:** ảnh 1 = `product.png`, ảnh 2 = `maya_sheet.png`, ảnh 3 = `keyframe_c1.png` · **Lưu thành:** `keyframe_c2.png`

**Cảnh:** cùng con phố, Maya đứng quay lưng về camera, tóc vén sang một bên, "BRUNSON 11" chiếm giữa khung.
```
Image 1 is the product: keep the back of the white jersey exactly as in image 1, the name BRUNSON in gold letters arched above a large gold number 11, same letters, spacing, outline and colours; do not retype, restyle or move them, and do not place the reference callout badges on it. Image 2 is the woman; keep her hair and build. Image 3 is the street and light to match.
Woman in her early 20s, slim build, light tan skin, long straight black hair in a high ponytail, small gold hoop earrings, the jersey worn oversized as a dress over black bike shorts, white high-top sneakers, wearing the jersey from image 1, standing still with her back to the camera, looking down the street, ponytail over one shoulder pulled to the front, shoulders relaxed, fabric smooth across the name and number.
UGC phone footage, vertical 9:16, a New York street at night, wet asphalt reflecting red and blue neon signs, steam rising from a street vent, warm sodium streetlights, high contrast, natural skin texture, real fabric folds, no color grading
Medium shot from behind at shoulder height, vertical 9:16, the name and number centred and filling about half of the frame width, top 15% and bottom 20% kept clear. One person in focus, no readable signs, no other text, no watermark.
```
**Soát trước khi làm video:** B-R-U-N-S-O-N đúng chính tả · số 11 đúng kiểu chữ · vải phẳng qua chữ

### Keyframe 3 · cho clip 3 · Nano Banana Pro
**Ảnh tải lên:** ảnh 1 = `product.png`, ảnh 2 = `keyframe_c1.png` · **Lưu thành:** `keyframe_c3.png`

**Cảnh:** cận ngực áo đang mặc dưới đèn đường: chữ NEW YORK vàng ở trên, patch cúp vàng bên cạnh, số 11 ở mép dưới.
```
Image 1 is the product: keep the gold NEW YORK lettering with its thin blue outline, the small gold trophy patch and the gold number 11 exactly as in image 1: same letters, shapes, colours and placement; do not redraw or restyle them. The large badges at the bottom of image 1 are only reference callouts. Image 2 is the woman, street and light to match.
Close-up of the chest of the white jersey worn by the woman, the gold NEW YORK lettering across the upper part of the frame, the small gold trophy patch on the wearer's left chest, the top of the gold number 11 at the bottom edge, fabric smooth, red and blue neon reflections on the white fabric.
UGC phone footage, vertical 9:16, warm sodium streetlights, high contrast, real fabric folds, no color grading
Macro close-up, straight-on, vertical 9:16, the lettering filling about 80% of the frame width, top 15% and bottom 20% kept clear. No other text, no watermark.
```
**Soát trước khi làm video:** chữ NEW YORK, cúp và số 11 đúng như ảnh gốc · chữ sắc nét

### Keyframe 4 · cho clip 4 · Nano Banana Pro
**Ảnh tải lên:** ảnh 1 = `product.png`, ảnh 2 = `maya_sheet.png` · **Lưu thành:** `keyframe_c4.png`

**Cảnh:** sân bóng rổ ngoài trời ban đêm, đèn pha, hàng rào lưới, Maya mặc áo đang cầm bóng chuẩn bị ném, vài người bạn mờ phía sau.
```
Image 1 is the product: keep the jersey exactly as in image 1, same gold lettering, numbers, trim and patches; do not retype, restyle or move anything, and do not place the reference callout badges on it. Image 2 is the woman; keep her face, hair and build.
Woman in her early 20s, slim build, light tan skin, long straight black hair in a high ponytail, small gold hoop earrings, the jersey worn oversized as a dress over black bike shorts, white high-top sneakers, wearing the jersey from image 1, standing at the top of the key on an outdoor basketball court at night, holding a basketball at her right hip, about to shoot, three friends watching from the chain-link fence behind her, soft and out of focus.
UGC phone footage, vertical 9:16, an outdoor city basketball court at night, bright white floodlights from above, chain-link fence, apartment buildings with lit windows in the background, high contrast, natural skin texture, real fabric folds, no color grading
Full shot from courtside at waist height, vertical 9:16, her head at about one quarter of the frame height, the jersey front visible, the hoop visible at the top right, top 15% and bottom 20% kept clear. One person in focus, no readable signs, no other text, no watermark, natural hands with five fingers.
```
**Soát trước khi làm video:** áo đúng · bạn bè phía sau mờ, không méo mặt · rổ nằm trong khung

## Clip 1 · 8s · Phố đêm: bước tới → khoe áo
**Khung đầu:** `keyframe_c1.png` · **Lưu video thành:** `c01_a.mp4` (gen lại thì lưu `c01_b.mp4`)

**Cảnh:** 4 giây đầu Maya bước tự tin về phía camera; 4 giây sau dừng lại, kéo vạt áo khoe chữ vàng rồi hất cằm nhìn ống kính.
```
Low-angle full shot, slow dolly out as the woman walks toward the camera with a confident, steady stride through the steam, neon reflections sliding across the wet street. Around the middle of the clip she stops, pulls the front of the jersey taut with both hands to show the gold lettering, then lifts her chin and stares into the lens.
Audio: city street ambience, distant traffic, no speech, no music. No subtitles, no on-screen text.
```
**Phủ định (Negative):** `subtitles, captions, on-screen text, watermark, misspelled name or numbers, large badges on the front panel, distorted logos, readable store signs, music`

## Clip 2 · 8s · Lưng áo → xoay người
**Khung đầu:** `keyframe_c2.png` · **Lưu video thành:** `c02_a.mp4`

**Cảnh:** 4 giây đầu Maya đứng yên quay lưng, "BRUNSON 11" rõ nét; 4 giây sau xoay người lại chậm rãi, nhìn thẳng ống kính.
```
Medium shot from behind, static. The woman stands still with her back to the camera for the first half of the clip, the name and number sharp and steady while steam drifts past. Then she turns around slowly to face the lens, gives a slight nod and holds her look.
Audio: city street ambience, distant traffic, no speech, no music. No subtitles, no on-screen text.
```
**Phủ định (Negative):** `subtitles, captions, changing letters, misspelled name, folds across the lettering, camera rotation, music`

## Clip 3 · 8s · Cận chữ vàng → patch cúp
**Khung đầu:** `keyframe_c3.png` · **Lưu video thành:** `c03_a.mp4`

**Cảnh:** một vệt sáng quét qua chữ NEW YORK làm chữ vàng loé lên; nửa sau camera lia chậm sang patch cúp và số 11.
```
Macro close-up, slow pan. A bright band of warm light sweeps slowly across the gold NEW YORK lettering from left to right, making the gold flash. In the second half the camera drifts down and across to the small gold trophy patch and the number 11, the fabric moving gently with her breath. The lettering stays flat and sharp.
Audio: city street ambience, no speech, no music. No subtitles, no on-screen text.
```
**Phủ định (Negative):** `subtitles, captions, changing letters, redrawn patch, extra text, blur on the lettering, fast motion, music`

## Clip 4 · 8s · Sân bóng: ném rổ → ăn mừng
**Khung đầu:** `keyframe_c4.png` · **Lưu video thành:** `c04_a.mp4`

**Cảnh:** 4 giây đầu Maya nhồi bóng rồi ném rổ vào lưới; 4 giây sau bạn bè ùa vào ăn mừng, kim tuyến vàng bay.
```
Full shot from courtside, static. The woman bounces the ball twice under the floodlights, rises into a smooth jump shot and the ball drops through the net. Around the middle of the clip her friends rush in cheering as gold confetti falls through the light; the jersey front faces the camera as she celebrates with both arms up.
Audio: ball bouncing on asphalt, rim rattle, cheering, no dialogue, no music. No subtitles, no on-screen text.
```
**Phủ định (Negative):** `subtitles, captions, readable signs, extra people in focus, distorted faces, distorted ball, misspelled lettering, professional athlete, music`

## Thiết lập khi gen video
- Cả 4 clip: chế độ **ảnh làm khung đầu** (first frame), 8 giây, dọc 9:16, **1080p** (lần trước clip ra 720p: nếu công cụ có tuỳ chọn 1080p thì chọn).
- Có ô Negative thì dán dòng "Phủ định"; không có thì bỏ qua.
- Tiếng của clip không quan trọng: video dùng nhạc rap, tiếng gốc bị tắt khi dựng.

Dựng: đưa clip vào `projects/nyk-brunson-11-champions-jersey/clips/` rồi nhắn "dựng video nyk".
