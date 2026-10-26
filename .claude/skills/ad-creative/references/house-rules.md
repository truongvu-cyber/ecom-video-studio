# House rules: Veo 3 + Nano Banana, built for the Editor

These rules override the defaults in `product-analysis.md` and `models.md`
(which assume Kling). They exist because Agent 2 (ad-editor) cuts the clips
automatically: every clip must give it room to cut, clean audio to keep, and
one consistent voice.

## Models

| job | default | note |
| --- | --- | --- |
| video | **Veo 3 / 3.1** (`--model veo`) | 4, 6 or 8 s per generation; write for **8 s** (1080p, reference jobs) |
| image (keyframes) | **Nano Banana Pro** (`--image-model nano-banana-pro`) | the user calls it "Nano Banana". If they only have the original Nano Banana: max 3 references, 1K output — tell them keyframes will be soft at 1080p |

## Clip architecture (the core rule)

A 15-20 s ad = **one dialogue clip + 3-5 B-roll clips**, all generated at 8 s.
The Editor uses only 2-4 s of each B-roll clip and splits the dialogue clip
across the timeline.

| clip | what | how to generate | audio | production.json |
| --- | --- | --- | --- | --- |
| `c01` | **A-roll / dialogue**: one person talks to camera with the product | Veo **Ingredients / reference images** (keyframe_c01 + product photo + design file), not first-frame: first-frame jobs often come back without sound | all spoken lines + room tone | 2-3 shots share `file_pattern: "c01*.mp4"`, `audio_type: dialogue`, each with its own `dialogue` line |
| `c02`… | **B-roll**: product close-up, personalization moment, unboxing, worn/used, lifestyle | **first-frame image-to-video** from `keyframe_cN.png` (best product fidelity) | real sound of the action (fabric, paper, click) + room tone, **no speech, no music** | `audio_type: sfx` (or `music_only` when the sound adds nothing) |

Why one dialogue clip: within one generation Veo keeps one voice; across
generations the voice changes even with the same description. A VOICE lock is
written anyway (it helps a regenerate stay close) but it is not trusted.

### The dialogue clip (c01)

- **At most 18 spoken words in total**, as 2-3 short lines (each 3-8 words).
- Write the timing as acting direction:
  `She glances at the lens. A short beat of silence. She says: Wait, you can put his name on it?`
  `She pauses, turns the hoodie toward the camera. She says: Any name, any color.`
  `She smiles. She says: The link is right below.` then `She holds the pose, smiling, for a moment.`
- Begin with ~0.5 s of the person already in frame, not speaking; end with ~1 s
  holding the pose. The Editor needs silence around every line.
- Colon form, **no quotes** (quotes burn subtitles). Every prompt and negative
  says `no subtitles, no on-screen text`.
- Person + product framing: medium or medium close-up, product visible but the
  printed design does not need to be legible here (strict print shots are B-roll).
- `Audio: her voice, quiet room tone, no music.`

### B-roll clips (c02…)

- One action, one slow camera move (`slow push in`, `static`, `slow orbit 15°`).
  The Editor will take the cleanest 2-4 s, so the action may fill the 8 s.
- The **moment before the action** is the keyframe (see `keyframes.md`).
- `Audio: <the real sounds of the action>, quiet room tone, no speech, no music.`
- Shots with a printed name, number or logo: follow `pod-customize.md`
  section 2 and mark them `print_fidelity: strict`.

## Lengths in production.json

- `gen_sec`: 8 for every clip (or what the user actually generated).
- `use_sec`: B-roll 2-4 s; a dialogue shot = its line at 2.5 words/s + 0.5 s.
- `use_sec <= gen_sec - 1` always (margin for the Editor's beat snapping).
- Sum of `use_sec` within ±2 s of `spec.target_sec`.

## Never

- Text, prices, captions or names as overlay in the video prompt: they go in
  `overlay` for the Editor. The only text in a generated frame is the product's
  real print, coming from the keyframe.
- A second talking clip with a different speaker or voice, unless the user asks
  (then warn: voices will not match).
- Music in any Veo clip (the Editor adds licensed music).
- A person who could pass for the real player whose name or number is on the
  product (same sex, build, look, doing pro moves like dunks). Veo refuses these
  as "famous person" content, and it would imply an endorsement. Cast the wearer
  as an obvious fan who looks nothing like the player (different sex, age or
  build, everyday clothes around the jersey) and keep the action fan-level.
