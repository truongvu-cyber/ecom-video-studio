# Đèn chiếu logo cửa xe (Cubs) — hướng UGC call-out — prompt tạo ảnh và video

Phần mô tả, hướng dẫn và ghi chú viết bằng tiếng Việt. Phần prompt (trong khung code) và các khóa giữ bằng tiếng Anh: **copy nguyên văn, không dịch**.

| Công cụ video | Công cụ ảnh | Tỉ lệ | Độ dài | Số clip | Phong cách | Thể loại | Âm thanh |
|---|---|---|---|---|---|---|---|
| Omni 1.1 Flash (Flow, chế độ Thành phần) | Nano Banana 2.1 | 9:16 | ~15 giây, 6 nhát cắt | 1 clip thoại + 3 B-roll × 8 giây | UGC điện thoại, bãi đỗ đêm + lối vào nhà ban ngày | call-out có lời + chứng minh | giữ giọng Mike và tiếng cửa, nhạc hip-hop ấm dưới lời |

**Lưu ý chung:**
- **Logo chiếu dưới đất luôn lấy từ `product_projection.png`** (ảnh 1 trong thành phần của mọi cảnh có logo); video chỉ làm nó sáng lên hoặc camera di chuyển. Không để model tự vẽ logo.
- Clip 1 là clip thoại duy nhất (giọng chỉ ổn định trong một lần gen). Lời thoại dạng `He says:` không dấu ngoặc kép, có khoảng lặng trước và sau mỗi câu.
- Mọi prompt có người/tay dán nguyên khoá **REALISM** và ghi rõ vị trí + đường đi so với xe và cửa (realism.md).
- Prompt mô tả hình logo, không gọi tên đội. Xe không để lộ logo hãng.

## Các khóa (dán nguyên văn, không sửa chữ nào)

**PRODUCT (sản phẩm):**
a palm-sized matte black square projector unit with a small round lens on its underside, stuck under the inside door panel of a car; when the door is open it projects a round logo onto the ground: a blue outer ring, a thin white ring, and a red letter C wrapping the red block letters UBS on a white field, exactly as in the product photo

**CHARACTER - Mike (nhân vật):**
man in his early 40s, medium build, light skin, short dark-blond hair, light stubble, royal-blue baseball cap with a red letter C on the front, white baseball jersey with thin blue pinstripes and a round red-and-blue crest with a letter C on the chest, no other lettering, worn open over a navy long-sleeve henley, dark jeans

**REALISM (độ chân thực + vật lý, dán vào mọi prompt có người/tay):**
Real human being filmed on a phone: natural skin with pores and slight unevenness, real eyes with reflections, hair with individual strands, clothing that creases and hangs with weight. Every movement obeys physics: feet stay on the ground, weight shifts before a step, hands grip objects with correct finger placement and stay on their surfaces, bodies and clothes keep clear of the car, the door, the ground and each other, objects keep their size and weight. One continuous action at real speed.

**STYLE (cảnh đêm):**
UGC phone footage, vertical 9:16, a quiet parking lot at night, dark textured asphalt, soft amber streetlights far in the background, a blue coupe with no visible badges or logos, a red-and-blue pennant hanging from the rear-view mirror, natural contrast, real textures, no color grading

**STYLE - day (cảnh lắp ban ngày):**
UGC phone footage, vertical 9:16, a home driveway in soft afternoon daylight, light grey concrete tiles, the same blue coupe with no visible badges or logos, a white flag with a big blue letter W hanging on the garage wall, clearly visible behind, natural colours, real skin and fabric texture, no color grading

**VOICE (giọng Mike, clip 1):**
a relaxed mid-range American male voice, friendly, slightly amused, speaking at a normal pace to a phone held at arm's length

**AUDIO (B-roll):** quiet ambience, no speech, no music

**NEGATIVE (chung):** subtitles, captions, on-screen text, watermark, misspelled or redrawn logo, extra logos, car brand badges, cinematic grading, music, plastic skin, airbrushed, beauty filter, uncanny face, extra fingers, fused fingers, distorted hands, extra limbs, body passing through the car or door, clipping through objects, floating objects, morphing, duplicated person, teleporting, sliding feet, warped background

## Bước 0 — Ảnh tham chiếu (có sẵn, không gen)

1. `frames/product_projection.png` — nguồn duy nhất của logo.
2. `frames/install_steps_row.png` — hộp đèn và tay thao tác thật.
3. `frames/mike_sheet.png` — nhân vật Mike (gen ở project trước, dùng lại).
4. `frames/car_night.png` — xe, mặt đường và ánh sáng đêm (keyframe 1 của project trước), để xe giống nhau giữa các cảnh.

## Bước 1 — Ảnh khung đầu (Nano Banana 2.1, 9:16)

### Keyframe 1 · cho clip 1 (thoại) · Nano Banana 2.1
**Ảnh tải lên:** ảnh 1 = `mike_sheet.png`, ảnh 2 = `car_night.png` · **Lưu thành:** `keyframe_c1.png`

**Cảnh:** đêm, Mike đứng ngoài xe cạnh cửa lái đang đóng, tay phải đặt trên tay nắm, nhìn thẳng ống kính như sắp nói.
```
Image 1 is the man; keep his face, cap and outfit exactly. Image 2 is the car, asphalt and night light to match; here the driver's door is fully closed.
Man in his early 40s, medium build, light skin, short dark-blond hair, light stubble, navy long-sleeve henley, dark jeans, plain navy baseball cap with no logo, standing on the asphalt outside the closed driver's door of the blue coupe, half a step from the car, body angled toward the phone, right hand resting on the door handle, left arm relaxed, looking straight into the lens with a small knowing smile, mouth closed.
Real human being filmed on a phone: natural skin with pores and slight unevenness, real eyes with reflections, hair with individual strands, clothing that creases and hangs with weight. Every movement obeys physics: feet stay on the ground, weight shifts before a step, hands grip objects with correct finger placement and stay on their surfaces, bodies and clothes keep clear of the car, the door, the ground and each other, objects keep their size and weight. One continuous action at real speed.
UGC phone footage, vertical 9:16, a quiet parking lot at night, dark textured asphalt, soft amber streetlights far in the background, a blue coupe with no visible badges or logos, a red-and-blue pennant hanging from the rear-view mirror, natural contrast, real textures, no color grading
Medium shot from chest height, vertical 9:16, the man in the centre, the closed door and handle visible beside him, the ground in front of the door dark with no projection yet, top 15% and bottom 20% kept clear. No text, no watermark, natural hands with five fingers.
```
**Soát trước khi làm video:** cửa đóng hẳn, chưa có logo dưới đất · mặt và mũ giống sheet · tay phải trên tay nắm, đủ ngón · không có logo hãng xe · hộp đèn nằm dưới mép dưới tấm ốp cửa, ống kính hướng xuống · logo ngay dưới mép cửa đang mở (door open), đất tối khi cửa đóng

### Keyframe 2 · cho clip 2 · Nano Banana 2.1
**Ảnh tải lên:** ảnh 1 = `product_projection.png`, ảnh 2 = `car_night.png` · **Lưu thành:** `keyframe_c2.png`

**Cảnh:** cận từ thấp bên ngoài xe: cửa lái mới hé mở một khoảng, logo đã hiện sắc nét trên mặt đường ngay dưới mép cửa.
```
Image 1 is the product: keep the projected ground logo exactly as in image 1, a blue outer ring, a thin white ring, a red letter C wrapping the red block letters UBS on a white field; do not redraw or retype it. Image 2 is the car, asphalt and night light to match.
Low close-up from outside the blue coupe at knee height: the driver's door is open about a third of the way, and from a small black unit under the inner door panel a beam projects the logo sharp and bright onto the dark asphalt just below the door edge, filling the lower half of the frame. No person in frame.
UGC phone footage, vertical 9:16, a quiet parking lot at night, dark textured asphalt, soft amber streetlights far in the background, a blue coupe with no visible badges or logos, a red-and-blue pennant hanging from the rear-view mirror, natural contrast, real textures, no color grading
Vertical 9:16, the logo sharp in the lower third, the door edge and the glowing unit above it, top 15% and bottom 20% kept clear. No text, no watermark.
```
**Soát trước khi làm video:** logo đúng hệt ảnh 1 từng nét · không có logo hãng xe · không có người · hộp đèn nằm dưới mép dưới tấm ốp cửa, ống kính hướng xuống · logo ngay dưới mép cửa đang mở (door open), đất tối khi cửa đóng

### Keyframe 3 · cho clip 3 · Nano Banana 2.1
**Ảnh tải lên:** ảnh 1 = `install_steps_row.png` · **Lưu thành:** `keyframe_c3.png`

**Cảnh:** ban ngày, cận hai bàn tay Mike cầm hộp đèn, ngón đang nhón một góc màng đỏ ở mặt keo, cửa xe mở phía sau.
```
Image 1 shows four real install photos; use the third one as the reference: two hands peeling a red film off the adhesive pad on the back of the black projector unit. Keep the unit's shape and the red film exactly as in image 1.
Close-up of a man's two hands in a navy long sleeve, standing outside the car beside the open driver's door, holding the unit at chest height in the left hand, the right fingers pinching one corner of the red film just starting to lift, the open door and dark inner door panel softly behind.
Real human being filmed on a phone: natural skin with pores and slight unevenness, real eyes with reflections, hair with individual strands, clothing that creases and hangs with weight. Every movement obeys physics: feet stay on the ground, weight shifts before a step, hands grip objects with correct finger placement and stay on their surfaces, bodies and clothes keep clear of the car, the door, the ground and each other, objects keep their size and weight. One continuous action at real speed.
UGC phone footage, vertical 9:16, a home driveway in soft afternoon daylight, light grey concrete tiles, the same blue coupe with no visible badges or logos, a white flag with a big blue letter W hanging on the garage wall, clearly visible behind, natural colours, real skin and fabric texture, no color grading
Close-up, vertical 9:16, the unit in the centre third, top 15% and bottom 20% kept clear. No text, no watermark, natural hands with five fingers.
```
**Soát trước khi làm video:** tay đủ ngón · màng đỏ đang bóc ở một góc · hộp đèn đúng hình · hộp đèn nằm dưới mép dưới tấm ốp cửa, ống kính hướng xuống · logo ngay dưới mép cửa đang mở (door open), đất tối khi cửa đóng

### Keyframe 4 · cho clip 4 · Nano Banana 2.1
**Ảnh tải lên:** ảnh 1 = `product_projection.png`, ảnh 2 = `mike_sheet.png`, ảnh 3 = `car_night.png` · **Lưu thành:** `keyframe_c4.png`

**Cảnh:** góc rất thấp sát mặt đường ban đêm, cửa lái mở, logo sắc nét chiếm phần dưới khung, chân phải của Mike (giày, ống quần jeans) vừa đặt xuống cạnh logo, người cắt ở ngang hông.
```
Image 1 is the product: keep the projected ground logo exactly as in image 1, a blue outer ring, a thin white ring, a red letter C wrapping the red block letters UBS on a white field; do not redraw or retype it. Image 2 is the man's shoes, jeans and build. Image 3 is the car, asphalt and night light to match.
Very low angle from the asphalt outside the blue coupe: the driver's door is open, the logo projected sharp and bright on the ground beside the door sill, and the man's right foot in a dark sneaker and dark jeans has just stepped onto the asphalt next to the logo, not on it, his body cropped at the waist, standing on the ground outside the car.
Real human being filmed on a phone: natural skin with pores and slight unevenness, real eyes with reflections, hair with individual strands, clothing that creases and hangs with weight. Every movement obeys physics: feet stay on the ground, weight shifts before a step, hands grip objects with correct finger placement and stay on their surfaces, bodies and clothes keep clear of the car, the door, the ground and each other, objects keep their size and weight. One continuous action at real speed.
UGC phone footage, vertical 9:16, a quiet parking lot at night, dark textured asphalt, soft amber streetlights far in the background, a blue coupe with no visible badges or logos, a red-and-blue pennant hanging from the rear-view mirror, natural contrast, real textures, no color grading
Vertical 9:16, the logo sharp in the lower third, the shoe beside it, the open door above, top 15% and bottom 20% kept clear. No text, no watermark.
```
**Soát trước khi làm video:** logo đúng hệt ảnh 1 · giày đặt cạnh logo, không đè lên · không có logo hãng xe · hộp đèn nằm dưới mép dưới tấm ốp cửa, ống kính hướng xuống · logo ngay dưới mép cửa đang mở (door open), đất tối khi cửa đóng

## Bước 2 — Prompt video (Omni 1.1 Flash, chế độ Thành phần, 8 giây, 9:16)

## Clip 1 · 8s · Thoại (A-roll) — Ingredients
**Khung đầu (ingredients, thứ tự tải lên):** `keyframe_c1.png`, `mike_sheet.png`, `product_projection.png` · **Lưu video thành:** `c01_a.mp4`

**Cảnh:** Mike nhìn ống kính nói câu gọi fan, kéo tay nắm mở cửa (người lùi theo cánh cửa, vẫn đứng ngoài xe), logo bừng sáng dưới đất, anh cúi chỉ vào hộp đèn nói "sixty seconds, no tools", đứng thẳng nhìn ống kính nói "link below", giữ nụ cười.
```
Medium shot, handheld phone at chest height, static. The man stands on the asphalt outside the closed driver's door of the blue coupe, half a step from the car, right hand on the door handle, looking into the lens. A short beat of silence. He says: Chicago fans, watch my door. He pulls the handle and swings the door open toward himself, stepping back along the outside of the door so it clears him, both feet staying on the ground; a bright round logo appears on the asphalt below the open door, exactly the logo in the product image. He glances down at it, bends at the waist and points with his left hand at the small black unit under the inner door panel, from outside the car. He says: Sixty seconds, no tools. He straightens up, looks into the lens and smiles. He says: Link below. He holds the smile for a moment.
Real human being filmed on a phone: natural skin with pores and slight unevenness, real eyes with reflections, hair with individual strands, clothing that creases and hangs with weight. Every movement obeys physics: feet stay on the ground, weight shifts before a step, hands grip objects with correct finger placement and stay on their surfaces, bodies and clothes keep clear of the car, the door, the ground and each other, objects keep their size and weight. One continuous action at real speed.
Audio: his voice, a relaxed mid-range American male voice, friendly, slightly amused, speaking at a normal pace; the clunk of the door latch, quiet night ambience, no music. No subtitles, no on-screen text.
```
**Phủ định (Negative):** `subtitles, captions, on-screen text, watermark, misspelled or redrawn logo, extra logos, car brand badges, music, plastic skin, airbrushed, beauty filter, uncanny face, extra fingers, fused fingers, distorted hands, extra limbs, body passing through the car or door, clipping through objects, floating objects, morphing, duplicated person, teleporting, sliding feet, warped background`
**Soát clip:** hộp đèn nằm dưới tấm ốp cửa (under the inner door panel), logo chỉ hiện khi cửa mở và nằm ngay dưới mép cửa · người đứng ngoài xe, không xuyên cửa/ngưỡng (sill) · mặt và áo giống sheet suốt 8 giây · lời đúng 3 câu

## Clip 2 · 8s · Cửa mở → logo bừng sáng (B-roll)
**Khung đầu:** `keyframe_c2.png` · **Lưu video thành:** `c02_a.mp4`

**Cảnh:** cửa tiếp tục mở rộng ra, chùm sáng mạnh lên, logo sắc hơn; camera đẩy chậm xuống logo.
```
Low close-up from outside the car at knee height, slow push in. The driver's door keeps swinging open wider at real speed and the projector beam brightens, so the logo on the asphalt glows stronger and sharper while staying perfectly still and identical in every frame. The camera moves slowly toward the logo until it fills most of the lower frame. No person in frame.
Audio: a soft door hinge, quiet night ambience, no speech, no music. No subtitles, no on-screen text.
```
**Phủ định (Negative):** `subtitles, captions, on-screen text, watermark, misspelled or redrawn logo, flickering logo, extra logos, car brand badges, people, music`
**Soát clip:** hộp đèn dưới tấm ốp cửa (under the inner door panel), ống kính hướng xuống · logo ngay dưới mép cửa mở (door open), đúng hệt ảnh gốc ở mọi giây · không có người

## Clip 3 · 8s · Bóc keo → dán (B-roll, ban ngày)
**Khung đầu:** `keyframe_c3.png` · **Lưu video thành:** `c03_a.mp4`

**Cảnh:** nửa đầu bóc hết màng đỏ một đường gọn; nửa sau đưa hộp đèn từ ngoài vào, ấn phẳng lên dưới tấm ốp cửa bằng lòng bàn tay, giữ rồi buông, hộp dính chắc.
```
Close-up, slow tilt up. The man stands on the driveway outside the car beside the open driver's door, holding the unit in his left hand at chest height. His right fingers pinch one corner of the red film and peel it off the adhesive pad in one smooth pull. Around the middle of the clip the camera tilts up to the bottom of the inner door panel; he brings the unit to the panel from the outside, presses it flat against the panel surface with his right palm, holds it for a moment, then lets go; the unit stays stuck to the panel, nothing passes into the panel.
Real human being filmed on a phone: natural skin with pores and slight unevenness, real eyes with reflections, hair with individual strands, clothing that creases and hangs with weight. Every movement obeys physics: feet stay on the ground, weight shifts before a step, hands grip objects with correct finger placement and stay on their surfaces, bodies and clothes keep clear of the car, the door, the ground and each other, objects keep their size and weight. One continuous action at real speed.
Audio: soft peel of the film, a firm press, quiet driveway ambience, no speech, no music. No subtitles, no on-screen text.
```
**Phủ định (Negative):** `subtitles, captions, unit falling, fast motion, music, plastic skin, airbrushed, beauty filter, uncanny face, extra fingers, fused fingers, distorted hands, extra limbs, body passing through the car or door, clipping through objects, floating objects, morphing, duplicated person, teleporting, sliding feet, warped background`
**Soát clip:** hộp đèn được ấn vào dưới mép dưới tấm ốp cửa (under the inner door panel), không dán lên ngưỡng cửa/ghế (sill, seat) · tay đủ ngón, không xuyên tấm ốp · áo và xe đúng màu khoá

## Clip 4 · 8s · Bước xuống cạnh logo (B-roll)
**Khung đầu:** `keyframe_c4.png` · **Lưu video thành:** `c04_a.mp4`

**Cảnh:** góc thấp: chân phải đã đặt cạnh logo, chân trái bước xuống theo, người đứng thẳng ngoài xe; camera đẩy chậm vào logo, logo giữ nguyên.
```
Very low angle from the asphalt, slow push in. The man steps out of the car: his right foot is already on the asphalt beside the logo, his left foot follows and lands next to it, both feet outside the car and beside the logo, never on it; his legs straighten as he stands up outside the open door, body cropped at the waist. The logo on the ground stays sharp, still and identical in every frame as the camera moves slowly toward it.
Real human being filmed on a phone: natural skin with pores and slight unevenness, real eyes with reflections, hair with individual strands, clothing that creases and hangs with weight. Every movement obeys physics: feet stay on the ground, weight shifts before a step, hands grip objects with correct finger placement and stay on their surfaces, bodies and clothes keep clear of the car, the door, the ground and each other, objects keep their size and weight. One continuous action at real speed.
Audio: a shoe on asphalt, quiet night ambience, no speech, no music. No subtitles, no on-screen text.
```
**Phủ định (Negative):** `subtitles, captions, misspelled or redrawn logo, flickering logo, extra logos, car brand badges, music, plastic skin, airbrushed, beauty filter, uncanny face, extra fingers, fused fingers, distorted hands, extra limbs, body passing through the car or door, clipping through objects, floating objects, morphing, duplicated person, teleporting, sliding feet, warped background`
**Soát clip:** logo ngay dưới mép cửa mở (door open), đúng hệt ảnh gốc · chân đặt ngoài xe cạnh logo, không đè lên, không xuyên ngưỡng cửa (sill) · đất tối khi cửa đóng (door closed)

## Thiết lập khi gen video
- Cả 4 clip: Omni 1.1 Flash, chế độ **Thành phần** (ingredients): ảnh sản phẩm/hình in trước, keyframe sau; 8 giây, dọc 9:16, tải **1080p** (không chọn tuỳ chọn tính tín dụng).
- Clip 1 là clip thoại: nếu model từ chối "Chicago fans" thì đổi thành "Baseball fans" và ghi lại trong production.json.
- Giữ tiếng gốc clip 1 (giọng + cửa); B-roll không có lời.
