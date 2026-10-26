# Failure modes

What video models get wrong, how to write around it, and how to check the result.
Most of these hold across every model; the model notes say where one is worse.

## Writing around the usual failures

| trigger | what goes wrong | write this instead |
| --- | --- | --- |
| hands doing fine work | extra or melted fingers | simple grips, hands still or slow; or frame the product with hands out of shot; use a real photo as first frame |
| text, labels, prices, signs | garbled fake letters | no text in the prompt; add it in the edit. Very short quoted words ("SALE") sometimes survive |
| a visible logo or team mark | warped lettering | real photo or keyframe as first frame, less motion on the product; or overlay the logo in the edit |
| more than three subjects | faces and objects merge | at most three main subjects; one person per clip unless the beat needs two; say the count ("a single woman", "two mugs") |
| "a person" | sometimes renders several | "one woman", "a single man" |
| a face across many clips | identity drifts when location or light changes | one location per clip, the CHARACTER lock in every clip, the same reference image |
| a fast-moving subject | face warp, rubber arms | natural pace; energy from camera and cuts. On Seedance never write "fast" |
| several camera moves in one line | floaty drift, or ignored | one move per clip; split the clip |
| a list of many items or beats | only 4-5 appear; scenes get dropped | 3-5 beats per 10 s; more clips |
| numbers for duration or speed | ignored ("24 seconds" gives 30) | set duration in the tool, not the prompt. A clock time of day helps keep light consistent |
| a strong emotion | overacted, wrong order | an ordered chain plus a stop line: `tears stay in her eyes and never fall, no smiling` |
| an animal, creature or odd object by name | wrong species or shape | describe it part by part, or use a reference image |
| an event ("the door opens") | it barely happens | place + moment + visible result: `at 4s the left door swings fully open` |
| a ban in the positive prompt ("no oil") | often ignored | describe what IS there; put exclusions in the negative field or a final `Avoid:` line |
| style named once in a long prompt | drifts toward photoreal or another style | repeat the STYLE lock in every clip; for animation add `NOT photorealistic` to the negative |
| mood words for a place ("aesthetic", "minimalist vibe") | stock-footage B-roll look | name a concrete ordinary place: "her own small kitchen counter" |
| a pristine gift box centred in frame | instant "ad" signal in UGC | product out of the box, already used; plain packaging off to the side if at all |
| quotes around Veo dialogue | burned-in subtitles | colon form without quotes, plus `no subtitles` |
| contradictory light and weather | muddy, confused frames | agree: not "golden hour" with "heavy downpour" |
| a real person or celebrity named | refusals, lookalikes | invented people only, unless the person has consented |
| a franchise, team or brand named | some models refuse or blur it | keep it if the model accepts; if refused, describe the look and carry the real marks through the photo or keyframe |

## Negative prompt starters

Use where the model has a negative field; otherwise fold the key ones into an
`Avoid:` line.

- **Any:** `blur, distortion, low quality, flicker, watermark, text, subtitles`
- **People:** `distorted face, extra fingers, deformed hands, waxy skin, outfit change, identity change`
- **Product:** `warped product, changed label, distorted logo, extra objects, duplicate product`
- **UGC:** `cinematic grading, ring light, studio lighting, gift box, beauty filter`
- **Animation:** `photorealistic, live action, 3D render` (or the reverse for 3D)

## Quality pass after generation (about ten seconds a clip)

1. **Physics.** Gravity, reflections, shadows match the light, sizes believable,
   liquids behave.
2. **Detail.** Fingers, faces, edges between objects, the product's shape and
   colour, no fake text.
3. **Brand and continuity.** Same outfit, same product, same light and palette
   as the previous clip; would it sit on the user's feed without looking odd.

If a clip fails, change the prompt and regenerate. Do not try to fix a broken
generation in the edit.

## Fixes by symptom

- **Face changed:** shorter, simpler action; character sheet as reference; one
  location; lock pasted word for word.
- **Product looks different:** real product photo as first frame; remove
  re-descriptions of the product in i2v; lower motion (higher cfg on Kling).
- **Colour or light jumps between clips:** last frame of the previous clip as
  the first frame; same time of day; colour-match in the edit.
- **Too glossy for UGC:** add window daylight, no ring light, no color grading,
  real skin texture; drop "cinematic"; ordinary location.
- **Nothing happens:** one stronger, visible action with a time marker; lower
  cfg on Kling; shorter prompt.
- **Lip-sync off:** shorter lines; voiceover instead; a lip-sync tool on that
  clip only.
