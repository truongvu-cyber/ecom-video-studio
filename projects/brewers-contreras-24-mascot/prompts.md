# Jersey Brew Crew Contreras #24 — mascot Barley ở sân vận động — prompt tạo ảnh và video

Phần mô tả, hướng dẫn và ghi chú viết bằng tiếng Việt. Phần prompt (trong khung code) và các khóa giữ bằng tiếng Anh: **copy nguyên văn, không dịch**.

| Công cụ video | Công cụ ảnh | Tỉ lệ | Độ dài | Số clip | Phong cách | Thể loại | Âm thanh |
|---|---|---|---|---|---|---|---|
| Omni 1.1 Flash (Flow, chế độ Thành phần) | Nano Banana 2.1 | 9:16 | ~14 giây, 8 nhát cắt | 4 clip × 8 giây, mỗi clip 2 hành động | sân bóng chày đêm có trận | hype montage mascot, không lời | tắt tiếng gốc, nhạc sports hype rap khi dựng |

**Lưu ý chung:**
- **Mọi chữ và patch trên áo lấy từ `product.png`** (ảnh 1 trong thành phần của mọi cảnh thấy áo): Brew Crew, CONTRERAS, 24, World Series 2026, NATIONAL LEAGUE CHAMPIONS 2026 đúng từng chữ. Áo mở cúc làm chữ tách là tự nhiên.
- Hai patch to ở đáy ảnh sản phẩm là ảnh minh hoạ; trên áo thật patch World Series ở **ngực trái**, NL Champions ở **tay trái** người mặc.
- Barley là mascot tự sáng tác (gấu), sheet gen riêng ở Bước 0; không giống mascot thật nào, không chữ trên mũ.
- Sân không có tên/logo đọc được; bảng điểm sáng vàng không chữ.

## Các khóa (dán nguyên văn, không sửa chữ nào)

**PRODUCT (sản phẩm):**
a powder-blue button-front baseball jersey with gold-and-white trim on the V collar, placket and sleeve ends; front: the script words Brew Crew in gold with a navy outline across the chest and a navy number 24 with gold outline below it on the wearer's left side; a round World Series 2026 patch on the wearer's left chest and a gold NATIONAL LEAGUE CHAMPIONS 2026 patch on the wearer's left sleeve; back: CONTRERAS in navy block letters arched above a large navy number 24 with gold outline; every letter, number and patch exactly as in the product photo

**CHARACTER - Barley (mascot):**
a tall, friendly ballpark mascot: a person in a full plush bear costume with honey-gold fur, a cream muzzle, a big round black nose, large round cheerful eyes, round ears, big padded paws with four fingers, wearing a navy baseball cap with a small gold glove-shaped emblem, no lettering, and the powder-blue jersey worn like a real jersey over the fur

**REALISM (độ chân thực + vật lý, dán vào mọi prompt có mascot/người):**
Real human being filmed on a phone: natural skin with pores and slight unevenness, real eyes with reflections, hair with individual strands, clothing that creases and hangs with weight. Every movement obeys physics: feet stay on the ground, weight shifts before a step, hands grip objects with correct finger placement and stay on their surfaces, bodies and clothes keep clear of the car, the door, the ground and each other, objects keep their size and weight. One continuous action at real speed.

**STYLE (sân bóng chày đêm có trận):**
phone footage, vertical 9:16, a packed baseball stadium at night during a playoff game, bright white stadium lights, stands packed with fans waving gold rally towels, powder-blue and navy bunting hanging along the stadium railing, a giant blank scoreboard glowing gold over the outfield, fresh green grass and brown infield dirt, natural contrast, real textures, no color grading

**AUDIO (mọi clip):** real sounds of the action, distant crowd roar, no speech, no music

**NEGATIVE (chung):** subtitles, captions, on-screen text, watermark, misspelled lettering, mirrored lettering, extra letters, wrong number, extra patches, patch on the stomach, readable stadium names, team logos on the scoreboard, jersey stretched flat like a sticker, music, plastic texture, uncanny face, extra fingers, distorted paws, extra limbs, clipping through objects, floating objects, morphing, duplicated mascot, teleporting, warped background

## Bước 0 — Ảnh tham chiếu

1. `frames/product.png` — nguồn duy nhất của chữ và patch trên áo.
2. **Ảnh mascot Barley (gen mới cho project này):**
   ```
   Photograph, character reference sheet, one image, 16:9: a real performer in a real plush mascot costume photographed in a studio, three full-body views (front, side, back) on the left, one head-and-chest close-up on the right, plain light-grey background, even soft light, true fur and fabric texture, no illustration, not a cartoon, no 3D render, no CGI. A tall, friendly ballpark mascot: a person in a full plush bear costume with honey-gold fur, a cream muzzle, a big round black nose, large round cheerful eyes, round ears, big padded paws with four fingers, wearing a navy baseball cap with a small gold glove-shaped emblem, no lettering, and a plain powder-blue baseball jersey with gold-and-white trim, unbuttoned, no lettering on it. No text, no watermark.
   ```
   **Lưu thành:** `barley_sheet.png`

## Bước 1 — Ảnh khung đầu (Nano Banana 2.1, 9:16)

### Keyframe 1 · cho clip 1 · Nano Banana 2.1
**Ảnh tải lên:** ảnh 1 = `product.png`, ảnh 2 = `barley_sheet.png` · **Lưu thành:** `keyframe_c1.png`

**Cảnh:** từ phía sau, trong đường hầm cầu thủ tối: Barley đứng ở miệng hầm, quay lưng về camera, mặt sau áo **CONTRERAS 24** rõ, phía trước là sân sáng rực.
```
Image 1 is the product: keep every letter, number, colour and patch of the jersey exactly as in image 1; do not redraw or retype the lettering. Image 2 is the mascot: keep its costume, cap and proportions exactly.
a tall, friendly ballpark mascot: a person in a full plush bear costume with honey-gold fur, a cream muzzle, a big round black nose, large round cheerful eyes, round ears, big padded paws with four fingers, wearing a navy baseball cap with a small gold glove-shaped emblem, no lettering, and the powder-blue jersey worn like a real jersey over the fur, seen from behind, standing on the concrete floor at the end of a dark players' tunnel, the jersey back facing the camera with CONTRERAS arched above a large number 24, the jersey hanging from its shoulders with natural folds; ahead of it the bright stadium opens up.
Real human being filmed on a phone: natural skin with pores and slight unevenness, real eyes with reflections, hair with individual strands, clothing that creases and hangs with weight. Every movement obeys physics: feet stay on the ground, weight shifts before a step, hands grip objects with correct finger placement and stay on their surfaces, bodies and clothes keep clear of the car, the door, the ground and each other, objects keep their size and weight. One continuous action at real speed.
phone footage, vertical 9:16, a packed baseball stadium at night during a playoff game, bright white stadium lights, stands packed with fans waving gold rally towels, powder-blue and navy bunting hanging along the stadium railing, a giant blank scoreboard glowing gold over the outfield, fresh green grass and brown infield dirt, natural contrast, real textures, no color grading
Vertical 9:16, the jersey back in the centre third, the bright field framed by the dark tunnel, top 15% and bottom 20% kept clear. No other text, no watermark.
```
**Soát trước khi làm video:** back reads CONTRERAS arched over a large 24 đúng chữ, không ngược · áo nằm trên vai mascot như áo thật (worn by the mascot, shoulders on the shoulders), không dán phẳng · mũ không chữ · bảng điểm không chữ

### Keyframe 2 · cho clip 2 · Nano Banana 2.1
**Ảnh tải lên:** ảnh 1 = `product.png`, ảnh 2 = `barley_sheet.png` · **Lưu thành:** `keyframe_c2.png`

**Cảnh:** góc thấp: Barley đứng trên nóc dugout, quay mặt về camera, hai tay giơ cao, mặt trước Brew Crew + 24 + patch World Series ở ngực trái; khán đài vẫy khăn vàng phía sau.
```
Image 1 is the product: keep every letter, number, colour and patch of the jersey exactly as in image 1; do not redraw or retype the lettering. Image 2 is the mascot: keep its costume, cap and proportions exactly.
a tall, friendly ballpark mascot: a person in a full plush bear costume with honey-gold fur, a cream muzzle, a big round black nose, large round cheerful eyes, round ears, big padded paws with four fingers, wearing a navy baseball cap with a small gold glove-shaped emblem, no lettering, and the powder-blue jersey worn like a real jersey over the fur, standing on the flat roof of the dugout facing the camera with both arms raised high, the gold Brew Crew script across its chest, the number 24 below it on its left side, the round World Series 2026 patch on its left chest, the NATIONAL LEAGUE CHAMPIONS 2026 patch on its left sleeve; behind it the stands are packed with cheering fans.
Real human being filmed on a phone: natural skin with pores and slight unevenness, real eyes with reflections, hair with individual strands, clothing that creases and hangs with weight. Every movement obeys physics: feet stay on the ground, weight shifts before a step, hands grip objects with correct finger placement and stay on their surfaces, bodies and clothes keep clear of the car, the door, the ground and each other, objects keep their size and weight. One continuous action at real speed.
phone footage, vertical 9:16, a packed baseball stadium at night during a playoff game, bright white stadium lights, stands packed with fans waving gold rally towels, powder-blue and navy bunting hanging along the stadium railing, a giant blank scoreboard glowing gold over the outfield, fresh green grass and brown infield dirt, natural contrast, real textures, no color grading
Low angle, vertical 9:16, the mascot in the centre third, top 15% and bottom 20% kept clear. No other text, no watermark.
```
**Soát trước khi làm video:** Brew Crew script across the chest, số 24 below the script bên trái người mặc · patch World Series wearer's left chest, NL Champions left sleeve · áo trên vai và ngực mascot, không dán phẳng · khán đài vẫy khăn vàng

### Keyframe 3 · cho clip 3 · Nano Banana 2.1
**Ảnh tải lên:** ảnh 1 = `product.png`, ảnh 2 = `barley_sheet.png` · **Lưu thành:** `keyframe_c3.png`

**Cảnh:** cận: vai và tay áo trái của Barley, patch **NATIONAL LEAGUE CHAMPIONS 2026** giữa khung, ngón tay lông vàng của bàn tay phải chỉ vào patch; đèn sân lấp lánh phía sau.
```
Image 1 is the product: keep the gold NATIONAL LEAGUE CHAMPIONS 2026 patch, the round World Series 2026 patch and the gold-and-white trim exactly as in image 1; do not redraw or retype any lettering. Image 2 is the mascot: match its honey-gold fur and padded paws.
Close-up of the mascot's left shoulder and upper arm in the powder-blue jersey: the gold NATIONAL LEAGUE CHAMPIONS 2026 patch on the left sleeve fills the centre of the frame, sharp, with its ball-in-glove monogram; the mascot's furry honey-gold right paw points at the patch with one padded finger; the edge of the round World Series 2026 patch on the left chest and the gold-and-white sleeve trim just in frame; stadium lights sparkle out of focus behind.
Real human being filmed on a phone: natural skin with pores and slight unevenness, real eyes with reflections, hair with individual strands, clothing that creases and hangs with weight. Every movement obeys physics: feet stay on the ground, weight shifts before a step, hands grip objects with correct finger placement and stay on their surfaces, bodies and clothes keep clear of the car, the door, the ground and each other, objects keep their size and weight. One continuous action at real speed.
phone footage, vertical 9:16, a packed baseball stadium at night during a playoff game, bright white stadium lights, stands packed with fans waving gold rally towels, powder-blue and navy bunting hanging along the stadium railing, a giant blank scoreboard glowing gold over the outfield, fresh green grass and brown infield dirt, natural contrast, real textures, no color grading
Close-up, vertical 9:16, the patch in the centre third, shallow depth of field, top 15% and bottom 20% kept clear. No other text, no watermark.
```
**Soát trước khi làm video:** patch NATIONAL LEAGUE CHAMPIONS 2026 trên wearer's left sleeve, chữ đúng · patch World Series ở left chest nếu thấy · không patch ở bụng · lông mascot đúng sheet

### Keyframe 4 · cho clip 4 · Nano Banana 2.1
**Ảnh tải lên:** ảnh 1 = `product.png`, ảnh 2 = `barley_sheet.png` · **Lưu thành:** `keyframe_c4.png`

**Cảnh:** trên khán đài: Barley đứng ở lối đi giữa các hàng ghế, cúi xuống giơ tay đập tay với một bé trai ~8 tuổi mặc cùng áo, ngồi cạnh bố; fan xung quanh vẫy khăn vàng.
```
Image 1 is the product: keep every letter, number, colour and patch of the jersey exactly as in image 1 on both the mascot and the child; do not redraw or retype the lettering. Image 2 is the mascot: keep its costume, cap and proportions exactly.
a tall, friendly ballpark mascot: a person in a full plush bear costume with honey-gold fur, a cream muzzle, a big round black nose, large round cheerful eyes, round ears, big padded paws with four fingers, wearing a navy baseball cap with a small gold glove-shaped emblem, no lettering, and the powder-blue jersey worn like a real jersey over the fur, standing in the concrete aisle between rows of stadium seats, leaning toward a smiling boy of about eight in the same powder-blue jersey who sits in the aisle seat next to his father; the mascot's right paw is raised for a high-five, the boy's hand coming up to meet it; fans around them wave gold rally towels.
Real human being filmed on a phone: natural skin with pores and slight unevenness, real eyes with reflections, hair with individual strands, clothing that creases and hangs with weight. Every movement obeys physics: feet stay on the ground, weight shifts before a step, hands grip objects with correct finger placement and stay on their surfaces, bodies and clothes keep clear of the car, the door, the ground and each other, objects keep their size and weight. One continuous action at real speed.
phone footage, vertical 9:16, a packed baseball stadium at night during a playoff game, bright white stadium lights, stands packed with fans waving gold rally towels, powder-blue and navy bunting hanging along the stadium railing, a giant blank scoreboard glowing gold over the outfield, fresh green grass and brown infield dirt, natural contrast, real textures, no color grading
Medium shot, vertical 9:16, the mascot and the boy in the centre third, top 15% and bottom 20% kept clear. No other text, no watermark, natural hands with five fingers.
```
**Soát trước khi làm video:** Brew Crew script across the chest trên áo mascot và áo bé · patch World Series wearer's left chest · áo mặc trên vai như áo thật · mascot đứng ở lối đi, bé ngồi ghế cạnh bố

## Bước 2 — Prompt video (Omni 1.1 Flash, chế độ Thành phần, 8 giây, 9:16)

## Clip 1 · 8s · Lao ra khỏi hầm → dang tay giữa sân
**Khung đầu (ingredients):** `product.png`, `keyframe_c1.png`, `barley_sheet.png` · **Lưu video thành:** `c01_a.mp4`

**Cảnh:** nửa đầu Barley chạy từ miệng hầm ra sân, camera bám sau lưng, CONTRERAS 24 rõ; nửa sau chạy tới cỏ, dừng lại, dang hai tay về phía khán đài, đèn sân lóa, khán giả vẫy khăn vàng.
```
Handheld tracking shot from behind, following. The mascot stands on the concrete at the end of the dark players' tunnel with the jersey back facing the camera. In the first half it jogs out of the tunnel onto the warning track and into the bright stadium lights, the camera following close behind, CONTRERAS arched above a large number 24 on its back sharp and readable, the jersey swinging with each step. In the second half it slows to a stop on the green grass, plants both feet and spreads its arms wide toward the stands as the lights flare and the packed crowd waves gold rally towels.
Real human being filmed on a phone: natural skin with pores and slight unevenness, real eyes with reflections, hair with individual strands, clothing that creases and hangs with weight. Every movement obeys physics: feet stay on the ground, weight shifts before a step, hands grip objects with correct finger placement and stay on their surfaces, bodies and clothes keep clear of the car, the door, the ground and each other, objects keep their size and weight. One continuous action at real speed.
Audio: padded footsteps on concrete then grass, a rising crowd roar, no speech, no music. No subtitles, no on-screen text.
```
**Phủ định (Negative):** `subtitles, captions, on-screen text, watermark, misspelled lettering, mirrored lettering, extra letters, wrong number, readable stadium names, jersey stretched flat like a sticker, music, plastic texture, uncanny face, extra fingers, distorted paws, extra limbs, body passing through the car or door, clipping through objects, floating objects, morphing, duplicated mascot, teleporting, sliding feet, warped background`
**Soát clip:** back reads CONTRERAS arched over a large 24 mọi giây, không ngược · áo worn by the mascot trên vai, đung đưa như áo thật, không dán phẳng · chân chạm đất khi chạy · bảng điểm, khán đài không chữ đọc được

## Clip 2 · 8s · Nhảy trên nóc dugout → vung khăn
**Khung đầu (ingredients):** `product.png`, `keyframe_c2.png`, `barley_sheet.png` · **Lưu video thành:** `c02_a.mp4`

**Cảnh:** nửa đầu Barley nhún nhảy một cái trên nóc dugout và tiếp đất, quay thẳng về camera, mặt trước Brew Crew + patch rõ; nửa sau rút khăn vàng từ túi quần, vung tròn trên đầu, khán giả phía sau hò reo theo.
```
Low angle, static. The mascot stands on the flat roof of the dugout facing the camera with both arms raised. In the first half it does one small bouncy hop and lands on both feet on the roof, facing the camera, the gold Brew Crew script across its chest, the number 24 on its left side and the round World Series 2026 patch on its left chest sharp and readable. In the second half it pulls a gold rally towel from its hip and swings it in big circles above its head while the packed stands behind it wave their towels back.
Real human being filmed on a phone: natural skin with pores and slight unevenness, real eyes with reflections, hair with individual strands, clothing that creases and hangs with weight. Every movement obeys physics: feet stay on the ground, weight shifts before a step, hands grip objects with correct finger placement and stay on their surfaces, bodies and clothes keep clear of the car, the door, the ground and each other, objects keep their size and weight. One continuous action at real speed.
Audio: a thump on the dugout roof, a towel whoosh, a big crowd roar, no speech, no music. No subtitles, no on-screen text.
```
**Phủ định (Negative):** `subtitles, captions, on-screen text, watermark, misspelled lettering, mirrored lettering, extra letters, wrong number, extra patches, patch on the stomach, readable stadium names, jersey stretched flat like a sticker, music, plastic texture, uncanny face, extra fingers, distorted paws, extra limbs, body passing through the car or door, clipping through objects, floating objects, morphing, duplicated mascot, teleporting, sliding feet, warped background`
**Soát clip:** Brew Crew script across the chest đúng chữ (mở cúc làm tách là tự nhiên), số 24 below the script · patch World Series wearer's left chest, NL Champions left sleeve · tiếp đất bằng chân trên nóc dugout · áo trên vai như áo thật

## Clip 3 · 8s · Chỉ patch NL Champions → vỗ ngực, cúi chào, lộ lưng
**Khung đầu (ingredients):** `product.png`, `keyframe_c3.png`, `barley_sheet.png` · **Lưu video thành:** `c03_a.mp4`

**Cảnh:** nửa đầu ngón tay mascot gõ hai cái vào patch NL Champions ở tay trái; nửa sau camera lùi ra và vòng ra sau, mascot vỗ ngực hai cái, cúi chào khán đài, lưng CONTRERAS 24 hiện ra.
```
Close-up, then the camera pulls back and arcs around behind the mascot. In the first half the mascot's furry right paw taps the gold NATIONAL LEAGUE CHAMPIONS 2026 patch on its left sleeve twice; the patch stays sharp with every letter unchanged. In the second half the camera pulls back and arcs around to its back while the mascot, standing on the grass, pats its chest twice with both paws and takes a deep theatrical bow toward the stands, revealing CONTRERAS arched above a large number 24 on the back of the jersey, sharp and readable.
Real human being filmed on a phone: natural skin with pores and slight unevenness, real eyes with reflections, hair with individual strands, clothing that creases and hangs with weight. Every movement obeys physics: feet stay on the ground, weight shifts before a step, hands grip objects with correct finger placement and stay on their surfaces, bodies and clothes keep clear of the car, the door, the ground and each other, objects keep their size and weight. One continuous action at real speed.
Audio: soft taps on fabric, a crowd cheer, no speech, no music. No subtitles, no on-screen text.
```
**Phủ định (Negative):** `subtitles, captions, on-screen text, watermark, misspelled lettering, mirrored lettering, extra letters, wrong number, blurry patch, extra patches, patch on the stomach, jersey stretched flat like a sticker, music, plastic texture, uncanny face, extra fingers, distorted paws, extra limbs, body passing through the car or door, clipping through objects, floating objects, morphing, duplicated mascot, teleporting, sliding feet, warped background`
**Soát clip:** patch NATIONAL LEAGUE CHAMPIONS 2026 trên wearer's left sleeve đúng chữ · khi quay lưng: back reads CONTRERAS arched over a large 24 · không patch ở bụng · áo trên vai như áo thật

## Clip 4 · 8s · Đập tay fan nhí → chỉ xuống, pháo giấy
**Khung đầu (ingredients):** `product.png`, `keyframe_c4.png`, `barley_sheet.png` · **Lưu video thành:** `c04_a.mp4`

**Cảnh:** nửa đầu Barley đập tay với bé, bé cười, bố vỗ tay; nửa sau Barley đứng thẳng ở lối đi, quay về camera, chỉ xuống dưới khung, pháo giấy vàng rơi khắp khán đài.
```
Medium shot, static. The mascot stands in the concrete aisle between rows of seats, leaning toward the smiling boy in the same powder-blue jersey who sits in the aisle seat beside his father. In the first half the mascot and the boy high-five, paw to palm, the boy laughing and his father clapping; nobody leaves their place. In the second half the mascot straightens up in the aisle, turns to face the camera with the gold Brew Crew script across its chest, and points down toward the bottom of the frame with its right paw while gold confetti drifts down over the stands.
Real human being filmed on a phone: natural skin with pores and slight unevenness, real eyes with reflections, hair with individual strands, clothing that creases and hangs with weight. Every movement obeys physics: feet stay on the ground, weight shifts before a step, hands grip objects with correct finger placement and stay on their surfaces, bodies and clothes keep clear of the car, the door, the ground and each other, objects keep their size and weight. One continuous action at real speed.
Audio: a high-five clap, a child laughing, crowd noise, no speech, no music. No subtitles, no on-screen text.
```
**Phủ định (Negative):** `subtitles, captions, on-screen text, watermark, misspelled lettering, mirrored lettering, extra letters, wrong number, readable stadium names, jersey stretched flat like a sticker, music, plastic texture, uncanny face, extra fingers, fused fingers, distorted paws, distorted hands, extra limbs, body passing through the car or door, clipping through objects, floating objects, morphing, duplicated person, teleporting, sliding feet, warped background`
**Soát clip:** Brew Crew script across the chest trên áo mascot, patch World Series wearer's left chest · áo bé đúng chữ nếu thấy · mascot đứng ở lối đi, bé ngồi ghế, không xuyên ghế · tay bé đủ ngón

## Thiết lập khi gen video
- Cả 4 clip: Omni 1.1 Flash, chế độ **Thành phần** (ingredients): ảnh sản phẩm trước, keyframe sau, rồi sheet mascot; 8 giây, dọc 9:16, tải **1080p** (không chọn tuỳ chọn tính tín dụng).
- Tiếng clip không dùng: video dùng nhạc sports hype rap khi dựng (bài chưa project nào dùng).
- Sau khi gen: `gen_review.py brewers-contreras-24-mascot`, soát theo `placement_checks`, đánh dấu pass/fail trước khi dựng.
