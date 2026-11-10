# Model reference

Typical behaviour as of mid-2026. These tools ship changes monthly: when the
user says their version behaves differently, follow the user. The machine-readable
limits (durations, word ranges) live in `../models.json`, and both scripts use
the key in brackets after each heading.

This studio generates in Google Flow only: clips with Omni 1.1 Flash (linted with the `veo` key, same prompt syntax), stills with Nano Banana (`house-rules.md`). Sections for other tools were removed on 2026-11-10; they are in git history.

## Google Veo 3 / 3.1 [veo]

**Order:** subject -> action -> style -> camera -> composition -> focus/lens ->
ambiance -> audio.

- **Dialogue:** colon form without quotes: `She says: Okay, wait, look at
  this.` Quotes tend to burn subtitles into the video. Also add
  `no subtitles, no on-screen text`.
- Lines short: under about 20 words, under 8 seconds each.
- Describe sound explicitly: room tone, rain, kettle click, `no music`.
- **Native audio is reliable in text-to-video.** With an image input, audio is
  often missing. For a reference image plus speech, use Ingredients (up to 3
  reference images) instead of first-frame.
- **Durations:** 4, 6 or 8 s (8 s for 1080p and reference jobs). 9:16 native.
- For UGC say `phone camera quality, not cinematic`, otherwise Veo goes glossy.
  A selfie from slightly below the chin reads more real than eye level.

```
Veo 3.1, 8s, 9:16, text-to-video
A woman in her late 20s, messy bun, oversized grey hoodie, films herself in her
own small bedroom at night, a lamp on the nightstand. Shot on a phone front
camera, vertical, handheld micro-shake, real skin tones, natural skin texture,
no color grading. She holds the mug warmer up, mostly looking at it, glances at
the lens once.
She says: Okay, my coffee has been hot for two hours. Two.
She sets the mug down on the warmer, steam rises.
Audio: her voice and quiet room tone only, no music. No subtitles, no on-screen text.
Negative: subtitles, captions, on-screen text, ring light, beauty filter, cinematic grading
```

## Any other tool [generic]

Use the default order from the guide, keep one action and one camera move per
clip, 5-10 s clips, voiceover in post.

---

## Reference frames with an image model

For keyframes built from the product photo (a person holding it, a new
setting, a start or end state), follow `keyframes.md`; it has the prompt order,
the image model table and the checks. The two prompts below are the basic
reference images.

Generate stills first when there is no real photo, for a character sheet, or
for a styled first frame:

```
Character reference sheet, one image, 16:9: three full-body views (front, side,
back) on the left, one chest-up close-up on the right, plain light-grey
background, even soft light. [CHARACTER lock]. [STYLE lock].
```

```
Product reference shot, centered, 9:16, on [surface], [light]. [PRODUCT lock].
[STYLE lock]. Sharp focus, logos and markings exactly as on the real product,
no added text.
```

Image models render short text far better than video models. Even so, add
prices and captions in the edit.
