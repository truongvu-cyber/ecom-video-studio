# Keyframes: reference images for each clip

**Every clip gets a keyframe.** Before each video prompt, write an image
prompt: product photo + prompt -> keyframe image. The user generates it, checks
it, and uses it as the first frame of that clip's video. This keeps the real
product in every clip and gives every generation a proper start image, whether
the clip shows a person lying in bed holding the product or the product alone
on a table.

```
product photo (+ character sheet)  ->  image model + keyframe prompt  ->  keyframe_c1.png
keyframe_c1.png                    ->  video model + clip 1 prompt (motion only)  ->  clip 1
```

Without a product (a story, an anime scene, a travel clip), the keyframe is
generated from the description and whatever references the user has (a
character sheet, a location photo); the rest of this file applies the same way.

## 1. One keyframe per clip

| the clip opens on... | keyframe |
| --- | --- |
| the product alone | the product placed in the clip's setting and light, framed as the clip starts |
| a person with the product | person + product in the pose just before the action |
| the same shot where the previous clip ended | its own keyframe, with the previous keyframe as an extra reference so room and light match |
| a change between two states (lamp off -> on) on Kling or Luma | a start keyframe **and** an end keyframe |
| a moment the user will film for real | no keyframe and no video prompt; note what the filmed shot must match |

Every clip header says `First frame: keyframe_cN.png`. Name them by clip number
(`keyframe_c1.png`, `keyframe_c2.png`, end frames `keyframe_c2_end.png`).

## 2. Reference images first

- **Product:** the clearest real photo: whole product visible, plain background,
  even light, no hand covering the distinctive detail. If the only photo is
  busy or cropped, the first keyframe prompt is a clean product shot.
- **Character sheet** (only if the same person appears in more than one clip):
  generate it once (prompt in `output-template.md`, Step 0) and pass it with the
  product photo to every keyframe that shows the person.
- **Earlier keyframe:** for the second and later keyframes in one location, add
  the first keyframe as a reference too, so the room and light stay the same.

## 3. The keyframe prompt

Write it in this order. Every keyframe repeats the CHARACTER and STYLE locks
word for word, like the video prompts.

1. **Reference roles.** Say what each uploaded image is and what to keep:
   `Image 1 is the product. Keep it exactly as in image 1: same shape,
   proportions, colours, materials, buttons, logos and markings. Do not redraw,
   restyle, resize oddly, duplicate it or add any new text.`
   With a character sheet: `Image 2 is the woman; keep her face, hair and
   outfit.`
2. **The moment.** The instant **before** the clip's action, so the video has
   something to animate: thumb resting on the button with the lamp still off;
   the mug lifted just above the warmer; the cover folded in her hands.
3. **Subject and grip.** CHARACTER lock, pose, where the product is, which hand
   holds it and how (`held in her right hand at chest height, fingers wrapped
   around the base, the front button facing the camera`). Product size relative
   to the hand or body.
4. **Place and light.** STYLE lock: location, time of day, light direction,
   palette, 2-3 lived-in background details.
5. **Framing = the clip's first frame.** Shot size, angle, lens feel, where the
   product sits in the frame, room for the planned camera move, the top 15% and
   bottom 20% kept free for overlays. **Ratio 9:16** (vertical).
6. **Realism or style cues** from the style block: phone photo, natural skin
   texture, real fabric folds; or the animated style's words.
7. **Exclusions:** `one product only, no extra objects in her hands, no text,
   no captions, no watermark, natural hands with five fingers`.

### Example: person in bed holding the product

```
Image 1 is the product: a matte white dome LED aurora projector on a round
base with one button on the front. Keep it exactly as in image 1: same shape,
proportions, colours and button; do not redraw, restyle, duplicate it or add
any text.

A woman in her late 20s, shoulder-length dark brown hair, oversized grey
hoodie, lies on her back in bed under a cream knit blanket at night, holding
the projector from image 1 in both hands on her chest, her right thumb resting
on the front button, the projector still off. Her face is relaxed, looking up
at the ceiling.

Her own small bedroom: a nightstand with a phone charger and a half-full mug at
the edge of frame, warm light from a small bedside lamp on the left, the rest of
the room dim, plain dark ceiling above her.

High-angle medium shot from above the bed, phone-camera look, vertical 9:16,
the projector sharp in the lower-middle of the frame, empty dark ceiling space
in the upper third. Natural skin texture, real fabric folds, no beauty filter.

One product only, nothing else in her hands, no text, no watermark, natural
hands with five fingers.
```

The clip 1 video prompt then starts from this image and only adds motion:
`Her thumb presses the button; green and blue aurora light spreads across the
ceiling and her face. Static camera.`

## 4. Image models

Typical behaviour in 2026; check the tool's current limits and follow the user
when they differ.

| model | references | good for | watch out |
| --- | --- | --- | --- |
| Nano Banana Pro / Nano Banana 2 (Google) | up to 14 images; 1K-4K; 9:16 supported | default: product fidelity, person + product, edits in plain language | describe what each reference is and what to keep |
| Nano Banana (original) | up to 3 images, 1K | quick drafts | low resolution for 1080p video |
| Seedream 4.x (ByteDance) | many references (4.5: up to 14), 2K-4K | multi-reference scenes, consistent sets | confirm the 9:16 size preset |
| GPT Image (ChatGPT) | uploaded images in chat | strong instruction following, text rendering | portrait is usually 2:3: extend or crop to 9:16 |
| Flux Kontext | one image edited | changing the scene around an existing photo | one reference at a time |
| Midjourney | omni-reference, `--ar 9:16` | styled and animated looks | loose with exact product details: avoid for exact products |
| Kling image / Elements | Kling's own references | staying inside Kling | check product detail closely |

When the user does not name one, write for Nano Banana Pro and keep the prompt in
plain sentences, so it also works elsewhere.

Logos, team marks and printed designs on the product are kept exactly as in the
photo by default (`keep the logo and lettering exactly as in image 1`). Remove a
mark only when the user asks: `remove the printed mark from the base; keep
everything else`.

## 5. Check every keyframe before animating it

1. **Product:** side by side with the real photo: shape, proportions, colour,
   buttons, markings. Any drift, regenerate now; video will not fix it.
2. **Hands and body:** five fingers, a grip that could hold the product's
   weight, no merged limbs.
3. **Frame:** 9:16 at 1080x1920 or more, the product where the planned move needs
   it, safe zones clear.
4. **Start state:** the moment before the action (lamp off, wax still solid).
5. **No fake text** anywhere.

Fix the prompt, not the image: name the failure in the next attempt ("the
projector has one button on the front, not two").

## 5b. Placement checks — strict review after every generation (user rule 2026-10-27)

Looking "roughly right" is not a pass. `product.json` carries
`placement_checks`: the things that must be true about **where the product
is and what state it is in**, written per product, e.g.

- door light: "unit stuck under the inner door panel, lens pointing down",
  "logo on the ground only while the door is open; dark ground when closed",
  "logo directly below the door edge, not under the seat or the wheel".
- apparel: "print centred on the chest, top edge two fingers below the
  collar", "name on the back between the shoulder blades", "logo not
  mirrored".
- mug / bottle: "print faces the camera, handle on the right".

What is **not** a failure (user rule 2026-10-27) — keep it natural, do not regenerate or
"fix" it in prompts:

- a jersey, shirt or jacket worn **open/unbuttoned** whose chest script splits across the
  placket ("Brew" on one panel, "Crew" on the other) or folds with the fabric;
- print partly hidden by an arm, hair, a fold or a hand for a moment;
- print seen at an angle or in motion blur during a real action (putting it on, a spin).

A failure is the print **itself** being wrong: misspelled or invented letters, wrong number,
mirrored text, a patch moved to another place, wrong colours.

Rules:

1. Every keyframe's `Soát trước khi làm video` line and every clip's
   `**Soát clip:**` line **repeat the placement checks that apply** to that
   shot, plus the shot's own checks (letters, hands, start state).
2. After `--stage images`, run `scripts/gen_review.py <id>` and read
   `edit/qc/gen_review.jpg` (every keyframe with its check list under it).
   After `--stage clips`, run it again: every clip as a 1-frame-per-second
   strip with its checks. A failed check is fixed **before the next stage
   starts**: rewrite the sentence of the prompt that governs that detail,
   regenerate that one job (`flow_run.py … --only <job>`), review again.
3. The review is written down: `gen_review.py --mark <job> pass|fail "<why>"`
   appends to `edit/gen_review.jsonl`; a clip without a `pass` mark is not
   handed to ad-editor (`validate.py` reports it).

## 6. Hand-off to the video prompt

The clip header names the keyframe file. The video prompt then describes motion
and camera only. It does not re-describe the product or the person, because
re-describing them in other words makes the video model drift from the image.
For Kling start + end, write both keyframes and a prompt for the change between
them.
