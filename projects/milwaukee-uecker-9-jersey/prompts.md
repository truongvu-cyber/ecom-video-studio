# Áo jersey Milwaukee Uecker #9 — prompt tạo ảnh và video

Phần mô tả, hướng dẫn và ghi chú viết bằng tiếng Việt. Phần prompt (trong khung code) và các khóa giữ bằng tiếng Anh: **copy nguyên văn, không dịch**.

| Công cụ video | Công cụ ảnh | Tỉ lệ | Độ dài | Số clip | Phong cách | Thể loại | Âm thanh |
|---|---|---|---|---|---|---|---|
| Veo 3.1 | Nano Banana Pro | 9:16 | ~16 giây | 4 clip × 8 giây | UGC watch party buổi tối | hype / UGC review | clip 1 có lời thoại, các clip khác tiếng động, nhạc hype không lời thêm khi dựng |

**Lưu ý chung:**
- Prompt mô tả hình dáng logo, không gọi tên thương hiệu, để model không từ chối hay làm mờ. Logo thật đi vào hình qua ảnh sản phẩm.
- Ảnh sản phẩm có hai patch lớn ở góc dưới là **hình minh hoạ**, không nằm trên áo. Prompt đã dặn model bỏ qua; khi soát keyframe, xem kỹ không có patch nào bị gắn lên vạt áo.

## Các khóa (dán nguyên văn, không sửa chữ nào)

**PRODUCT (sản phẩm):**
navy button-front baseball jersey with gold piping along the placket, collar and sleeve ends, the word Milwaukee in gold script across the chest, a gold number 9 below the script on the wearer's left side, a small gold check-shaped logo on the wearer's right chest, a round World Series 2026 patch on the wearer's left chest above the script, a NATIONAL LEAGUE CHAMPIONS 2026 patch on the wearer's left sleeve, a gold monogram patch on the wearer's right sleeve, and on the back the name UECKER in gold block letters above a large gold number 9

**CHARACTER - Jake (nhân vật):**
man in his early 30s, medium sturdy build, fair skin, short brown hair, full trimmed brown beard, white crew-neck t-shirt under the open jersey collar, dark blue jeans

**STYLE (phong cách, bối cảnh, ánh sáng):**
UGC phone footage, vertical 9:16, a cozy Midwest living room at night before a game, blue glow from a large TV off to the side, warm lamp light from the right, a couch and a coffee table with snacks and unlabeled drink bottles, natural skin texture, real fabric folds, no color grading

**VOICE (giọng nói, cho clip 1):**
American man, early 30s, Midwest accent, excited and friendly, quick natural pace, a little hoarse like before a big game

**AUDIO (âm thanh):** living room room tone, faint muffled TV game sound, no music

**NEGATIVE (những thứ cần tránh):** subtitles, captions, on-screen text, watermark, misspelled name or numbers, extra patches on the front panels, floating badges, distorted logos, readable TV channel graphics, ring light, beauty filter, cinematic grading, music

## Bước 0 — Ảnh tham chiếu (làm trước mọi cảnh)

1. **Ảnh sản phẩm:** `frames/product.png`. Ảnh này có cả mặt sau (bên trái) và mặt trước (bên phải): **luôn tải lên làm ảnh 1**.
2. **Ảnh nhân vật Jake:** gen một lần, dùng cho keyframe 1, 3 và 4.
   ```
   Character reference sheet, one image, 16:9: three full-body views (front, side, back) on the left, one chest-up close-up on the right, plain light-grey background, even soft light. Man in his early 30s, medium sturdy build, fair skin, short brown hair, full trimmed brown beard, white crew-neck t-shirt, dark blue jeans. No text, no logos, no watermark.
   ```
   **Lưu thành:** `jake_sheet.png`

## Ảnh khung đầu (gen và soát xong hết mới sang video)

### Keyframe 1 · cho clip 1 · Nano Banana Pro
**Ảnh tải lên:** ảnh 1 = `product.png`, ảnh 2 = `jake_sheet.png` · **Lưu thành:** `keyframe_c1.png`

**Cảnh:** Jake mặc áo đứng giữa phòng khách buổi tối, đèn TV hắt xanh một bên, nhìn ống kính, tay đang chạm vạt áo chuẩn bị khoe.
```
Image 1 is the product: a navy baseball jersey, shown from the back on the left and the front on the right. The two large round badges at the bottom of image 1 are only reference callouts of the patches; do not place them on the jersey. Keep the jersey exactly as in image 1: same script lettering, numbers, piping, patches, colours and placement; do not retype, restyle or move anything. Image 2 is the man; keep his face, hair and beard.
Man in his early 30s, medium sturdy build, fair skin, short brown hair, full trimmed brown beard, white crew-neck t-shirt under the open jersey collar, dark blue jeans, wearing the jersey from image 1 buttoned, standing in the middle of the room facing the camera, right hand pinching the jersey's front edge, about to show the chest patch, excited half smile.
UGC phone footage, vertical 9:16, a cozy Midwest living room at night before a game, blue glow from a large TV off to the side, warm lamp light from the right, a couch and a coffee table with snacks and unlabeled drink bottles, natural skin texture, real fabric folds, no color grading
Medium shot from chest height, vertical 9:16, his head at about one third of the frame height, the whole front of the jersey visible and flat, top 15% and bottom 20% kept clear. One person, no other text, no watermark, natural hands with five fingers.
```
**Soát trước khi làm video:** chữ Milwaukee, số 9 đúng · patch World Series ở ngực, patch NL Champions ở tay áo · không có patch thừa trên vạt áo · tay đủ 5 ngón · ảnh dọc 9:16

### Keyframe 2 · cho clip 2 · Nano Banana Pro
**Ảnh tải lên:** ảnh 1 = `product.png`, ảnh 2 = `keyframe_c1.png` · **Lưu thành:** `keyframe_c2.png`

**Cảnh:** áo treo trên móc gỗ ở cửa phòng, quay lưng ra, "UECKER 9" chiếm giữa khung.
```
Image 1 is the product: keep the back of the navy jersey exactly as in image 1, the name UECKER in gold block letters above a large gold number 9, same letters, size, spacing and colours; do not retype, restyle or move them. The two large round badges at the bottom of image 1 are only reference callouts; do not place them on the jersey. Image 2 is the room and light to match.
The jersey hangs from a wooden hanger on a hook on the living room door, back facing the camera, fabric smooth across the name and number, sleeves hanging straight.
UGC phone footage, vertical 9:16, a cozy Midwest living room at night before a game, blue glow from a large TV off to the side, warm lamp light from the right, natural texture of the fabric, no color grading
Straight-on medium close-up, vertical 9:16, the name and number centred and filling about half of the frame width, top 15% and bottom 20% kept clear. No people, no other text, no watermark.
```
**Soát trước khi làm video:** U-E-C-K-E-R đúng chính tả · số 9 đúng kiểu chữ · vải phẳng, không nếp gấp cắt qua chữ

### Keyframe 3 · cho clip 3 · Nano Banana Pro
**Ảnh tải lên:** ảnh 1 = `product.png`, ảnh 2 = `keyframe_c1.png` · **Lưu thành:** `keyframe_c3.png`

**Cảnh:** cận cảnh patch World Series 2026 trên ngực áo đang mặc, một phần chữ Milwaukee ở mép dưới khung.
```
Image 1 is the product: keep the round World Series 2026 patch and the gold script lettering exactly as in image 1: same embroidery, colours, numbers and placement; do not redraw or restyle them. The two large round badges at the bottom of image 1 are only reference callouts; the chest patch is the small one on the wearer's left chest. Image 2 is the man, room and light to match.
Close-up of the wearer's left chest of the navy jersey worn by the man, the round patch sharp in the centre, the top of the gold script word below it, gold piping running down the placket on the right of the frame, fabric smooth.
UGC phone footage, vertical 9:16, a cozy Midwest living room at night before a game, blue glow from a large TV off to the side, warm lamp light from the right, natural skin texture, real fabric folds, no color grading
Macro close-up, straight-on, vertical 9:16, the patch filling about 40% of the frame width, top 15% and bottom 20% kept clear. No other text, no watermark.
```
**Soát trước khi làm video:** chữ và số 2026 trên patch đúng như ảnh gốc · thêu rõ nét

### Keyframe 4 · cho clip 4 · Nano Banana Pro
**Ảnh tải lên:** ảnh 1 = `product.png`, ảnh 2 = `jake_sheet.png`, ảnh 3 = `keyframe_c1.png` · **Lưu thành:** `keyframe_c4.png`

**Cảnh:** watch party: Jake ngồi mép ghế sofa trước TV, người hơi nhổm lên, hai bạn ngồi phía sau bị mờ, ngay trước khoảnh khắc bật dậy reo hò.
```
Image 1 is the product: keep the jersey exactly as in image 1, same lettering, numbers, piping, patches and colours; do not retype, restyle or move anything, and do not place the two reference callout badges on it. Image 2 is the man; keep his face, hair and beard. Image 3 is the room and light to match.
Man in his early 30s, medium sturdy build, fair skin, short brown hair, full trimmed brown beard, white crew-neck t-shirt under the open jersey collar, dark blue jeans, wearing the jersey from image 1, sitting on the front edge of the couch leaning forward toward the TV, fists half raised, mouth open in anticipation; two friends sit behind him on the couch, soft and out of focus.
UGC phone footage, vertical 9:16, a cozy Midwest living room at night before a game, blue glow from a large TV off to the side, warm lamp light from the right, a couch and a coffee table with snacks and unlabeled drink bottles, natural skin texture, real fabric folds, no color grading
Medium shot from the side of the TV looking back at him, vertical 9:16, his head at about one third of the frame height, the jersey front visible, top 15% and bottom 20% kept clear. No readable screen graphics, no other text, no watermark, natural hands with five fingers.
```
**Soát trước khi làm video:** áo đúng · hai người phía sau mờ, không méo mặt · không có chữ trên màn hình TV

## Clip 1 · 8s · Lời thoại (A-roll)
**Cách gen:** Veo **Ingredients** (ảnh tham chiếu), không dùng chế độ khung đầu vì chế độ đó hay mất tiếng · **Khung đầu:** không có, tham chiếu `keyframe_c1.png` + `product.png` + `jake_sheet.png` · **Lưu video thành:** `c01_a.mp4` (gen lại thì lưu `c01_b.mp4`)

**Cảnh:** Jake nói 3 câu với camera: khoe patch ngực, xoay người khoe tay áo và lưng, rồi chỉ xuống dưới. Giữa các câu có khoảng nghỉ để dựng cắt.
```
Man in his early 30s, medium sturdy build, fair skin, short brown hair, full trimmed brown beard, white crew-neck t-shirt under the open jersey collar, dark blue jeans, wearing a navy button-front baseball jersey with gold piping along the placket, collar and sleeve ends, the word Milwaukee in gold script across the chest, a gold number 9 below the script on the wearer's left side, a small gold check-shaped logo on the wearer's right chest, a round World Series 2026 patch on the wearer's left chest above the script, a NATIONAL LEAGUE CHAMPIONS 2026 patch on the wearer's left sleeve, a gold monogram patch on the wearer's right sleeve, and on the back the name UECKER in gold block letters above a large gold number 9.
Cozy living room at night, blue TV glow from the side, warm lamp from the right. Medium shot at chest height, static, slight handheld shake.
He pinches the jersey front toward the lens. He says: Milwaukee fans, look at this.
A short pause. He turns to show the sleeve, then his back. He says: World Series and NL Champions patches. Uecker nine.
He turns back, grins and points down. He says: Link's below, grab yours. He holds the grin.
Voice: American man, early 30s, Midwest accent, excited, quick natural pace.
Audio: his voice, room tone, faint TV game sound, no music. No subtitles, no on-screen text.
```
**Phủ định (Negative):** `subtitles, captions, on-screen text, watermark, misspelled name or numbers, extra patches on the front panels, floating badges, distorted logos, music`

## Clip 2 · 8s · Lưng áo UECKER 9
**Khung đầu:** `keyframe_c2.png` · **Lưu video thành:** `c02_a.mp4`

**Cảnh:** camera đẩy chậm vào lưng áo treo trên cửa, ánh TV chớp nhẹ lên vải. Chữ và số đứng yên.
```
Straight-on medium close-up, slow push in toward the name and number. The jersey hangs still on the door; flickering blue light from the TV plays softly across the fabric. Nothing else moves; the lettering stays flat and sharp.
Audio: faint muffled TV game sound from the next room, a soft creak of the hanger, no speech, no music. No subtitles, no on-screen text.
```
**Phủ định (Negative):** `subtitles, captions, changing letters, misspelled name, extra text, folds across the lettering, camera rotation, music`

## Clip 3 · 8s · Cận patch
**Khung đầu:** `keyframe_c3.png` · **Lưu video thành:** `c03_a.mp4`

**Cảnh:** cận patch World Series, ngón tay chạm nhẹ mép patch rồi rút ra, camera đẩy rất chậm.
```
Macro close-up, very slow push in on the round chest patch. His fingertip slowly traces the edge of the patch, then moves away; the embroidery catches the warm lamp light. The patch and the lettering stay flat and still.
Audio: soft fabric rustle, faint muffled TV game sound, no speech, no music. No subtitles, no on-screen text.
```
**Phủ định (Negative):** `subtitles, captions, changing numbers, redrawn patch, extra text, blur on the patch, fast motion, music`

## Clip 4 · 8s · Watch party
**Khung đầu:** `keyframe_c4.png` · **Lưu video thành:** `c04_a.mp4`

**Cảnh:** Jake bật dậy khỏi sofa reo hò, hai tay giơ lên, bạn bè phía sau cũng nhổm dậy (mờ). Không có chữ hay hình đồ hoạ trên TV.
```
Medium shot, static. The man leaps up from the couch edge and cheers with both fists in the air, jersey front facing the camera; the two friends behind him jump up too, soft and out of focus. Blue TV light flickers across the room.
Audio: cheering and clapping, muffled TV game sound, no dialogue, no music. No subtitles, no on-screen text.
```
**Phủ định (Negative):** `subtitles, captions, readable TV graphics, extra people in focus, distorted faces, misspelled lettering, music`

## Thiết lập khi gen video
- Clip 1: chế độ **Ingredients / ảnh tham chiếu**, 8 giây, dọc 9:16, 1080p.
- Clip 2–4: chế độ **ảnh làm khung đầu** (first frame), 8 giây, dọc 9:16, 1080p.
- Có ô Negative thì dán dòng "Phủ định"; không có thì bỏ qua.

Dựng: đưa clip vào `projects/milwaukee-uecker-9-jersey/clips/` rồi nhắn "dựng video jersey".
