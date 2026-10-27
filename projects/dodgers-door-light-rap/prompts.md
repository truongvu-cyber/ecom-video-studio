# Đèn chiếu logo cửa xe (Dodgers) — hype rap, hook mở cửa phát sáng — prompt tạo ảnh và video

Phần mô tả, hướng dẫn và ghi chú viết bằng tiếng Việt. Phần prompt (trong khung code) và các khóa giữ bằng tiếng Anh: **copy nguyên văn, không dịch**.

| Công cụ video | Công cụ ảnh | Tỉ lệ | Độ dài | Số clip | Phong cách | Thể loại | Âm thanh |
|---|---|---|---|---|---|---|---|
| Omni 1.1 Flash (Flow, chế độ Thành phần) | Nano Banana 2.1 | 9:16 | ~15 giây, 8 nhát cắt | 4 clip × 8 giây, mỗi clip 2 hành động | bãi đỗ LA đêm sau trận, hàng cọ + đèn sân xa; garage ban ngày | hype montage, không lời | tắt tiếng gốc, nhạc rap 120–160 BPM khi dựng |

**Lưu ý chung:**
- **Logo chiếu luôn lấy từ `product_projection.png`** (ảnh 1 trong thành phần của mọi cảnh có logo). Chữ Dodgers script xanh, bóng chày trắng chỉ đỏ phía trên chữ g, vệt tốc độ đỏ. Video chỉ làm nó sáng lên, mờ đi hoặc camera di chuyển; không để model tự vẽ logo.
- Ảnh sản phẩm có chữ quảng cáo ("Rep your team…", "60-sec install", huy hiệu) — đó là chữ của listing, **không** đưa vào cảnh.
- Logo đọc đúng chiều với người đứng ngoài xe nhìn vào cửa; mặt đường ướt chỉ **lấp lánh**, không có vũng nước phản chiếu ngược chữ.
- **Shot 1 là trigger**: cửa đã đang mở ở frame đầu, logo bừng lên ngay — không mở bằng cửa đóng/đất tối.
- Mỗi clip 2 nửa hành động khác nhau (0–4 s, 4–8 s). Mọi prompt có người dán khoá **REALISM**, ghi rõ vị trí so với xe/cửa; người luôn đứng ngoài xe.
- Dre là người mới của project này, sheet gen riêng ở Bước 0 (ảnh chụp thật). Xe lấy từ `keyframe_c1.png` cho mọi cảnh sau. Xe không lộ logo hãng.

## Các khóa (dán nguyên văn, không sửa chữ nào)

**PRODUCT (sản phẩm):**
a palm-sized matte black square projector unit with a small round lens on its underside, stuck under the inside door panel of a car near its bottom edge; when the door is open it projects a logo onto the ground directly below and just outside the door edge: the word Dodgers in flowing blue script, a white baseball with red stitches above the letter g, red speed lines trailing from the ball and under the script, exactly as in the product photo, reading left to right

**CHARACTER - Dre (nhân vật):**
Latino man in his late 20s, lean build, light-brown skin, short black skin-fade haircut, thin moustache, a small script tattoo on the right forearm, a thin silver chain, royal-blue baseball cap with white interlocking letters L and A on the front, flat brim, white baseball jersey with the word Dodgers in blue script across the chest and a red number below it, worn open over a plain black tee, black cargo pants, clean white sneakers

**REALISM (độ chân thực + vật lý, dán vào mọi prompt có người/tay):**
Real human being filmed on a phone: natural skin with pores and slight unevenness, real eyes with reflections, hair with individual strands, clothing that creases and hangs with weight. Every movement obeys physics: feet stay on the ground, weight shifts before a step, hands grip objects with correct finger placement and stay on their surfaces, bodies and clothes keep clear of the car, the door, the ground and each other, objects keep their size and weight. One continuous action at real speed.

**STYLE (đêm sau trận):**
clean phone footage at night, vertical 9:16, a parking lot after the game, dark asphalt still wet and glistening, tall palm trees and a distant stadium glowing with white floodlights on the horizon, a glossy black sedan with dark tinted windows and no visible badges or logos, a royal-blue rally towel hanging from the rear-view mirror, deep natural contrast, real textures, no color grading

**STYLE - day (garage ban ngày):**
clean phone footage, vertical 9:16, a home driveway in front of an open garage in soft Los Angeles afternoon daylight, light concrete, a palm tree at the edge of frame, the same glossy black sedan with no visible badges or logos, a royal-blue rally towel hanging from the rear-view mirror, natural colours, real skin and fabric texture, no color grading

**AUDIO (mọi clip):** real sounds of the action, quiet ambience, no speech, no music

**NEGATIVE (chung):** subtitles, captions, on-screen text, watermark, misspelled or redrawn logo, mirrored logo, logo reflection in a puddle, flickering logo, extra logos, car brand badges, cinematic grading, music, plastic skin, airbrushed, beauty filter, uncanny face, extra fingers, fused fingers, distorted hands, extra limbs, body passing through the car or door, clipping through objects, floating objects, morphing, duplicated person, teleporting, sliding feet, warped background

## Bước 0 — Ảnh tham chiếu

1. `frames/product_projection.png` — nguồn duy nhất của logo và hình hộp đèn.
2. `frames/install_steps_grid.png` — 4 ảnh lắp thật (pin, lau, bóc màng đỏ, dán).
3. **Ảnh nhân vật Dre (gen mới cho project này, ảnh chụp thật):**
   ```
   Photograph, character reference sheet, one image, 16:9: a real person photographed in a studio, three full-body views (front, side, back) on the left, one chest-up close-up on the right, plain light-grey background, even soft light, real skin and fabric texture, cool confident look at the lens, no illustration, not a cartoon, no 3D render, no CGI. Latino man in his late 20s, lean build, light-brown skin, short black skin-fade haircut, thin moustache, a small script tattoo on the right forearm, a thin silver chain, royal-blue baseball cap with white interlocking letters L and A on the front, flat brim, white baseball jersey with the word Dodgers in blue script across the chest and a red number below it, worn open over a plain black tee, black cargo pants, clean white sneakers. No other text, no watermark.
   ```
   **Lưu thành:** `dre_sheet.png`

## Bước 1 — Ảnh khung đầu (Nano Banana 2.1, 9:16)

### Keyframe 1 · cho clip 1 (hook) · Nano Banana 2.1
**Ảnh tải lên:** ảnh 1 = `product_projection.png` · **Lưu thành:** `keyframe_c1.png`

**Cảnh:** góc máy sát mặt đường ướt, ngoài xe; cửa lái sedan đen **đã mở một phần ba và đang bung ra**, chùm sáng trắng từ hộp đèn dưới tấm ốp vừa bật, logo Dodgers đã hiện sáng rõ dưới mép cửa; hàng cọ và đèn sân vận động phía xa. Không người.
```
Image 1 is the product: keep the projected ground logo exactly as in image 1, the word Dodgers in flowing blue script, a white baseball with red stitches above the letter g, red speed lines; do not redraw or retype it, and ignore every caption, badge and headline printed on image 1.
Camera almost on the wet asphalt, outside the glossy black sedan, looking at its driver's door swinging open, already a third open; a small black unit under the inner door panel near its bottom edge shines a cone of white light down, and the logo glows bright and sharp on the glistening asphalt directly below and just outside the door edge, reading left to right toward the camera. No person in frame.
clean phone footage at night, vertical 9:16, a parking lot after the game, dark asphalt still wet and glistening, tall palm trees and a distant stadium glowing with white floodlights on the horizon, a glossy black sedan with dark tinted windows and no visible badges or logos, a royal-blue rally towel hanging from the rear-view mirror, deep natural contrast, real textures, no color grading
Vertical 9:16, the logo in the lower-middle third, the door edge above it, top 15% and bottom 20% kept clear. No puddle reflection of the logo, no other text, no watermark.
```
**Soát trước khi làm video:** logo đúng hệt ảnh 1 (Dodgers script xanh, bóng chỉ đỏ trên chữ g), đọc đúng chiều, không ngược (never mirrored) · hộp đèn dưới mép tấm ốp cửa (under the inner door panel), ống kính hướng xuống · logo ngay dưới-ngoài mép cửa mở (door open), không dưới ghế/bánh · không có chữ listing, không logo hãng xe · khăn rally xanh ở gương, cọ + đèn sân thấy được

### Keyframe 2 · cho clip 2 · Nano Banana 2.1
**Ảnh tải lên:** ảnh 1 = `product_projection.png`, ảnh 2 = `dre_sheet.png`, ảnh 3 = `keyframe_c1.png` · **Lưu thành:** `keyframe_c2.png`

**Cảnh:** góc thấp đêm, cửa lái mở hẳn, logo nét dưới mép cửa; giày trắng của Dre vừa đặt xuống mặt đường **cạnh** logo (không đè), người cắt ngang hông, đứng ngoài xe; quần cargo đen.
```
Image 1 is the product: keep the projected ground logo exactly as in image 1, the word Dodgers in flowing blue script, a white baseball with red stitches above the letter g, red speed lines; do not redraw or retype it, and ignore every caption, badge and headline printed on image 1. Image 2 is the man: match his white sneakers, black cargo pants and the open white jersey hem. Image 3 is the car, the logo position and the night light to match.
Low angle from the wet asphalt outside the glossy black sedan: the driver's door is fully open, the small black unit under the inner door panel projects the logo sharp onto the ground directly below and just outside the door edge, and the man's right foot in a clean white sneaker has just landed on the asphalt beside the logo, not on it, his body cropped at the waist, the hem of the open white jersey and the black tee visible, standing on the ground outside the car.
Real human being filmed on a phone: natural skin with pores and slight unevenness, real eyes with reflections, hair with individual strands, clothing that creases and hangs with weight. Every movement obeys physics: feet stay on the ground, weight shifts before a step, hands grip objects with correct finger placement and stay on their surfaces, bodies and clothes keep clear of the car, the door, the ground and each other, objects keep their size and weight. One continuous action at real speed.
clean phone footage at night, vertical 9:16, a parking lot after the game, dark asphalt still wet and glistening, tall palm trees and a distant stadium glowing with white floodlights on the horizon, a glossy black sedan with dark tinted windows and no visible badges or logos, a royal-blue rally towel hanging from the rear-view mirror, deep natural contrast, real textures, no color grading
Vertical 9:16, the logo sharp in the lower third, the sneaker beside it, the open door above, top 15% and bottom 20% kept clear. No puddle reflection of the logo, no other text, no watermark.
```
**Soát trước khi làm video:** logo đúng hệt ảnh 1, không ngược (never mirrored) · hộp đèn dưới tấm ốp cửa (under the inner door panel) · logo dưới-ngoài mép cửa mở (door open) · giày trắng cạnh logo, không đè, đứng ngoài xe (outside the car) · không logo hãng xe

### Keyframe 3 · cho clip 3 · Nano Banana 2.1
**Ảnh tải lên:** ảnh 1 = `install_steps_grid.png`, ảnh 2 = `dre_sheet.png`, ảnh 3 = `keyframe_c1.png` · **Lưu thành:** `keyframe_c3.png`

**Cảnh:** ban ngày, cận hai bàn tay Dre (hình xăm cẳng tay phải, vạt jersey trắng mở thấy ở mép) cầm hộp đèn, ngón nhón một góc màng đỏ; cửa lái sedan đen mở phía sau, garage và cây cọ mờ xa.
```
Image 1 shows four real install photos; use the third one (Remove Backing) as the reference: two hands peeling a red film off the adhesive pad on the back of the black projector unit. Keep the unit's shape and the red film exactly as in image 1 and ignore the captions and numbers on it. Image 2 is the man: match his light-brown skin, forearm tattoo, open white jersey and black tee. Image 3 is the car to match, now in daylight.
Close-up of the man's two hands, the small script tattoo on his right forearm, the open white jersey with blue script just visible at the edge of frame, standing on the driveway outside the car beside the open driver's door, holding the unit at chest height in the left hand, the right fingers pinching one corner of the red film just starting to lift, the open door and dark inner door panel softly behind.
Real human being filmed on a phone: natural skin with pores and slight unevenness, real eyes with reflections, hair with individual strands, clothing that creases and hangs with weight. Every movement obeys physics: feet stay on the ground, weight shifts before a step, hands grip objects with correct finger placement and stay on their surfaces, bodies and clothes keep clear of the car, the door, the ground and each other, objects keep their size and weight. One continuous action at real speed.
clean phone footage, vertical 9:16, a home driveway in front of an open garage in soft Los Angeles afternoon daylight, light concrete, a palm tree at the edge of frame, the same glossy black sedan with no visible badges or logos, a royal-blue rally towel hanging from the rear-view mirror, natural colours, real skin and fabric texture, no color grading
Close-up, vertical 9:16, the unit in the centre third, top 15% and bottom 20% kept clear. No text, no watermark, natural hands with five fingers.
```
**Soát trước khi làm video:** tay đủ ngón, hình xăm cẳng tay phải, vạt jersey trắng · màng đỏ đang bóc ở một góc · hộp đèn đúng hình · sedan đen cửa mở phía sau, đứng ngoài xe (outside the car) · vị trí sẽ dán dưới tấm ốp cửa (under the inner door panel), không phải ngưỡng cửa (sill) · khăn rally xanh ở gương

### Keyframe 4 · cho clip 4 · Nano Banana 2.1
**Ảnh tải lên:** ảnh 1 = `product_projection.png`, ảnh 2 = `dre_sheet.png`, ảnh 3 = `keyframe_c1.png` · **Lưu thành:** `keyframe_c4.png`

**Cảnh:** đêm, full shot góc thấp từ phía sau-lệch của Dre: Dre đứng ngoài xe cạnh cửa lái mở, cách ngưỡng một bước, tay phải đặt trên mép cửa, logo nét dưới mép cửa trước mũi giày; đèn sân và cọ phía xa.
```
Image 1 is the product: keep the projected logo exactly as in image 1, ignore its captions and badges. Image 2 is the man; keep his face, cap, chain and outfit. Image 3 is the car and night light.
Latino man in his late 20s, lean build, light-brown skin, short black skin-fade haircut, thin moustache, a small script tattoo on the right forearm, a thin silver chain, royal-blue baseball cap with white interlocking letters L and A on the front, flat brim, white baseball jersey with the word Dodgers in blue script across the chest and a red number below it, worn open over a plain black tee, black cargo pants, clean white sneakers, standing on the wet asphalt outside the open driver's door, one step back from the sill, right hand on the top of the door edge, looking down at the logo sharp on the ground just below and outside the door edge, in front of his sneakers.
Real human being filmed on a phone: natural skin with pores and slight unevenness, real eyes with reflections, hair with individual strands, clothing that creases and hangs with weight. Every movement obeys physics: feet stay on the ground, weight shifts before a step, hands grip objects with correct finger placement and stay on their surfaces, bodies and clothes keep clear of the car, the door, the ground and each other, objects keep their size and weight. One continuous action at real speed.
clean phone footage at night, vertical 9:16, a parking lot after the game, dark asphalt still wet and glistening, tall palm trees and a distant stadium glowing with white floodlights on the horizon, a glossy black sedan with dark tinted windows and no visible badges or logos, a royal-blue rally towel hanging from the rear-view mirror, deep natural contrast, real textures, no color grading
Full shot from a low angle, vertical 9:16, the logo sharp in the lower third, the man and the open door above it, top 15% and bottom 20% kept clear. One person only, no puddle reflection of the logo, no other text, no watermark, natural hands with five fingers.
```
**Soát trước khi làm video:** logo đúng hệt ảnh 1, không ngược (never mirrored) · logo dưới-ngoài mép cửa mở (door open), hộp đèn dưới tấm ốp cửa (under the inner door panel) · Dre đứng ngoài xe, không trên ngưỡng (sill) · mặt, mũ LA, jersey Dodgers mở giống sheet · không logo hãng xe

## Bước 2 — Prompt video (Omni 1.1 Flash, chế độ Thành phần, 8 giây, 9:16)

## Clip 1 · 8s · Hook: cửa đang bung → logo bừng sáng (drop)
**Khung đầu (ingredients):** `keyframe_c1.png` · **Lưu video thành:** `c01_a.mp4`

**Cảnh:** nửa đầu cửa lái đang bung tiếp từ một phần ba tới mở hẳn, chùm sáng mạnh lên, logo bừng từ sáng vừa tới nét căng; nửa sau camera đẩy chậm vào logo đến khi logo chiếm phần dưới khung, hơi nước mỏng bay ngang ánh sáng. Không người.
```
Night. Camera almost on the wet asphalt outside the glossy black sedan, slow push in; the car has a plain steering wheel centre and plain wheel hubs with no emblem anywhere. From the very first frame the driver's door is already swinging open: in the first half it keeps swinging from a third open to fully open at real speed, the small black unit under the inner door panel shines brighter, and the logo on the glistening asphalt directly below and just outside the door edge blooms from glowing to sharp and brilliant: the word Dodgers in flowing blue script, the white baseball with red stitches above the letter g, red speed lines. In the second half the door stays open and the camera keeps moving slowly toward the logo until it fills most of the lower frame, a thin wisp of mist drifting through the light cone; the logo stays perfectly still, sharp, reading left to right and identical in every frame. No person in frame.
Audio: a car door hinge, a soft electronic click, quiet night ambience with a distant crowd, no speech, no music. No subtitles, no on-screen text.
```
**Phủ định (Negative):** `subtitles, captions, on-screen text, watermark, misspelled or redrawn logo, mirrored logo, logo reflection in a puddle, flickering logo, extra logos, car brand badges, emblem on the steering wheel, emblem on the wheel hubs, people, music, morphing, warped background`
**Soát clip:** cửa đang mở ở giây 0, logo hiện ngay (door open) và nằm dưới-ngoài mép cửa · hộp đèn dưới tấm ốp cửa (under the inner door panel), ống kính hướng xuống · logo Dodgers đúng hệt ảnh gốc, đọc đúng chiều (never mirrored), không nhoè, không đổi chữ · không có người

## Clip 2 · 8s · Bước xuống → đứng nhìn → bạn tới
**Khung đầu (ingredients):** `keyframe_c2.png`, `dre_sheet.png` · **Lưu video thành:** `c02_a.mp4`

**Cảnh:** nửa đầu chân thứ hai của Dre đặt xuống cạnh logo, camera nghiêng lên theo người đứng thẳng ngoài cửa, mũ LA, jersey mở, nhìn xuống logo rồi gật đầu; nửa sau bạn Nico (hoodie royal-blue, mũ đen) đi từ đuôi xe dọc mép ngoài cửa tới cạnh Dre, chỉ xuống logo, hai người đập tay.
```
Night. Low angle from the wet asphalt, slow tilt up. Both of the man's white sneakers are planted on the asphalt beside the logo, never on it, and he never steps over the sill. In the first half he rises to standing outside the open driver's door, his open white Dodgers jersey hanging over the black tee, the royal-blue LA cap and silver chain coming into frame as the camera tilts up to his face; he looks down at the logo and gives one slow nod. In the second half his friend, a man in his late 20s in a royal-blue hoodie and a plain black cap, walks from the rear of the car along the outside of the open door, stops beside him on the open side of the door, points down at the logo, and the two bump fists; nobody passes through the door or the sill. The logo on the ground stays sharp, still and identical in every frame: the word Dodgers in flowing blue script, the white baseball with red stitches, red speed lines.
Real human being filmed on a phone: natural skin with pores and slight unevenness, real eyes with reflections, hair with individual strands, clothing that creases and hangs with weight. Every movement obeys physics: feet stay on the ground, weight shifts before a step, hands grip objects with correct finger placement and stay on their surfaces, bodies and clothes keep clear of the car, the door, the ground and each other, objects keep their size and weight. One continuous action at real speed.
Audio: sneakers on wet asphalt, a fist bump, quiet night ambience with a distant crowd, no speech, no music. No subtitles, no on-screen text.
```
**Phủ định (Negative):** `subtitles, captions, misspelled or redrawn logo, mirrored logo, logo reflection in a puddle, flickering logo, extra logos, car brand badges, music, plastic skin, airbrushed, beauty filter, uncanny face, extra fingers, fused fingers, distorted hands, extra limbs, body passing through the car or door, clipping through objects, floating objects, morphing, duplicated person, teleporting, sliding feet, warped background`
**Soát clip:** logo dưới-ngoài mép cửa mở (door open), đúng hệt ảnh gốc mọi giây, không ngược (never mirrored) · hộp đèn dưới tấm ốp cửa (under the inner door panel) · hai người đứng ngoài xe (outside the car), không đè logo, không xuyên ngưỡng (sill) · mũ LA, jersey Dodgers mở giống sheet suốt clip

## Clip 3 · 8s · Bóc keo → dán (ban ngày)
**Khung đầu (ingredients):** `keyframe_c3.png`, `dre_sheet.png`, `install_steps_grid.png` · **Lưu video thành:** `c03_a.mp4`

**Cảnh:** nửa đầu bóc hết màng đỏ một đường; nửa sau camera nghiêng xuống mép dưới tấm ốp trong cửa, tay đưa hộp đèn từ ngoài vào, ấn phẳng vào mặt dưới mép tấm ốp bằng lòng bàn tay, giữ rồi buông — dính chắc.
```
Daylight. Close-up, slow tilt. The man stands on the driveway outside the car beside the open driver's door of the glossy black sedan, holding the unit in his left hand at chest height, the script tattoo on his right forearm visible. In the first half his right fingers pinch one corner of the red film and peel it off the adhesive pad in one smooth pull. In the second half the camera tilts to the lowest part of the inner door panel, just above the sill and far below the armrest and door handle; he brings the unit to that lowest edge from the outside, presses it flat against the underside of the panel's bottom lip with his right palm so the lens faces the ground, holds it for a moment, then lets go; the unit stays stuck at the very bottom of the panel, lens pointing down, nothing passes into the panel.
Real human being filmed on a phone: natural skin with pores and slight unevenness, real eyes with reflections, hair with individual strands, clothing that creases and hangs with weight. Every movement obeys physics: feet stay on the ground, weight shifts before a step, hands grip objects with correct finger placement and stay on their surfaces, bodies and clothes keep clear of the car, the door, the ground and each other, objects keep their size and weight. One continuous action at real speed.
Audio: soft peel of the film, a firm press, quiet driveway ambience, no speech, no music. No subtitles, no on-screen text.
```
**Phủ định (Negative):** `subtitles, captions, on-screen text, unit falling, fast motion, music, plastic skin, airbrushed, beauty filter, uncanny face, extra fingers, fused fingers, distorted hands, extra limbs, body passing through the car or door, clipping through objects, floating objects, morphing, duplicated person, teleporting, sliding feet, warped background`
**Soát clip:** hộp đèn ấn vào mặt dưới tấm ốp cửa (under the inner door panel), ống kính hướng xuống, không dán lên ngưỡng cửa/ghế (sill, seat) · tay đủ ngón, không xuyên tấm ốp · hình xăm, xe đen đúng khoá suốt clip

## Clip 4 · 8s · Đóng cửa → mở lại → CTA
**Khung đầu (ingredients):** `keyframe_c4.png`, `dre_sheet.png` · **Lưu video thành:** `c04_a.mp4`

**Cảnh:** nửa đầu Dre đóng cửa bằng tay phải, logo tắt, đất tối; rồi mở lại, logo bừng lần nữa; nửa sau Dre nhìn thẳng ống kính, nhếch mép, chỉ tay xuống logo.
```
Night. Low-angle full shot, static. One person only. The man, wearing the royal-blue LA cap, the silver chain and the white Dodgers jersey open over the black tee exactly as in the character reference, stands on the wet asphalt outside the open driver's door, one step back from the sill, his right hand on the top of the door edge. In the first half he swings the door closed: the logo on the asphalt fades out as the door shuts, leaving dark wet ground; then he pulls the door open again and the logo blooms back sharp directly below and just outside the door edge. In the second half he looks straight into the lens with a small confident smirk and points down at the logo with his right index finger; his feet stay planted beside the logo, never on it. The logo is the word Dodgers in flowing blue script, the white baseball with red stitches above the letter g, red speed lines, identical every time it is visible.
Real human being filmed on a phone: natural skin with pores and slight unevenness, real eyes with reflections, hair with individual strands, clothing that creases and hangs with weight. Every movement obeys physics: feet stay on the ground, weight shifts before a step, hands grip objects with correct finger placement and stay on their surfaces, bodies and clothes keep clear of the car, the door, the ground and each other, objects keep their size and weight. One continuous action at real speed.
Audio: a car door closing and opening, quiet night ambience with a distant crowd, no speech, no music. No subtitles, no on-screen text.
```
**Phủ định (Negative):** `subtitles, captions, misspelled or redrawn logo, mirrored logo, logo reflection in a puddle, extra logos, car brand badges, extra people, music, plastic skin, airbrushed, beauty filter, uncanny face, extra fingers, fused fingers, distorted hands, extra limbs, body passing through the car or door, clipping through objects, floating objects, morphing, duplicated person, teleporting, sliding feet, warped background`
**Soát clip:** logo chỉ hiện khi cửa mở (door open), đất tối khi cửa đóng (door closed) · logo dưới-ngoài mép cửa, đúng hệt ảnh gốc, không ngược (never mirrored) · hộp đèn dưới tấm ốp cửa (under the inner door panel) · Dre đứng ngoài xe (outside the car), không trên ngưỡng (sill) · mũ, dây chuyền, jersey giống sheet, đúng 1 người

## Thiết lập khi gen video
- Cả 4 clip: Omni 1.1 Flash, chế độ **Thành phần** (ingredients): ảnh sản phẩm/hình in trước, keyframe sau, rồi sheet nhân vật; 8 giây, dọc 9:16, tải **1080p** (không chọn tuỳ chọn tính tín dụng).
- Tiếng clip không dùng: video dùng nhạc rap khi dựng.
- Sau mỗi stage: `gen_review.py dodgers-door-light-rap`, soát theo `placement_checks`, đánh dấu pass/fail trước khi dựng.
