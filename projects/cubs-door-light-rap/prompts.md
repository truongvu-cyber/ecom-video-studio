# Đèn chiếu logo cửa xe (Cubs) — hướng hype rap, hook mở cửa — prompt tạo ảnh và video

Phần mô tả, hướng dẫn và ghi chú viết bằng tiếng Việt. Phần prompt (trong khung code) và các khóa giữ bằng tiếng Anh: **copy nguyên văn, không dịch**.

| Công cụ video | Công cụ ảnh | Tỉ lệ | Độ dài | Số clip | Phong cách | Thể loại | Âm thanh |
|---|---|---|---|---|---|---|---|
| Omni 1.1 Flash (Flow, chế độ Thành phần) | Nano Banana 2.1 | 9:16 | ~14,5 giây, 8 nhát cắt | 4 clip × 8 giây, mỗi clip 2 hành động | đêm bãi đỗ sau mưa + lối vào nhà ban ngày | hype montage, không lời | tắt tiếng gốc, nhạc drill rap khi dựng |

**Lưu ý chung:**
- **Logo chiếu luôn lấy từ `product_projection.png`** (ảnh 1 trong thành phần của mọi cảnh có logo). Video chỉ làm nó sáng lên, mờ đi hoặc camera di chuyển; không để model tự vẽ logo.
- Mỗi clip gồm **2 nửa có hành động khác nhau** (0–4 s và 4–8 s); khi dựng mỗi nửa thành một nhát cắt.
- Mọi prompt có người/tay dán nguyên khoá **REALISM** và ghi rõ vị trí + đường đi so với xe và cửa (realism.md). Mọi cảnh soát theo `placement_checks` trong product.json.
- Prompt mô tả hình logo, không gọi tên đội. Xe không để lộ logo hãng.

## Các khóa (dán nguyên văn, không sửa chữ nào)

**PRODUCT (sản phẩm):**
a palm-sized matte black square projector unit with a small round lens on its underside, stuck under the inside door panel of a car near its bottom edge; when the door is open it projects a round logo onto the ground directly below the door edge: a blue outer ring, a thin white ring, and a red letter C wrapping the red block letters UBS on a white field, exactly as in the product photo

**CHARACTER - Mike (nhân vật):**
man in his early 40s, medium build, light skin, short dark-blond hair, light stubble, navy henley in the team's blue, long sleeves, dark jeans, plain royal-blue baseball cap with no logo

**REALISM (độ chân thực + vật lý, dán vào mọi prompt có người/tay):**
Real human being filmed on a phone: natural skin with pores and slight unevenness, real eyes with reflections, hair with individual strands, clothing that creases and hangs with weight. Every movement obeys physics: feet stay on the ground, weight shifts before a step, hands grip objects with correct finger placement and stay on their surfaces, bodies and clothes keep clear of the car, the door, the ground and each other, objects keep their size and weight. One continuous action at real speed.

**STYLE (cảnh đêm sau mưa):**
clean phone footage, vertical 9:16, an empty parking lot at night just after rain, dark asphalt with shallow puddles that mirror the lights, soft amber streetlights far in the background, a blue coupe with no visible badges or logos, a small red-and-blue pennant hanging from the rear-view mirror, deep natural contrast, real textures, no color grading

**STYLE - day (cảnh lắp ban ngày):**
clean phone footage, vertical 9:16, a home driveway in soft afternoon daylight, light grey concrete tiles, the same blue coupe with no visible badges or logos, a blue-and-red team pennant in the garage window behind, natural colours, real skin and fabric texture, no color grading

**AUDIO (mọi clip):** real sounds of the action, quiet ambience, no speech, no music

**NEGATIVE (chung):** subtitles, captions, on-screen text, watermark, misspelled or redrawn logo, flickering logo, extra logos, car brand badges, cinematic grading, music, plastic skin, airbrushed, beauty filter, uncanny face, extra fingers, fused fingers, distorted hands, extra limbs, body passing through the car or door, clipping through objects, floating objects, morphing, duplicated person, teleporting, sliding feet, warped background

## Bước 0 — Ảnh tham chiếu (có sẵn, không gen)

1. `frames/product_projection.png` — nguồn duy nhất của logo.
2. `frames/install_steps_row.png` — hộp đèn và tay thao tác thật.
3. `frames/mike_sheet.png` — nhân vật Mike (dùng lại).
4. `frames/car_night.png` — xe và ánh sáng đêm của các bản trước (giữ xe giống nhau).

## Bước 1 — Ảnh khung đầu (Nano Banana 2.1, 9:16)

### Keyframe 1 · cho clip 1 (hook) · Nano Banana 2.1
**Ảnh tải lên:** ảnh 1 = `product_projection.png`, ảnh 2 = `car_night.png` · **Lưu thành:** `keyframe_c1.png`

**Cảnh:** góc máy sát mặt đường ướt, cửa lái của coupe xanh **đang đóng**, đèn đường vàng phản chiếu trong vũng nước, mặt đất dưới cửa còn tối (chưa có logo) — khoảnh khắc ngay trước khi cửa mở.
```
Image 1 is the product's projected logo for reference only; in this frame the door is closed so the ground is dark and no logo is visible yet. Image 2 is the car and the night light to match.
Camera almost on the wet asphalt, outside the car, looking along the side of the blue coupe at its closed driver's door; shallow puddles mirror the amber streetlights; the ground below the door is dark. No person in frame.
clean phone footage, vertical 9:16, an empty parking lot at night just after rain, dark asphalt with shallow puddles that mirror the lights, soft amber streetlights far in the background, a blue coupe with no visible badges or logos, a small red-and-blue pennant hanging from the rear-view mirror, deep natural contrast, real textures, no color grading
Vertical 9:16, the door edge in the middle third, the wet ground filling the lower third, top 15% and bottom 20% kept clear. No text, no watermark.
```
**Soát trước khi làm video:** cửa đóng hẳn, đất tối, chưa có logo · vũng nước phản chiếu đèn · không có logo hãng xe · không có người · hộp đèn chưa nhìn thấy vì cửa đóng (under the inner door panel) · sẵn sàng cho logo hiện ngay dưới mép cửa khi mở (door open)

### Keyframe 2 · cho clip 2 · Nano Banana 2.1
**Ảnh tải lên:** ảnh 1 = `product_projection.png`, ảnh 2 = `mike_sheet.png`, ảnh 3 = `car_night.png` · **Lưu thành:** `keyframe_c2.png`

**Cảnh:** góc thấp đêm, cửa lái mở, logo nét ngay dưới mép cửa trên mặt đường ướt, chân phải Mike (giày tối, jeans) vừa đặt xuống cạnh logo, người cắt ngang hông, đứng ngoài xe.
```
Image 1 is the product: keep the projected ground logo exactly as in image 1, a blue outer ring, a thin white ring, a red letter C wrapping the red block letters UBS on a white field; do not redraw or retype it. Image 2 is the man's shoes, jeans and build. Image 3 is the car and the night light to match.
Low angle from the wet asphalt outside the blue coupe: the driver's door is open, a small black unit under the inner door panel projects the logo sharp onto the ground directly below the door edge, and the man's right foot in a dark sneaker and dark jeans has just landed on the asphalt next to the logo, not on it, his body cropped at the waist, standing on the ground outside the car.
Real human being filmed on a phone: natural skin with pores and slight unevenness, real eyes with reflections, hair with individual strands, clothing that creases and hangs with weight. Every movement obeys physics: feet stay on the ground, weight shifts before a step, hands grip objects with correct finger placement and stay on their surfaces, bodies and clothes keep clear of the car, the door, the ground and each other, objects keep their size and weight. One continuous action at real speed.
clean phone footage, vertical 9:16, an empty parking lot at night just after rain, dark asphalt with shallow puddles that mirror the lights, soft amber streetlights far in the background, a blue coupe with no visible badges or logos, a small red-and-blue pennant hanging from the rear-view mirror, deep natural contrast, real textures, no color grading
Vertical 9:16, the logo sharp in the lower third, the shoe beside it, the open door above, top 15% and bottom 20% kept clear. No text, no watermark.
```
**Soát trước khi làm video:** logo đúng hệt ảnh 1 từng nét · hộp đèn dưới mép tấm ốp cửa (under the inner door panel), ống kính hướng xuống · logo ngay dưới mép cửa mở (door open) · giày đặt cạnh logo, không đè · không có logo hãng xe

### Keyframe 3 · cho clip 3 · Nano Banana 2.1
**Ảnh tải lên:** ảnh 1 = `install_steps_row.png`, ảnh 2 = `mike_sheet.png` · **Lưu thành:** `keyframe_c3.png`

**Cảnh:** ban ngày, cận hai bàn tay Mike (tay áo henley xanh) cầm hộp đèn, ngón nhón một góc màng đỏ, cửa lái mở phía sau, cờ đuôi nheo trong cửa garage mờ phía xa.
```
Image 1 shows four real install photos; use the third one as the reference: two hands peeling a red film off the adhesive pad on the back of the black projector unit. Keep the unit's shape and the red film exactly as in image 1. Image 2 is the man: match his navy henley sleeves and skin.
Close-up of the man's two hands in navy henley sleeves, standing on the driveway outside the car beside the open driver's door, holding the unit at chest height in the left hand, the right fingers pinching one corner of the red film just starting to lift, the open door and dark inner door panel softly behind.
Real human being filmed on a phone: natural skin with pores and slight unevenness, real eyes with reflections, hair with individual strands, clothing that creases and hangs with weight. Every movement obeys physics: feet stay on the ground, weight shifts before a step, hands grip objects with correct finger placement and stay on their surfaces, bodies and clothes keep clear of the car, the door, the ground and each other, objects keep their size and weight. One continuous action at real speed.
clean phone footage, vertical 9:16, a home driveway in soft afternoon daylight, light grey concrete tiles, the same blue coupe with no visible badges or logos, a blue-and-red team pennant in the garage window behind, natural colours, real skin and fabric texture, no color grading
Close-up, vertical 9:16, the unit in the centre third, top 15% and bottom 20% kept clear. No text, no watermark, natural hands with five fingers.
```
**Soát trước khi làm video:** tay đủ ngón, tay áo henley xanh · màng đỏ đang bóc ở một góc · hộp đèn đúng hình · xe xanh, cửa mở phía sau · vị trí sẽ dán là dưới mép tấm ốp cửa (under the inner door panel), không phải ngưỡng cửa (sill) · cờ đuôi nheo mờ trong cửa garage

### Keyframe 4 · cho clip 4 · Nano Banana 2.1
**Ảnh tải lên:** ảnh 1 = `product_projection.png`, ảnh 2 = `mike_sheet.png`, ảnh 3 = `car_night.png` · **Lưu thành:** `keyframe_c4.png`

**Cảnh:** đêm, full shot góc thấp: Mike đứng ngoài xe cạnh cửa lái mở, cách ngưỡng cửa một bước, nhìn xuống logo nét dưới mép cửa; một người bạn nam áo khoác tối đứng ở đuôi xe, mờ, sắp đi tới.
```
Image 1 is the product: keep the projected ground logo exactly as in image 1, a blue outer ring, a thin white ring, a red letter C wrapping the red block letters UBS on a white field; do not redraw or retype it. Image 2 is the man; keep his face, cap and outfit. Image 3 is the car and the night light to match.
Man in his early 40s, medium build, light skin, short dark-blond hair, light stubble, navy henley in the team's blue, long sleeves, dark jeans, plain royal-blue baseball cap with no logo, standing on the wet asphalt outside the open driver's door, one step back from the sill, looking down at the logo projected sharp on the ground directly below the door edge; a second man in his 30s in a dark jacket stands at the rear of the car, out of focus, about to walk over along the outside of the door.
Real human being filmed on a phone: natural skin with pores and slight unevenness, real eyes with reflections, hair with individual strands, clothing that creases and hangs with weight. Every movement obeys physics: feet stay on the ground, weight shifts before a step, hands grip objects with correct finger placement and stay on their surfaces, bodies and clothes keep clear of the car, the door, the ground and each other, objects keep their size and weight. One continuous action at real speed.
clean phone footage, vertical 9:16, an empty parking lot at night just after rain, dark asphalt with shallow puddles that mirror the lights, soft amber streetlights far in the background, a blue coupe with no visible badges or logos, a small red-and-blue pennant hanging from the rear-view mirror, deep natural contrast, real textures, no color grading
Full shot from a low angle, vertical 9:16, the logo sharp in the lower third, the man and the open door above it, top 15% and bottom 20% kept clear. Two people only, one in focus, no text, no watermark, natural hands with five fingers.
```
**Soát trước khi làm video:** logo đúng hệt ảnh 1 · logo ngay dưới mép cửa mở (door open), hộp đèn dưới tấm ốp cửa (under the inner door panel) · Mike đứng ngoài xe, không đứng trên ngưỡng (sill) · bạn ở đuôi xe, mờ · mặt và mũ giống sheet · không có logo hãng xe

## Bước 2 — Prompt video (Omni 1.1 Flash, chế độ Thành phần, 8 giây, 9:16)

## Clip 1 · 8s · Hook: cửa bung → logo bừng sáng
**Khung đầu (ingredients):** `keyframe_c1.png` · **Lưu video thành:** `c01_a.mp4`

**Cảnh:** nửa đầu cửa lái bung ra chậm, chùm sáng từ hộp đèn dưới tấm ốp bật lên, logo hiện và nét dần trên mặt đường ướt ngay dưới mép cửa, phản chiếu trong vũng nước; nửa sau camera đẩy chậm vào logo, logo đứng yên và nét. Không có người.
```
Camera almost on the wet asphalt outside the blue coupe, slow push in; the car has a plain steering wheel centre and plain wheel hubs with no emblem anywhere. In the first half the closed driver's door swings open outward at real speed; as it opens, a small black unit under the inner door panel lights up and projects the logo onto the ground directly below the door edge, the logo blooming from faint to sharp and bright, its colours mirrored in the shallow puddle beside it. In the second half the door stays open and the camera keeps moving slowly toward the logo until it fills most of the lower frame; the logo stays perfectly still, sharp and identical in every frame. No person in frame.
Audio: a car door latch and hinge, a drip of water, quiet night ambience, no speech, no music. No subtitles, no on-screen text.
```
**Phủ định (Negative):** `subtitles, captions, on-screen text, watermark, misspelled or redrawn logo, flickering logo, extra logos, car brand badges, emblem on the steering wheel, emblem on the wheel hubs, people, music, morphing, warped background`
**Soát clip:** cửa đóng ở giây 0, đất tối; logo chỉ hiện khi cửa mở và nằm ngay dưới mép cửa (door open) · hộp đèn dưới tấm ốp cửa (under the inner door panel), ống kính hướng xuống · logo đúng hệt ảnh gốc, không nhoè, không đổi · không có người

## Clip 2 · 8s · Bước xuống → đứng nhìn
**Khung đầu (ingredients):** `keyframe_c2.png`, `mike_sheet.png` · **Lưu video thành:** `c02_a.mp4`

**Cảnh:** nửa đầu chân trái Mike bước xuống theo, đặt cạnh logo, hai chân ngoài xe; nửa sau camera nghiêng lên theo người đứng thẳng, Mike đứng ngoài cửa, mũ xanh, cúi nhìn logo và gật đầu nhẹ.
```
Low angle from the wet asphalt, slow tilt up. In the first half the man steps out of the car: his right foot is already planted on dark asphalt between the camera and the logo, a full shoe-length nearer the camera than the logo's edge; his left foot follows and lands beside the right one on the same dark patch, so both shoes stay on plain asphalt in front of the logo and no shoe ever touches or covers any part of the logo ring; his navy henley stays navy, his legs straightening as he stands up outside the open door. In the second half the camera tilts slowly up his body to his face: he stands on the ground outside the door, one step from the sill, looks down at the logo and gives a small satisfied nod. The logo on the ground stays sharp, still and identical in every frame.
Real human being filmed on a phone: natural skin with pores and slight unevenness, real eyes with reflections, hair with individual strands, clothing that creases and hangs with weight. Every movement obeys physics: feet stay on the ground, weight shifts before a step, hands grip objects with correct finger placement and stay on their surfaces, bodies and clothes keep clear of the car, the door, the ground and each other, objects keep their size and weight. One continuous action at real speed.
Audio: a shoe on wet asphalt, quiet night ambience, no speech, no music. No subtitles, no on-screen text.
```
**Phủ định (Negative):** `subtitles, captions, misspelled or redrawn logo, flickering logo, extra logos, car brand badges, music, plastic skin, airbrushed, beauty filter, uncanny face, extra fingers, fused fingers, distorted hands, extra limbs, body passing through the car or door, clipping through objects, floating objects, morphing, duplicated person, teleporting, sliding feet, warped background`
**Soát clip:** logo ngay dưới mép cửa mở (door open), đúng hệt ảnh gốc ở mọi giây · hộp đèn dưới tấm ốp cửa (under the inner door panel) · hai chân ngoài xe cạnh logo, không đè, không xuyên ngưỡng (sill) · mũ royal-blue, henley xanh giống sheet suốt clip

## Clip 3 · 8s · Bóc keo → dán (ban ngày)
**Khung đầu (ingredients):** `keyframe_c3.png`, `mike_sheet.png`, `car_night.png` · **Lưu video thành:** `c03_a.mp4`

**Cảnh:** nửa đầu bóc hết màng đỏ một đường; nửa sau camera nghiêng lên dưới tấm ốp cửa, tay đưa hộp đèn từ ngoài vào, ấn phẳng lên mặt dưới tấm ốp bằng lòng bàn tay, giữ rồi buông, hộp dính chắc.
```
Close-up, slow tilt up. The man stands on the driveway outside the car beside the open driver's door, holding the unit in his left hand at chest height, his navy henley sleeves visible. In the first half his right fingers pinch one corner of the red film and peel it off the adhesive pad in one smooth pull. In the second half the camera tilts to the lowest part of the inner door panel of the blue car, just above the sill and far below the armrest and door handle; he brings the unit to that lowest edge from the outside, presses it flat against the underside of the panel's bottom lip with his right palm so the lens faces the ground, holds it for a moment, then lets go; the unit stays stuck at the very bottom of the panel, lens pointing down, nothing passes into the panel.
Real human being filmed on a phone: natural skin with pores and slight unevenness, real eyes with reflections, hair with individual strands, clothing that creases and hangs with weight. Every movement obeys physics: feet stay on the ground, weight shifts before a step, hands grip objects with correct finger placement and stay on their surfaces, bodies and clothes keep clear of the car, the door, the ground and each other, objects keep their size and weight. One continuous action at real speed.
Audio: soft peel of the film, a firm press, quiet driveway ambience, no speech, no music. No subtitles, no on-screen text.
```
**Phủ định (Negative):** `subtitles, captions, unit falling, fast motion, music, plastic skin, airbrushed, beauty filter, uncanny face, extra fingers, fused fingers, distorted hands, extra limbs, body passing through the car or door, clipping through objects, floating objects, morphing, duplicated person, teleporting, sliding feet, warped background`
**Soát clip:** hộp đèn được ấn vào mặt dưới tấm ốp cửa (under the inner door panel), ống kính hướng xuống, không dán lên ngưỡng cửa/ghế (sill, seat) · tay đủ ngón, không xuyên tấm ốp · tay áo henley xanh, xe xanh đúng khoá suốt clip

## Clip 4 · 8s · Bạn tới xem → đóng cửa
**Khung đầu (ingredients):** `keyframe_c4.png`, `mike_sheet.png` · **Lưu video thành:** `c04_a.mp4`

**Cảnh:** nửa đầu bạn đi từ đuôi xe vòng theo mép ngoài cửa, dừng cạnh Mike ở phía cửa mở, chỉ xuống logo; nửa sau Mike đóng cửa bằng tay phải, logo mờ dần rồi tắt, hai người đứng yên.
```
Low-angle full shot, static. Two people only. The man stands on the wet asphalt outside the open driver's door, one step back from the sill, looking down at the logo. In the first half his friend, a man in his 30s in a dark jacket, walks from the rear of the car along the outside of the door, stops beside the man on the open side of the door and points down at the logo, impressed; he never passes the door or the sill. In the second half the man reaches the door edge with his right hand and swings the door shut; the logo on the asphalt fades out smoothly as the door closes, leaving dark wet ground, both men still standing in place.
Real human being filmed on a phone: natural skin with pores and slight unevenness, real eyes with reflections, hair with individual strands, clothing that creases and hangs with weight. Every movement obeys physics: feet stay on the ground, weight shifts before a step, hands grip objects with correct finger placement and stay on their surfaces, bodies and clothes keep clear of the car, the door, the ground and each other, objects keep their size and weight. One continuous action at real speed.
Audio: footsteps on wet asphalt, a car door closing, quiet night ambience, no speech, no music. No subtitles, no on-screen text.
```
**Phủ định (Negative):** `subtitles, captions, misspelled or redrawn logo, extra logos, car brand badges, extra people in focus, music, plastic skin, airbrushed, beauty filter, uncanny face, extra fingers, fused fingers, distorted hands, extra limbs, body passing through the car or door, clipping through objects, floating objects, morphing, duplicated person, teleporting, sliding feet, warped background`
**Soát clip:** logo ngay dưới mép cửa mở (door open), đúng hệt ảnh gốc; đất tối khi cửa đóng (door closed) · hộp đèn dưới tấm ốp cửa (under the inner door panel) · bạn đi vòng ngoài cửa, không xuyên cửa/ngưỡng (sill); hai người đứng ngoài xe · mũ và áo Mike giống sheet, đúng 2 người

## Thiết lập khi gen video
- Cả 4 clip: Omni 1.1 Flash, chế độ **Thành phần** (ingredients): ảnh sản phẩm/hình in trước, keyframe sau, rồi sheet nhân vật; 8 giây, dọc 9:16, tải **1080p** (không chọn tuỳ chọn tính tín dụng).
- Tiếng clip không dùng: video dùng nhạc drill rap khi dựng.
- Sau mỗi stage: `gen_review.py cubs-door-light-rap`, soát theo `placement_checks`, đánh dấu pass/fail trước khi sang stage sau.
