# Jersey Brew Crew Uecker #9 powder blue — unbox nhanh, mẫu Sienna — prompt tạo ảnh và video

Phần mô tả, hướng dẫn và ghi chú viết bằng tiếng Việt. Phần prompt (trong khung code) và các khóa giữ bằng tiếng Anh: **copy nguyên văn, không dịch**.

| Công cụ video | Công cụ ảnh | Tỉ lệ | Độ dài | Số clip | Phong cách | Thể loại | Âm thanh |
|---|---|---|---|---|---|---|---|
| Omni 1.1 Flash (Flow, chế độ Thành phần) | Nano Banana 2.1 | 9:16 | ~15 giây, 8 nhát cắt | 4 clip × 8 giây, mỗi clip 2 hành động | phòng ngủ fan buổi tối, đèn dây | unbox nhanh + try-on, không lời | tắt tiếng gốc, nhạc sports rap 120–160 BPM khi dựng |

**Lưu ý chung:**
- **Mọi chữ và patch trên áo lấy từ `product.png`** (ảnh 1 trong thành phần của mọi cảnh thấy áo). Không để model tự vẽ chữ: Brew Crew, UECKER, 9, World Series 2026, NATIONAL LEAGUE CHAMPIONS 2026 phải đúng từng chữ. Áo mở cúc làm chữ tách là tự nhiên.
- Hai patch to ở đáy ảnh sản phẩm là ảnh minh hoạ; trên áo thật patch World Series ở **ngực trái**, NL Champions ở **tay trái** người mặc.
- Không quay qua gương (chữ trong gương bị ngược).
- Nhân vật Sienna là người mới của project này, sheet gen riêng ở Bước 0 (ảnh chụp thật). Từ ngữ mô tả mẫu giữ ở mức "glam, confident, fitted": crop top, short denim cạp cao — không dùng từ gợi dục để Flow không chặn.
- **Shot 1 là trigger** (UECKER 9 trong hộp), mẫu xuất hiện từ nửa sau clip 1.

## Các khóa (dán nguyên văn, không sửa chữ nào)

**PRODUCT (sản phẩm):**
a powder-blue button-front baseball jersey with gold-and-white trim on the V collar, placket and sleeve ends; front: the script words Brew Crew in gold with a navy outline across the chest and a navy number 9 with gold outline below it on the wearer's left side; a round World Series 2026 patch on the wearer's left chest and a gold NATIONAL LEAGUE CHAMPIONS 2026 patch on the wearer's left sleeve; back: UECKER in navy block letters above a large navy number 9 with gold outline; every letter, number and patch exactly as in the product photo

**CHARACTER - Sienna (nhân vật):**
American woman in her mid-20s, glamorous and confident, lightly tanned skin, long wavy black hair, berry lipstick, fit athletic figure, fitted white crop top, high-waist denim shorts, gold nails, navy baseball cap with a small gold glove-shaped emblem, no lettering, worn backwards

**REALISM (độ chân thực + vật lý, dán vào mọi prompt có người/tay):**
Real human being filmed on a phone: natural skin with pores and slight unevenness, real eyes with reflections, hair with individual strands, clothing that creases and hangs with weight. Every movement obeys physics: feet stay on the ground, weight shifts before a step, hands grip objects with correct finger placement and stay on their surfaces, bodies and clothes keep clear of the car, the door, the ground and each other, objects keep their size and weight. One continuous action at real speed.

**STYLE (phòng ngủ buổi tối):**
phone footage, vertical 9:16, a cozy bedroom in the evening, warm fairy lights along the headboard, a powder-blue and gold pennant pinned on the bedroom wall, a navy-and-gold foam finger leaning on the shelf, white bedding, soft warm key light from a bedside lamp, natural contrast, real textures, no color grading

**AUDIO (mọi clip):** real sounds of the action, quiet room tone, no speech, no music

**NEGATIVE (chung):** subtitles, captions, on-screen text, watermark, misspelled lettering, mirrored lettering, extra letters, wrong number, extra patches, patch on the stomach, mirror reflection, music, plastic skin, airbrushed, beauty filter, uncanny face, extra fingers, fused fingers, distorted hands, extra limbs, clipping through objects, floating objects, morphing, duplicated person, teleporting, warped background

## Bước 0 — Ảnh tham chiếu

1. `frames/product.png` — nguồn duy nhất của chữ và patch trên áo.
2. **Ảnh nhân vật Sienna (gen mới cho project này, ảnh chụp thật):**
   ```
   Photograph, character reference sheet, one image, 16:9: a real person photographed in a studio, three full-body views (front, side, back) on the left, one chest-up close-up on the right, plain light-grey background, even soft light, real skin and fabric texture, confident smile at the lens, no illustration, not a cartoon, no 3D render, no CGI. American woman in her mid-20s, glamorous and confident, lightly tanned skin, long wavy black hair, berry lipstick, fit athletic figure, fitted white crop top, high-waist denim shorts, gold nails, navy baseball cap with a small gold glove-shaped emblem, no lettering, worn backwards. No text, no watermark.
   ```
   **Lưu thành:** `sienna_sheet.png`

## Bước 1 — Ảnh khung đầu (Nano Banana 2.1, 9:16)

### Keyframe 1 · cho clip 1 · Nano Banana 2.1
**Ảnh tải lên:** ảnh 1 = `product.png`, ảnh 2 = `sienna_sheet.png` · **Lưu thành:** `keyframe_c1.png`

**Cảnh:** nhìn từ trên xuống: hộp kraft mở trên giường trắng, giấy lụa trắng vừa được vén, áo gấp nằm **mặt sau lên trên** để lộ UECKER 9; hai bàn tay Sienna (sơn móng nude) đang giữ hai mép giấy lụa.
```
Image 1 is the product: keep every letter, number, colour and patch of the jersey exactly as in image 1; do not redraw or retype the lettering. Image 2 is the woman: match her skin, hands and white crop top sleeve.
Top-down close-up of an open kraft shipping box on white bedding: white tissue paper just parted by a woman's two hands with gold nails, revealing the powder-blue jersey folded neatly with its back facing up, UECKER in navy block letters arched above a large navy number 9 with gold outline, the gold-and-white trim of the collar visible at the top of the fold.
Real human being filmed on a phone: natural skin with pores and slight unevenness, real eyes with reflections, hair with individual strands, clothing that creases and hangs with weight. Every movement obeys physics: feet stay on the ground, weight shifts before a step, hands grip objects with correct finger placement and stay on their surfaces, bodies and clothes keep clear of the car, the door, the ground and each other, objects keep their size and weight. One continuous action at real speed.
phone footage, vertical 9:16, a cozy bedroom in the evening, warm fairy lights along the headboard, a powder-blue and gold pennant pinned on the bedroom wall, a navy-and-gold foam finger leaning on the shelf, white bedding, soft warm key light from a bedside lamp, natural contrast, real textures, no color grading
Vertical 9:16, the lettering in the centre third, top 15% and bottom 20% kept clear. No other text, no watermark, natural hands with five fingers.
```
**Soát trước khi làm video:** áo gấp mặt sau lên trên (back facing up), UECKER above large 9 đúng từng chữ · không ngược, không lộn trái (never inside-out or upside down) · tay đủ ngón · cờ đuôi nheo xanh-vàng thấy được

### Keyframe 2 · cho clip 2 · Nano Banana 2.1
**Ảnh tải lên:** ảnh 1 = `product.png`, ảnh 2 = `sienna_sheet.png` · **Lưu thành:** `keyframe_c2.png`

**Cảnh:** cận macro: Sienna đang mặc áo; patch tròn World Series 2026 trên **ngực trái** người mặc, đầu ngón tay cô chạm mép patch; một phần chữ Brew Crew vàng ở mép khung.
```
Image 1 is the product: keep the round World Series 2026 patch, the gold Brew Crew script and the gold-and-white trim exactly as in image 1; do not redraw or retype any lettering. Image 2 is the woman: match her skin and hair.
Macro close-up of the powder-blue jersey being worn by the woman: the round World Series 2026 patch on the wearer's left chest fills the centre of the frame, sharp, her fingertip with a gold nail resting at the patch's edge, the edge of the gold Brew Crew script and the gold-and-white placket trim just in frame, a strand of black hair falling across the shoulder.
Real human being filmed on a phone: natural skin with pores and slight unevenness, real eyes with reflections, hair with individual strands, clothing that creases and hangs with weight. Every movement obeys physics: feet stay on the ground, weight shifts before a step, hands grip objects with correct finger placement and stay on their surfaces, bodies and clothes keep clear of the car, the door, the ground and each other, objects keep their size and weight. One continuous action at real speed.
phone footage, vertical 9:16, a cozy bedroom in the evening, warm fairy lights along the headboard, a powder-blue and gold pennant pinned on the bedroom wall, a navy-and-gold foam finger leaning on the shelf, white bedding, soft warm key light from a bedside lamp, natural contrast, real textures, no color grading
Macro, vertical 9:16, the patch in the centre third, shallow depth of field, top 15% and bottom 20% kept clear. No other text, no watermark, natural hands with five fingers.
```
**Soát trước khi làm video:** patch World Series 2026 trên ngực trái người mặc (wearer's left chest), chữ đúng · viền vàng-trắng nẹp áo (gold trim, placket) · không patch ở bụng · tay đủ ngón

### Keyframe 3 · cho clip 3 · Nano Banana 2.1
**Ảnh tải lên:** ảnh 1 = `product.png`, ảnh 2 = `sienna_sheet.png` · **Lưu thành:** `keyframe_c3.png`

**Cảnh:** medium shot: Sienna đứng trên sàn cạnh giường, cầm áo bằng hai vai giơ trước ngực, **mặt sau quay về camera** (UECKER 9), mặt cô ló ra trên cổ áo, cười; mũ navy.
```
Image 1 is the product: keep every letter, number, colour and patch of the jersey exactly as in image 1; do not redraw or retype the lettering. Image 2 is the woman; keep her face, hair, cap and outfit.
American woman in her mid-20s, glamorous and confident, lightly tanned skin, long wavy black hair, berry lipstick, fit athletic figure, fitted white crop top, high-waist denim shorts, gold nails, navy baseball cap with a small gold glove-shaped emblem, no lettering, worn backwards, standing on the floor beside the bed, holding the powder-blue jersey up by its shoulders at chest height with the back facing the camera, UECKER above a large number 9, her smiling face just above the collar.
Real human being filmed on a phone: natural skin with pores and slight unevenness, real eyes with reflections, hair with individual strands, clothing that creases and hangs with weight. Every movement obeys physics: feet stay on the ground, weight shifts before a step, hands grip objects with correct finger placement and stay on their surfaces, bodies and clothes keep clear of the car, the door, the ground and each other, objects keep their size and weight. One continuous action at real speed.
phone footage, vertical 9:16, a cozy bedroom in the evening, warm fairy lights along the headboard, a powder-blue and gold pennant pinned on the bedroom wall, a navy-and-gold foam finger leaning on the shelf, white bedding, soft warm key light from a bedside lamp, natural contrast, real textures, no color grading
Medium shot, vertical 9:16, the jersey back in the centre third, top 15% and bottom 20% kept clear. No other text, no watermark, natural hands with five fingers.
```
**Soát trước khi làm video:** mặt sau UECKER above large 9 đúng chữ, không ngược (never mirrored) · áo xanh pastel viền vàng-trắng (powder blue, gold trim) · mặt và mũ giống sheet · tay đủ ngón

### Keyframe 4 · cho clip 4 · Nano Banana 2.1
**Ảnh tải lên:** ảnh 1 = `product.png`, ảnh 2 = `sienna_sheet.png` · **Lưu thành:** `keyframe_c4.png`

**Cảnh:** full shot trực diện (không gương): Sienna đứng giữa phòng, mặc áo mở ngoài crop top trắng, mũ navy, tay chống hông, mặt trước Brew Crew + 24 + patch ngực trái rõ.
```
Image 1 is the product: keep every letter, number, colour and patch of the jersey exactly as in image 1; do not redraw or retype the lettering. Image 2 is the woman; keep her face, hair, cap and outfit.
American woman in her mid-20s, glamorous and confident, lightly tanned skin, long wavy black hair, berry lipstick, fit athletic figure, fitted white crop top, high-waist denim shorts, gold nails, navy baseball cap with a small gold glove-shaped emblem, no lettering, worn backwards, wearing the powder-blue jersey open over the white crop top, hem loose over the denim shorts, not tucked in, standing on the floor in the middle of the bedroom facing the camera directly, one hand on her hip, the number 9 below it on her left side, the round World Series 2026 patch on her left chest and the NATIONAL LEAGUE CHAMPIONS 2026 patch on her left sleeve.
Real human being filmed on a phone: natural skin with pores and slight unevenness, real eyes with reflections, hair with individual strands, clothing that creases and hangs with weight. Every movement obeys physics: feet stay on the ground, weight shifts before a step, hands grip objects with correct finger placement and stay on their surfaces, bodies and clothes keep clear of the car, the door, the ground and each other, objects keep their size and weight. One continuous action at real speed.
phone footage, vertical 9:16, a cozy bedroom in the evening, warm fairy lights along the headboard, a powder-blue and gold pennant pinned on the bedroom wall, a navy-and-gold foam finger leaning on the shelf, white bedding, soft warm key light from a bedside lamp, natural contrast, real textures, no color grading
Full shot facing the camera, no mirror, no posters or photos of people on the walls, vertical 9:16, the jersey front in the centre third, top 15% and bottom 20% kept clear. No other text, no watermark, natural hands with five fingers.
```
**Soát trước khi làm video:** mặt trước Brew Crew script centred across the chest, số 9 bên trái người mặc (below the script, wearer's left) · patch World Series ngực trái, NL Champions tay trái (left chest, left sleeve) · áo mở, không nhét quần (worn open, never tucked in) · không gương, không poster người · mặt giống sheet

## Bước 2 — Prompt video (Omni 1.1 Flash, chế độ Thành phần, 8 giây, 9:16)

Thứ tự clip theo story: c01 mở hộp → giũ (trigger ở nửa đầu), c02 patch WS → patch NL, c03 lật mặt trước → mặc, c04 xoay → CTA.

## Clip 1 · 8s · Mở hộp → giũ áo (hook + drop)
**Khung đầu (ingredients):** `product.png`, `keyframe_c1.png`, `sienna_sheet.png` · **Lưu video thành:** `c01_a.mp4`

**Cảnh:** nửa đầu tay vén hết giấy lụa, áo gấp mặt sau lộ rõ; nửa sau Sienna nhấc áo bằng hai vai ra khỏi hộp, giũ một cái cho thẳng, giơ trước camera mặt sau, camera lùi lên thành medium shot thấy mặt cô cười.
```
Top-down close-up, then the camera rises and pulls back. The woman stands on the floor beside the bed, leaning over the box. In the first half her hands fold the white tissue paper fully open inside the kraft box on the white bedding, revealing the powder-blue jersey folded with its back facing up, UECKER above a large number 9, every letter sharp and unchanged. In the second half she takes the jersey by both shoulders, lifts it out of the box and gives it one shake so it hangs straight, holding it up at chest height with the back facing the camera while the camera rises and pulls back to a medium shot of her smiling face above the collar; the lettering stays sharp and readable the whole time.
Real human being filmed on a phone: natural skin with pores and slight unevenness, real eyes with reflections, hair with individual strands, clothing that creases and hangs with weight. Every movement obeys physics: feet stay on the ground, weight shifts before a step, hands grip objects with correct finger placement and stay on their surfaces, bodies and clothes keep clear of the car, the door, the ground and each other, objects keep their size and weight. One continuous action at real speed.
Audio: rustling tissue paper, a fabric shake, quiet room tone, no speech, no music. No subtitles, no on-screen text.
```
**Phủ định (Negative):** `subtitles, captions, on-screen text, watermark, misspelled lettering, mirrored lettering, extra letters, wrong number, jersey inside-out, music, plastic skin, airbrushed, beauty filter, uncanny face, extra fingers, fused fingers, distorted hands, extra limbs, body passing through the car or door, clipping through objects, floating objects, morphing, duplicated person, teleporting, sliding feet, warped background`
**Soát clip:** áo ra khỏi hộp mặt sau lên trên (comes out folded, back on top), UECKER above large 9 đúng chữ mọi giây · không lộn trái, không ngược (never inside-out or upside down, never mirrored) · tay đủ ngón · mặt giống sheet

## Clip 2 · 8s · Cận patch World Series → patch NL Champions (drop)
**Khung đầu (ingredients):** `product.png`, `keyframe_c2.png` · **Lưu video thành:** `c02_a.mp4`

**Cảnh:** nửa đầu macro, đầu ngón tay vuốt chậm theo viền patch World Series ở ngực trái; nửa sau camera trượt sang vai trái xuống tay áo trái, Sienna hơi nâng cánh tay, patch NATIONAL LEAGUE CHAMPIONS 2026 hiện rõ.
```
Macro close-up, slow slide left. In the first half the woman's fingertip traces slowly around the edge of the round World Series 2026 patch on the wearer's left chest of the powder-blue jersey; the patch stays sharp and every letter unchanged. In the second half the camera slides slowly across her left shoulder and down her left sleeve while she lifts the arm slightly, bringing the gold NATIONAL LEAGUE CHAMPIONS 2026 patch on the left sleeve into sharp focus in the centre of the frame, its ball-in-glove monogram and lettering exactly as in the product image.
Real human being filmed on a phone: natural skin with pores and slight unevenness, real eyes with reflections, hair with individual strands, clothing that creases and hangs with weight. Every movement obeys physics: feet stay on the ground, weight shifts before a step, hands grip objects with correct finger placement and stay on their surfaces, bodies and clothes keep clear of the car, the door, the ground and each other, objects keep their size and weight. One continuous action at real speed.
Audio: a soft brush on fabric, quiet room tone, no speech, no music. No subtitles, no on-screen text.
```
**Phủ định (Negative):** `subtitles, captions, on-screen text, watermark, misspelled lettering, mirrored lettering, extra letters, blurry patch, extra patches, patch on the stomach, music, plastic skin, airbrushed, beauty filter, uncanny face, extra fingers, fused fingers, distorted hands, extra limbs, body passing through the car or door, clipping through objects, floating objects, morphing, duplicated person, teleporting, sliding feet, warped background`
**Soát clip:** patch World Series 2026 trên wearer's left chest, chữ đúng, nét · patch NATIONAL LEAGUE CHAMPIONS 2026 trên left sleeve, chữ đúng · không patch nào ở bụng hay lưng (never on the stomach or the back) · ngón tay đủ, không xuyên vải

## Clip 3 · 8s · Lật mặt trước → mặc vào
**Khung đầu (ingredients):** `product.png`, `keyframe_c3.png`, `sienna_sheet.png` · **Lưu video thành:** `c03_a.mp4`

**Cảnh:** nửa đầu Sienna xoay áo một vòng để mặt trước Brew Crew hướng camera, chữ vàng bắt sáng đèn; nửa sau cô xỏ tay trái rồi tay phải vào tay áo, kéo áo lên vai, chỉnh cổ áo, để mở cúc.
```
Medium shot, static. The woman stands on the floor beside the bed holding the powder-blue jersey up by its shoulders with the back facing the camera. In the first half she turns the jersey around so the front faces the camera: the gold Brew Crew script across the chest catches the lamp light, the navy number 9 below it on the left side, the round World Series 2026 patch on the left chest. In the second half she slides her left arm into the left sleeve, then her right arm into the right sleeve, pulls the jersey onto her shoulders over the white crop top, leaves it open, straightens the collar with both hands and flicks her hair back over one shoulder, hem loose, not tucked in; every letter and patch stays exactly as in the product image.
Real human being filmed on a phone: natural skin with pores and slight unevenness, real eyes with reflections, hair with individual strands, clothing that creases and hangs with weight. Every movement obeys physics: feet stay on the ground, weight shifts before a step, hands grip objects with correct finger placement and stay on their surfaces, bodies and clothes keep clear of the car, the door, the ground and each other, objects keep their size and weight. One continuous action at real speed.
Audio: fabric rustle, quiet room tone, no speech, no music. No subtitles, no on-screen text.
```
**Phủ định (Negative):** `subtitles, captions, on-screen text, watermark, misspelled lettering, mirrored lettering, extra letters, wrong number, extra patches, patch on the stomach, music, plastic skin, airbrushed, beauty filter, uncanny face, extra fingers, fused fingers, distorted hands, extra limbs, body passing through the car or door, clipping through objects, floating objects, morphing, duplicated person, teleporting, sliding feet, warped background`
**Soát clip:** mặt trước Brew Crew script centred across the chest, không ngược · số 9 below the script bên trái người mặc · patch World Series wearer's left chest, NL Champions left sleeve, không ở bụng · áo mặc mở, chữ tách theo nẹp là tự nhiên (worn open, never tucked in) · tay xỏ đúng tay áo, không xuyên vải

## Clip 4 · 8s · Xoay khoe mặt sau → CTA
**Khung đầu (ingredients):** `product.png`, `keyframe_c4.png`, `sienna_sheet.png` · **Lưu video thành:** `c04_a.mp4`

**Cảnh:** nửa đầu Sienna xoay chậm một vòng tại chỗ, mặt sau UECKER 9 hướng camera giữa vòng xoay rồi quay lại mặt trước; nửa sau cô nhìn thẳng camera, nháy mắt, chỉ tay xuống dưới khung.
```
Full shot facing the camera, static, no mirror. The woman stands on the floor in the middle of the bedroom wearing the powder-blue jersey open over the white crop top and the navy cap worn backwards. In the first half she turns one slow full circle in place, her feet stepping around on the spot: halfway through the back faces the camera, UECKER above a large number 9 sharp and readable, then she comes back to face the camera with the gold Brew Crew script across her chest. In the second half she looks straight into the lens, winks and points down toward the bottom of the frame with her right index finger, smiling; every letter and patch stays exactly as in the product image.
Real human being filmed on a phone: natural skin with pores and slight unevenness, real eyes with reflections, hair with individual strands, clothing that creases and hangs with weight. Every movement obeys physics: feet stay on the ground, weight shifts before a step, hands grip objects with correct finger placement and stay on their surfaces, bodies and clothes keep clear of the car, the door, the ground and each other, objects keep their size and weight. One continuous action at real speed.
Audio: soft footsteps on the floor, quiet room tone, no speech, no music. No subtitles, no on-screen text.
```
**Phủ định (Negative):** `subtitles, captions, on-screen text, watermark, misspelled lettering, mirrored lettering, extra letters, wrong number, mirror reflection, music, plastic skin, airbrushed, beauty filter, uncanny face, extra fingers, fused fingers, distorted hands, extra limbs, body passing through the car or door, clipping through objects, floating objects, morphing, duplicated person, teleporting, sliding feet, warped background`
**Soát clip:** khi quay lưng: back reads UECKER over a large 9 đúng chữ · khi quay lại: Brew Crew script centred across the chest, patch World Series left chest, NL Champions left sleeve · áo mở (worn open, never tucked in) · không gương · mặt giống sheet, chân trên sàn

## Thiết lập khi gen video
- Cả 4 clip: Omni 1.1 Flash, chế độ **Thành phần** (ingredients): ảnh sản phẩm trước, keyframe sau, rồi sheet nhân vật; 8 giây, dọc 9:16, tải **1080p** (không chọn tuỳ chọn tính tín dụng).
- Tiếng clip không dùng: video dùng nhạc drill khi dựng.
- Sau khi gen: `gen_review.py brewers-uecker-9-blue-unbox`, soát từng chữ trên áo theo `placement_checks`, đánh dấu pass/fail trước khi dựng.
