# Output template

Two parts: the direction summary (Stage 2, shown before the prompts; a full
story table only when the user asked to approve the plan first), then the prompt
file (Stage 6). Replace everything in angle brackets. Name the file
`<subject-slug>-video-prompts.md`.

## Story draft (for approval)

```markdown
# <Title> - story draft

**Format:** <tool + version> · <ratio> · <length> · <dialogue language / VO / music> · <style #name> · <genre>
**Why this, here, now:** <the coherence sentence>
**Hook (first 2 s):** <what is already happening in frame one>
**Improved from your idea:** <one line>

| Clip | Time | Purpose | What we see | Spoken / VO | Overlay text (edit) |
|------|------|---------|-------------|-------------|---------------------|
| 1 | 0-5s | Hook | ... | ... | ... |
```

## Prompt file

````markdown
# <Title> - AI video prompts

| Tool | Ratio | Length | Clips | Style | Genre | Audio |
|------|-------|--------|-------|-------|-------|-------|
| <Kling 3.0> | <9:16> | <30s> | <5> | <#2 UGC phone> | <problem-solution> | <VO in post> |

## Locks (paste word for word, never rephrase)

**CHARACTER - <name>:**
<woman in her early 30s, shoulder-length dark brown hair in a loose clip, light
olive skin, small silver hoop earrings, oversized oat-coloured knit sweater>

**PRODUCT:**
<palm-sized cylindrical mug warmer, matte cream ceramic top, thin walnut-wood
base ring, one small round button on the front, no visible text>

**STYLE:**
<style block from styles.md> + <location, time of day, light direction, lens,
palette, motion language, ratio>

**AUDIO:** <quiet room tone, faint rain, no music>

**NEGATIVE:** <from styles.md and failure-modes.md>

## Step 0 - Reference images (before any clip)

1. Product: upload a real photo (best). Or generate one:
   ```
   Product reference shot, centered, 9:16, on <surface>, <light>. <PRODUCT>.
   <STYLE>. Sharp focus, logos and markings exactly as on the real product, no added text.
   ```
2. Character sheet (only if a person appears and no real photo is used):
   ```
   Character reference sheet, 16:9: three full-body views (front, side, back) on
   the left, one chest-up close-up on the right, plain light-grey background,
   even soft light. <CHARACTER>. <STYLE>.
   ```
3. Use these as references for every keyframe and clip below.

## Keyframes (generate and check these before any clip)

One per clip, in clip order. Every clip below starts from its keyframe. See
`keyframes.md`.

### Keyframe 1 · for clip 1 · <Nano Banana Pro>
**References:** image 1 = <product photo>, image 2 = <character sheet> · **Save as:** keyframe_c1.png
```
Image 1 is the product: <one line>. Keep it exactly as in image 1: same shape,
proportions, colours and markings; do not redraw, restyle, duplicate it or add
any text. <Image 2 is the person; keep her face, hair and outfit.>
<CHARACTER lock> <pose and grip>, <the moment just before the clip's action>.
<STYLE lock>
<framing of the clip's first frame>, vertical 9:16, <safe zones clear>.
<exclusions: one product only, no text, no watermark, natural hands>
```
**Check before animating:** product matches the photo · hands · 9:16 · start state

## Clip 1 · 5s · Hook
**Reference:** keyframe_c1.png · **First frame:** keyframe_c1.png
```
<the full prompt, locks pasted in>
```
**Negative:** `<...>`
**Spoken:** <speaker - line> · **Tip:** <save the last frame for clip 2>

## Clip 2 · 5s · <purpose>
...

## Voiceover / audio script (when the tool makes no speech)
| Time | Speaker | Line | Tone |
|------|---------|------|------|

**Music:** <genre, BPM, no vocals>

## Edit guide
1. Clips 1 -> N in order; cut on action or on the beat.
2. Transitions: <hard cuts; match cut on the product>.
3. Overlays: <hook text 0-2s, price, CTA> inside the safe zone (not the top 15%
   or bottom 20% of a 9:16 frame).
4. Captions on: most people watch muted.
5. End card: <logo, offer, CTA>.
6. Export: <1080x1920, 30fps, H.264>.

## If something looks off
- Face changed -> character sheet as reference, simpler action, same location.
- Product changed -> real photo as first frame, less motion.
- Light or colour jumps -> last frame as next first frame, colour-match in edit.
- Too glossy -> window light, no ring light, no color grading.
````

Quick prompts (one clip) skip the file: a code block with the prompt, then a
`**Negative:** `...`` line (or an `Avoid:` line inside the prompt when the model
has no negative field), then one line of settings (duration, ratio, audio
on/off, what to bind as reference).
