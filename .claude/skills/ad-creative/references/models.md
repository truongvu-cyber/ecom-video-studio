# Model reference

Typical behaviour as of mid-2026. These tools ship changes monthly: when the
user says their version behaves differently, follow the user. The machine-readable
limits (durations, word ranges) live in `../models.json`, and both scripts use
the key in brackets after each heading.

## Picking a model

| need | first choice | why |
| --- | --- | --- |
| a real product photo brought to life | Kling 3.0 image-to-video | best motion from a still, keeps the product |
| a person AND a product both kept faithful | Kling 3.0 Omni multi-image | binds two reference images at once |
| someone talking to camera with native speech | Veo 3.1 | strongest lip-synced dialogue from text |
| several beats with cuts in one generation | Kling 3.0, Sora 2, Seedance 2 | multi-shot in one output |
| natural human body motion, dance | Seedance | strongest human movement |
| cheap fast iteration | Hailuo, Veo Fast, Seedance 1 | low cost per clip |
| stylised looks, strict camera control | Runway, Luma | keyframes and references |
| a still reference frame or character sheet | an image model (Nano Banana, GPT Image, Flux, Midjourney) | then animate it |

Pick one model for the whole video when possible. Mixing models mixes looks.

---

## Kling 2.x [kling] and Kling 3.0 / Omni [kling3]

**Formula (official order):** camera language + light -> subject -> subject
motion -> scene -> atmosphere. Simple words, short sentences.

- **Image-to-video:** the first frame carries the look. The prompt describes
  motion and camera only. The output ratio is inherited from the input image, so
  feed a 9:16 image for a 9:16 clip.
- **End frame:** start + end image interpolates between them. Good for reveals
  and for chaining clips.
- **Durations:** 2.x gives 5 or 10 s. 3.0 accepts 3-15 s.
- **Multi-shot (3.0 only):** up to 6 labeled shots in one output, each with a
  duration. Older versions: one shot, one beat.
- **Audio (3.0 only):** native audio with lip-sync. State who speaks and when;
  put tone as a modifier (`warm, amused voice`). 2.x: no audio, dub in post.
- **References:** the app binds people and products through Elements slots. The
  official API uses `<<<image_1>>>`, `<<<image_2>>>` (Omni) and
  `<<<element_1>>>` for a registered subject. Write `@product` / `@avatar` in the
  prompt and tell the user what to bind them to.
- **cfg_scale:** about 0.3-0.5 for more motion, 0.7-0.9 to stick to the prompt.
- **Negative field:** supported. Default it to blur, distortion, low quality,
  then add the style's negatives.
- **Strong camera words:** orbit, 360 orbit (products), dolly push, crash zoom,
  whip pan, tracking, macro close-up, POV, time freeze.

```
Kling 2.x, image-to-video, 5s, 9:16
Slow dolly in, soft window light from the left. The candle warmer lamp
@product switches on, its warm glow spreads over the wax and the surface
begins to melt evenly. A dim bedroom nightstand at night, a paperback and a
charging cable soft in the background. Calm, cozy atmosphere.
Negative: blur, distortion, low quality, flicker, warped product, extra
objects, text, watermark
```

```
Kling 3.0 multi-shot, 12s total, 9:16, audio on
Shot 1 (3s): Close-up, handheld. A woman's hand clicks the lamp @product on.
Shot 2 (4s): Macro, locked off. Wax surface turns glossy and melts in a ring.
Shot 3 (5s): Medium shot, slight push in. She sits on the bed with a mug,
glances at the candle, small smile. She says softly: "No match, no flame."
Style: warm cozy home footage, tungsten lamp glow, amber and cream palette, 9:16.
Audio: quiet room tone, faint rain on the window, no music.
Negative: blur, distortion, flicker, warped product, extra fingers, text, subtitles
```

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

## Sora 2 [sora]

Prefers a labeled, sectioned prompt over one prose block.

```
[Prose: setting, subject, look, real-feel or style anchors.]

Cinematography:
Camera shot: [framing, angle, ratio]
Mood: [one or two words]

Actions:
- [beat 1, one action]
- [beat 2]
- [final beat, how the clip ends]

Dialogue:
- @avatar: "Short natural line."

Background Sound:
[ambience, music or no music]
```

- One clear camera move and one action per shot. Sparse = more creative,
  dense = more consistent. Quotes are fine in the Dialogue block.
- **Durations:** 4, 8, 12, 16, 20 s; can extend. Up to about 6 beats or shots
  in one generation. Sizes 720x1280 / 1080x1920.
- First frame via an input image matching the output size. Characters (cameos)
  are consent-gated.
- No negative field: write the wanted result positively.

## Seedance 1.0 / 1.5 [seedance] and Seedance 2.x [seedance2]

- **Order 2.x:** subject -> action -> environment -> camera -> style ->
  constraints. **Order 1.x:** subject + action -> scene -> camera -> style.
- **60-100 words** (2.x tolerates up to about 120), natural sentences, one
  primary camera move. Lighting
  description moves quality the most. **Never use "fast"**: it is the single
  biggest quality killer.
- **1.x:** no audio, first/last frame only, params as suffixes
  (`--ratio 9:16 --duration 5 --camerafixed false`), no negative field (use an
  `Avoid:` clause).
- **2.x:** native audio and lip-sync, up to 9 reference images as `@Image1` ...
  `@Image9` (also `@Video1`, `@Audio1`), duration 4-15 s, up to about 4
  labeled shots in one generation. Rejects real human faces
  as references; use Kling Omni for a real person.

```
Seedance 2.0, 8s, 9:16
A woman in her thirties (@Image1) sits at a kitchen table in soft morning
window light, a laptop and a plant at the edge of frame. She lifts the gravity
pepper grinder (@Image2), tips it over a plate of eggs, and its small light
glows as pepper falls. Handheld, slight low angle, vertical. Real skin tones,
natural phone look, no color grading. She says, offhand: "One hand. That's it."
Avoid: cinematic grading, ring light, gift box, on-screen text.
```

## Hailuo / MiniMax [hailuo]

- No native audio. Write spoken lines as acting direction and dub in post.
- Camera commands in square brackets, up to three: `[Push in]`, `[Pull out]`,
  `[Pan left]`, `[Truck right]`, `[Pedestal up]`, `[Tilt down]`, `[Zoom in]`,
  `[Shake]`, `[Tracking shot]`, `[Static shot]`.
- Subject reference from one clear image (one subject only). 6 or 10 s.
- The prompt optimizer rewrites prompts; turn it off for tight control.

## Runway Gen-4 family [runway]

- Strong camera and motion control from a reference image; little or no speech.
- Keep subject words identical across clips; reuse the same reference and seed.
- 5 or 10 s. Short prompts focused on camera + motion.

## Luma Ray [luma]

- Start and end keyframes carry continuity; the prompt describes the motion
  between them. 5, 9 or 10 s; extend for longer takes. Limited speech.

## Wan 2.x [wan]

- Open model, negative field supported, good value for B-roll. 5 or 10 s.

## Higgsfield and other front-ends

They route to the models above. Write for the underlying model the user picks
inside them, and use the front-end's character or preset features for
consistency.

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
