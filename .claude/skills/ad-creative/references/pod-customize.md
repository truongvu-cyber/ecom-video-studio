# POD customize playbook (#22) and print fidelity

For print-on-demand and personalized products (name, number, photo, date on a
shirt, hoodie, jersey, mug, blanket, ornament, tumbler). The sale is the
personalization, so the video must show **their name on a real-looking
product**, sharply, at least once.

## 1. Beat pattern (15-20 s)

| beat | clip | purpose | example |
| --- | --- | --- | --- |
| Hook 0-2.5 s | c01 (dialogue) | surprise or desire in frame one | "Wait, you can put his name on it?" holding the product |
| Personalize 2.5-6 s | B-roll | the name appears / is chosen | hand types a name on a phone, cut to the product with that name, slow push in |
| Proof 6-9 s | B-roll | quality you can see | macro of the print/embroidery, fingers brushing it, even light |
| Feeling 9-12 s | B-roll | the moment it is for | gift opened, partner reads the name and smiles; or worn on a cozy evening |
| Line 2 | c01 (dialogue) | the offer in plain words | "Any name, any color." |
| CTA last 2.5-3 s | c01 (dialogue) + overlay | tell them where | "The link is right below." + overlay "Personalize yours ↓" |

Unboxing variant: replace Proof with a gift box opening that reveals the name.
Sports variant (jersey with name + number): Personalize beat = the back of the
jersey turned to camera, name and number filling a third of the frame.

## 2. Print fidelity rules (shots marked `print_fidelity: strict`)

Video models redraw small text. These rules keep the print readable:

1. **The print comes from the keyframe, never from the video prompt.** The
   keyframe is made in Nano Banana from the product photo **plus the design
   file** (PNG/SVG of the name or artwork): `Image 2 is the exact artwork
   printed on the chest; reproduce its letters, font, colour and placement
   exactly; do not retype or restyle the text.`
2. Check the keyframe letter by letter. If Nano Banana gets the name wrong,
   fix the keyframe (regenerate or correct it in Photoshop) **before** Veo.
3. Camera: straight-on or within ~15°, `static` or `slow push in`. No orbit
   past 15°, no product rotation, no fast handheld.
4. The printed area is flat and facing the lens: no fabric folds across the
   letters, no hand covering them, no strong glare.
5. Even, soft light; the print fills at least a quarter of the frame width.
6. Keep the motion small and around the print (a hand settling the fabric,
   steam rising from a mug) so the letters stay still.
7. In `production.json` give these shots `print_fidelity: "strict"`; the
   Editor sends a frame of each for a human check against the design file.

## 3. Flat mockup -> worn / in-use keyframe

When the user only has a flat mockup (shirt on white), the first keyframe
turns it into a scene while keeping the print:

```
Image 1 is the product mockup: <PRODUCT lock>. Image 2 is the exact artwork printed
on it. Keep the garment's colour, cut and the print exactly as in images 1 and 2:
same letters, font, size, colour and placement on the chest; do not retype,
restyle or move the print.
<CHARACTER lock> wears it, standing in <place>, <light>, chest facing the camera,
fabric smooth across the print, arms relaxed at the sides.
Phone photo, natural skin texture, real fabric folds away from the print.
Medium shot from chest up, vertical 9:16, print in the centre third, top 15% and
bottom 20% kept clear. One person, one garment, no extra text, no watermark,
natural hands with five fingers.
```

## 4. Name variants cost credits

Each different name **on the product** needs its own keyframe and its own
B-roll clips (the dialogue clip can be reused if the name is not spoken). Cheap
variants (no new generation): hook overlay, CTA text, music, shot order. In the
brief, list the variants with their cost: "3 names = 3 keyframes + 6 clips".
