# Model photos — building a person who looks photographed (user request 2026-10-27)

Read this whenever a project invents a person: the character sheet (`Bước 0`), and every
keyframe in which that person is the subject. It turns a person into a **model card**
(identity, fixed for the project) plus **looks** (one per photo), and
`scripts/model_prompt.py` assembles the prompts from the card in a fixed slot order, so no
prompt is written free-hand.

Source: ten prompts from a Vietnamese "AI model photo" page the user shared (selfies,
flash portraits, low-angle close-ups, "Korean Romantic" studio portrait). What follows is
what they do well, mapped to our tools and rules.

## 1. What makes those prompts work

1. **Medium first.** Every prompt opens with the format and the claim that it is a real
   phone photo: "A vertical 9:16 outdoor selfie of an adult woman; photorealistic quality
   resembling a genuine smartphone shot." The model decides *photo vs render* from the
   first sentence.
2. **A fixed order, head to background.** Skin → face shape → brows → eyes (+ where they
   look) → lashes → nose (+ highlight) → lips (+ expression) → hair → accessories → outfit →
   pose → camera → light → background → quality. The same order every time means nothing
   is forgotten and two looks of one person can be compared line by line.
3. **Ranges and positions, not adjectives.** "hair ranging from medium to dark brown",
   "face in the mid-right area", "bougainvillea draping from the upper-left", "arm visible
   in the bottom-right". A position in the frame is worth more than "beautiful".
4. **Realism is balanced, never 'flawless'.** "smooth yet realistic skin texture",
   "visible natural pores", "natural oil shine", "no beauty filter, realistic
   imperfections". Smoothness is allowed only next to a texture word.
5. **Light = source + direction + effect.** "bright warm midday sunlight creating
   highlights on the face, nose, hair and clothing, with soft shadows"; "harsh camera
   flash… against a very dark environment"; "warm street lamp in the left background
   creating a golden rim-light on her flyaway hairs". Never just "good lighting".
6. **The camera is a person holding a phone.** Device, distance, height and tilt, framing
   from–to, where the face sits, lens behaviour: "camera held very close at slightly below
   eye level, subtle wide-angle distortion, framed from the top of the head to the waist,
   face in the upper-right".
7. **Background as an inventory.** Three to five concrete things with places ("white
   cabana with sheer curtains on both sides, resort furniture in the distance, vivid blue
   sky"), not "a nice resort".
8. **Imperfections chosen per look.** Night flash → "heavy grain, slight motion blur";
   daylight selfie → "slight wide-angle distortion, natural imperfections". The
   imperfection sells the photo.
9. **One focal point.** "Sharp focus on the nose bridge and tip", "face and sunglasses
   the focal point". The model spends detail where it is told to.
10. **Looks have names.** "Soft Smile - see-through bangs + oversized white tee", "Sleepy
    Pout - hair pulled back + white tank top": *expression - hair + outfit*. One face, a
    series of named looks.
11. **Identity is locked to a reference.** "Preserve her exact facial identity… Do not
    change her face." The look changes; the face never does.

## 2. What we do NOT copy

- **Length.** Theirs run 300–450 words. Nano Banana 2.1 in Flow follows 40–260 words best
  (`prompt_lint` warns above 260, fails near 400). Every slot is one short clause.
- **"99.99 % precision, no elements added or omitted".** That clause is for re-creating an
  existing photo; we invent people, so it only wastes words.
- **A real person's face as reference.** Our identity reference is always the project's own
  generated `frames/<name>_sheet.png` (formats.md §4: a new person every project, never
  someone who could pass for a real athlete or celebrity).
- **Revealing or sensual wording** ("naturally sensual", "exposing… upper chest", "low
  neckline", "seductive"): Flow refuses or the ad gets flagged. "glam, confident, fitted"
  is the ceiling (Uecker project). `model_prompt.py` fails these words.
- **One beauty ideal.** Porcelain skin, contact lenses and "Douyin" makeup are one market's
  taste. The card follows the buyer persona in `product.json` (age, region, style).
- **Studio 85 mm portraits for UGC.** The camera follows the format: phone selfie / handheld
  for ugc and trends, tripod or gimbal only where the format says so.

## 3. The model card (`projects/<id>/cast/<name>.json`)

```json
{
  "name": "Kayla",
  "identity": {
    "subject": "American woman in her mid-20s",
    "build": "slim build",
    "skin": "light skin with a few freckles, natural texture with visible pores",
    "face": "soft oval face, straight natural brows",
    "eyes": "hazel almond-shaped eyes",
    "hair": "long straight brown hair, centre part",
    "marks": "",
    "accessories": "small silver hoop earrings",
    "fan_item": "royal-blue baseball cap with white interlocking letters L and A on the front",
    "outfit": "oversized royal-blue hoodie with the word Dodgers in white script across the chest, black biker shorts, white sneakers"
  },
  "looks": [
    {
      "id": "selfie-blue-hour",
      "title": "Sly Smile - hair down + Dodgers hoodie",
      "shot": "front-camera selfie held at arm's length",
      "setting": "outdoor, parking lot beside the stadium just after sunset",
      "expression": "sly closed-lip half smile, eyes on the lens",
      "makeup": "",
      "hair_style": "",
      "outfit": "",
      "pose": "body angled slightly, head tilted right, selfie arm visible in the bottom-left",
      "camera": "phone at face height, slightly above, framed from the top of the head to the waist, face in the upper-middle third, slight wide-angle distortion",
      "light": "last orange glow of sunset from behind her left shoulder making a soft rim on her hair, face lit by cool blue-hour skylight",
      "background": "black coupe a few metres behind, palm trees silhouetted on the horizon, stadium floodlights far away",
      "focus": "sharp focus on her eyes and the cap",
      "quality": "slight grain, natural imperfections, no beauty filter"
    }
  ]
}
```

- **identity** is the person, fixed for the whole project. `fan_item` is
  `product.json.world.cues[0]` **verbatim** (formats.md §4b); `outfit` is what they wear by
  default. These fields also produce the CHARACTER lock and the sheet.
- **looks** are photos of that person. Empty `makeup` / `hair_style` / `outfit` mean "as in
  the identity". `title` follows *expression - hair + outfit*.
- Every look slot is **one clause** with a position, direction or range where it can have
  one (§1.3).

## 4. Banks (pick, then make concrete)

| slot | options seen working |
| --- | --- |
| shot | front-camera selfie at arm's length · handheld phone by a friend · phone on a tripod at chest height · mirror-free (never a mirror selfie when there is print: text flips) |
| camera angle | slightly elevated side angle · eye level · extreme low angle pointing up, subject looking down into the lens · high angle looking down |
| framing | top of the head to the waist · to the chest · to the thighs · close-up from the upper chest up |
| face placement | mid-right · upper-right · centred · upper-middle third (keep top 15 % / bottom 20 % for text) |
| expression | wide smile showing teeth · soft closed-lip smile · playful pout · sleepy pout, eyes slightly upward · wink · calm dreamy downward gaze · raised eyebrows, amazed |
| light | midday sun from above-right, highlights on nose and hair, soft shadows · direct phone flash in a dark place, high contrast, grain · warm overhead indoor light, pale beige ceiling · warm street lamp behind-left, golden rim on flyaways · large softbox front-left + soft fill (studio only) · blue hour, cool skylight + orange horizon |
| imperfections | slight wide-angle distortion · light grain · heavy grain + slight motion blur (night flash) · natural skin shine on forehead and nose · flyaway strands |
| focus | eyes · nose bridge and tip · the product on the body (cap, jersey patch) · hands holding the product |

## 5. Assembly (what `model_prompt.py` writes)

Look prompt (one paragraph, slot order fixed):

```
<Medium>: Photorealistic vertical 9:16 <shot>, <setting>, a genuine smartphone photo.
<Identity ref>: Image <n> is <name>: keep the exact face, skin tone and proportions; do not change the face.
<Person>: <subject>, <build>, <skin>, <face>, <eyes>, <hair or hair_style>, <marks>, <accessories>, <fan_item>, <outfit>.
<Expression + pose>: <expression>; <pose>.
<Camera>: <camera>.
<Light>: <light>.
<Background>: <background>.
<Focus + quality>: <focus>; <quality>; real skin texture with visible pores, no beauty filter. No text, no watermark.
```

Sheet prompt (`Bước 0`, identity only, studio): the existing photo-sheet form (formats.md
§4) filled from `identity` — three full-body views + one chest-up close-up, plain grey
background, "no illustration, not a cartoon, no 3D render, no CGI".

When the person is in a **keyframe**, the keyframe keeps its own scene sentence, the
REALISM lock and the STYLE lock (keyframes.md); the look supplies only the person lines
(expression + pose, camera, light, focus) so the two never contradict.

## 6. Checks (script + review)

`model_prompt.py` fails a card when: a required slot is empty; `fan_item` is not
`world.cues[0]` verbatim; a look prompt is over 380 words (warns over 260); a banned word
appears (sensual, seductive, sexy, lingerie, cleavage, exposing, revealing, naked,
flawless; colour words like "nude-pink lips" are fine). Review the image with the card
open: face = sheet, expression and gaze as written, light from the named side, every named
background item present, nothing added in the focus area.
