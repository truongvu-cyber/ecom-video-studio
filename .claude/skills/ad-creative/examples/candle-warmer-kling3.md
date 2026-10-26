# Candle warmer lamp - AI video prompts

Worked example of a full run from a product photo and the name "candle warmer
lamp with timer": a 20-second Reel for a US audience.

**What Claude showed before the prompts (Stage 2):**
1. A matte black lamp that melts a jar candle from the top; the 3-second proof
   is the wax surface turning glossy under the glow.
2. Direction: mood transformation, cozy evening (angle row 3, genre #3, style
   #6), Kling 3.0 image-to-video, 20 s, hands plus one person, voiceover in post,
   because the product sells a feeling and is in its winter peak.
3. Hook: "No flame, no match. Your candle, 2 hours later." (not picked: "My
   candle lasts twice as long now" - an unmeasured claim; "POV: you finally
   stopped buying lighters" - weaker proof in frame one).
4. Assumed: the timer dial on the base (not visible in the photo, confirmed by
   the name); size taken from a standard jar candle.
5. Alternatives: (2) satisfying ASMR macro, 10 s, no people; (3) gift angle "for
   the friend who burns candles all winter", festive style #7.
Plan from `shotplan.py script.txt --model kling3 --target 20` on this script
(spoken as voiceover and on-screen lines; clip 3 keeps one line in native audio):

```
No flame, no match. Your candle, 2 hours later.
This lamp melts the wax from the top, so the whole room smells like it.
Set the timer, get in bed, and it shuts itself off.
It looks like a little reading lamp on my nightstand.
Comment GLOW and I will send you the link.
```

shotplan gives five clips to generate at 4 / 6 / 4 / 4 / 4 s (22 s) and to use at
3.3 / 5.5 / 4.0 / 3.6 / 3.3 s (19.6 s).

| Tool | Ratio | Length | Clips | Style | Genre | Audio |
|------|-------|--------|-------|-------|-------|-------|
| Kling 3.0 image-to-video | 9:16 | 20s | 5 | #6 Cozy hygge home | Problem -> solution | Native audio, one spoken line in clip 3 |

**Why this, here, now:** a woman in her own small bedroom on a rainy evening
wants her candle's smell without leaving a flame burning while she reads, and
films the lamp because a friend asked what it is.

## Locks (paste word for word, never rephrase)

**CHARACTER - Mara:**
woman in her early 30s, shoulder-length dark brown hair in a loose claw clip, light olive skin, small silver hoop earrings, oversized oat-coloured knit sweater

**PRODUCT:**
matte black metal candle warmer lamp with a small dome shade, thin curved arm, round walnut-wood base, a jar candle with an amber glass jar under the shade

**STYLE:**
Warm cozy home footage, tungsten lamp light and candle glow, soft blankets and knit textures, rain visible on the window, amber and cream palette, gentle slow camera, intimate quiet mood, small lived-in bedroom at 9pm, light from the right, 35mm look, vertical 9:16

**AUDIO:** quiet room tone, soft rain on the window, no music

**NEGATIVE:** blur, distortion, flicker, warped product, changed shade shape, extra objects, distorted face, extra fingers, text, subtitles, watermark, logo

## Step 0 - Reference images

1. Product: the real photo of the lamp over the candle, lamp off, plain background.
2. Character: no real photo of Mara, so generate a sheet first (Nano Banana Pro):
   ```
   Character reference sheet, 16:9: three full-body views (front, side, back) on the left, one chest-up close-up on the right, plain light-grey background, even soft light. woman in her early 30s, shoulder-length dark brown hair in a loose claw clip, light olive skin, small silver hoop earrings, oversized oat-coloured knit sweater. Warm cozy home footage, tungsten lamp light and candle glow, soft blankets and knit textures, rain visible on the window, amber and cream palette, gentle slow camera, intimate quiet mood, small lived-in bedroom at 9pm, light from the right, 35mm look, vertical 9:16
   ```

## Keyframes (generate and check these before any clip)

One per clip, all on Nano Banana Pro, all from the real product photo. From
keyframe 2 on, add keyframe 1 as an extra reference so the room and light match.

### Keyframe 1 · for clip 1 · Nano Banana Pro
**References:** image 1 = product photo · **Save as:** keyframe_c1.png
```
Image 1 is the product: a matte black metal candle warmer lamp with a small dome shade, a thin curved arm and a round walnut-wood base, over an amber glass jar candle. Keep it exactly as in image 1: same shape, proportions, colours and finish; do not redraw, restyle, duplicate it or add any text.

The lamp stands switched off on a wooden nightstand, the candle wax solid and matte. A woman's right hand enters from the right edge of the frame, index finger hovering just above the switch on the lamp's base, not yet pressing it.

Warm cozy home footage, tungsten lamp light and candle glow, soft blankets and knit textures, rain visible on the window, amber and cream palette, gentle slow camera, intimate quiet mood, small lived-in bedroom at 9pm, light from the right, 35mm look, vertical 9:16

Close-up at the height of the nightstand, the lamp and candle sharp in the centre, the upper third dim and clear for an overlay. One lamp only, no text, no watermark, natural hand with five fingers.
```
**Check before animating:** lamp shape and shade match the photo · lamp off · finger not touching yet

### Keyframe 2 · for clip 2 · Nano Banana Pro
**References:** image 1 = product photo, image 2 = keyframe_c1.png · **Save as:** keyframe_c2.png
```
Image 1 is the product: a matte black metal candle warmer lamp with a small dome shade, a thin curved arm and a round walnut-wood base, over an amber glass jar candle. Keep it exactly as in image 1: same shape, proportions, colours and finish; do not redraw, restyle, duplicate it or add any text. Image 2 shows the room; keep its light and nightstand.

Macro view of the candle under the lit lamp: the warm light falls on the wax surface, which is just starting to turn glossy at the centre while the edges are still solid.

Warm cozy home footage, tungsten lamp light and candle glow, soft blankets and knit textures, rain visible on the window, amber and cream palette, gentle slow camera, intimate quiet mood, small lived-in bedroom at 9pm, light from the right, 35mm look, vertical 9:16

Extreme close-up from slightly above, the glossy centre of the wax in the middle of the frame, the lower edge of the dome shade visible at the top. No text, no watermark.
```

### Keyframe 3 · for clip 3 · Nano Banana Pro
**References:** image 1 = product photo, image 2 = Mara's character sheet, image 3 = keyframe_c1.png · **Save as:** keyframe_c3.png
```
Image 1 is the product: a matte black metal candle warmer lamp with a small dome shade, a thin curved arm and a round walnut-wood base, over an amber glass jar candle. Keep it exactly as in image 1: same shape, proportions, colours and finish; do not redraw, restyle, duplicate it or add any text. Image 2 is the woman; keep her face, hair and outfit. Image 3 shows the room; keep its light and nightstand.

woman in her early 30s, shoulder-length dark brown hair in a loose claw clip, light olive skin, small silver hoop earrings, oversized oat-coloured knit sweater sits up in bed under a cream blanket, her right hand reaching toward the lamp on the nightstand, fingers just touching the timer dial on its wooden base, a closed paperback in her left hand. The lamp is on and the wax is already glossy.

Warm cozy home footage, tungsten lamp light and candle glow, soft blankets and knit textures, rain visible on the window, amber and cream palette, gentle slow camera, intimate quiet mood, small lived-in bedroom at 9pm, light from the right, 35mm look, vertical 9:16

Medium shot at eye level, the lamp sharp in the right third of the frame, the upper third kept clear for an overlay. Natural skin texture, real fabric folds, no beauty filter. One lamp only, nothing else in her right hand, no text, no watermark, natural hands with five fingers.
```

### Keyframe 4 · for clip 4 · Nano Banana Pro
**References:** image 1 = product photo, image 2 = keyframe_c1.png · **Save as:** keyframe_c4.png
```
Image 1 is the product: a matte black metal candle warmer lamp with a small dome shade, a thin curved arm and a round walnut-wood base, over an amber glass jar candle. Keep it exactly as in image 1: same shape, proportions, colours and finish; do not redraw, restyle, duplicate it or add any text. Image 2 shows the room; keep its light and nightstand.

The lamp glows on the nightstand with the wax fully melted and glossy, beside a paperback and a half-full mug, looking like a small reading lamp. No person in frame.

Warm cozy home footage, tungsten lamp light and candle glow, soft blankets and knit textures, rain visible on the window, amber and cream palette, gentle slow camera, intimate quiet mood, small lived-in bedroom at 9pm, light from the right, 35mm look, vertical 9:16

Close-up with shallow depth of field, the lamp sharp in the left half of the frame, the bed blurred behind it. One lamp only, no text, no watermark.
```

### Keyframe 5 · for clip 5 · Nano Banana Pro
**References:** image 1 = product photo, image 2 = keyframe_c1.png · **Save as:** keyframe_c5.png
```
Image 1 is the product: a matte black metal candle warmer lamp with a small dome shade, a thin curved arm and a round walnut-wood base, over an amber glass jar candle. Keep it exactly as in image 1: same shape, proportions, colours and finish; do not redraw, restyle, duplicate it or add any text. Image 2 shows the room; keep its light and nightstand.

The whole small bedroom at night, rain on the window, the lamp on the nightstand the only warm light, the bed made with the cream blanket, nobody in the room.

Warm cozy home footage, tungsten lamp light and candle glow, soft blankets and knit textures, rain visible on the window, amber and cream palette, gentle slow camera, intimate quiet mood, small lived-in bedroom at 9pm, light from the right, 35mm look, vertical 9:16

Medium-wide shot from the doorway, the lamp in the lower right third, the dark upper third of the frame empty for the call-to-action overlay. One lamp only, no text, no watermark.
```

## Clip 1 · 4s · Hook
**Reference:** keyframe_c1.png · **First frame:** keyframe_c1.png
```
Close-up, static. The finger presses the switch; the lamp glows on at once and warm light lands on the wax. Audio: a soft click, quiet room tone, soft rain on the window, no music.
```
**Negative:** `blur, distortion, flicker, warped product, changed shade shape, extra objects, extra fingers, text, subtitles, watermark`
**Overlay (edit):** "No flame. No match."

## Clip 2 · 6s · Proof
**Reference:** keyframe_c2.png · **First frame:** keyframe_c2.png
```
Macro, slow push in toward the candle. The glossy centre of the wax spreads outward in an even ring until the whole surface is liquid, a thin wisp of warm air shimmering above it. Audio: quiet room tone, soft rain on the window, no music.
```
**Negative:** `blur, distortion, flicker, warped product, extra objects, text, subtitles, watermark`

## Clip 3 · 4s · Build
**Reference:** keyframe_c3.png · **First frame:** keyframe_c3.png
```
Medium shot, eye level, static. She turns the timer dial a quarter turn, lets go, and settles back against the pillow, opening the paperback. She says softly, offhand: "Timer's on. I'm not getting up." The candle glow flickers gently on the wall behind her. Audio: her voice, quiet room tone, soft rain on the window, no music.
```
**Negative:** `distorted face, extra fingers, outfit change, warped product, text, subtitles, watermark`

## Clip 4 · 4s · Build
**Reference:** keyframe_c4.png · **First frame:** keyframe_c4.png
```
Close-up, static, shallow depth of field. The lamp glows steadily; the candle light flickers softly on the mug and the paperback, a faint shimmer rising from the melted wax. Audio: quiet room tone, soft rain on the window, no music.
```
**Negative:** `blur, flicker, warped product, extra objects, text, subtitles, watermark`

## Clip 5 · 4s · CTA / end
**Reference:** keyframe_c5.png · **First frame:** keyframe_c5.png
```
Medium-wide shot, slow pull back toward the doorway. Rain streaks down the window while the lamp keeps glowing on the nightstand, the room otherwise dark and still. Audio: quiet room tone, soft rain on the window, no music.
```
**Negative:** `blur, flicker, warped product, people, text, subtitles, watermark`
**Overlay (edit):** "Comment GLOW for the link" in the empty upper third.

## Edit guide
1. Generate and check keyframes 1-5 first, then clips 1-5.
2. Clips in order, trimmed to 3.3 / 5.5 / 4.0 / 3.6 / 3.3 s.
3. Hard cuts; match cut from clip 1's lit wax to clip 2's macro.
4. Overlays inside the safe zone; captions on.
5. Export 1080x1920, 30fps, H.264.
