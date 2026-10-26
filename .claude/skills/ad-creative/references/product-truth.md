# Mode A — Product Truth and advertiser analysis

The user supplies the product (photo, name, and whatever else they know). You
play the advertiser and fill the gaps with analysis — but you keep three kinds
of statement apart, in `projects/<id>/product.json` (schema:
`schemas/product.schema.json`):

| bucket | what goes in | can it appear in the ad? |
| --- | --- | --- |
| `facts` | seen in the photo (`source: image`) or stated by the user (`source: user`) | yes |
| `inferred` | your marketing judgement: persona, gift occasion, pain, desire, angle, season | yes, as framing ("the gift he'll actually wear") — never as a product fact |
| `unknown` | material, size, weight, price, shipping time, durability, origin, reviews… that nobody stated | **no**. Not in dialogue, not in overlay, not implied |

`claims` lists every product statement the ad will make; each needs
`evidence` = a key in `facts`. A claim without evidence is blocked by
`scripts/validate.py`. Ask the user for the fact, or drop the claim.

Personalization claims ("any name", "any color") need the user to confirm the
shop really offers them — ask once if the listing does not show it.

## The analysis (in brief.md, user's language)

1. **Product card** — what it is, visible details, print/text on it (exact),
   where it lives, 3-second proof. From the photo only (table in
   `product-analysis.md` §1).
2. **Two buyers** — the self-buyer and the gift-buyer (POD is mostly gifts):
   who, for whom, which occasion, what they fear (wrong size, cheap print,
   late delivery) and what they want to feel.
3. **Three angles** — one line each, with the persona it serves. Mark the
   recommended one.
4. **Season and offer** — today's date against occasions (Valentine, Mother's/
   Father's Day, back to school, football season, Halloween, BFCM, Christmas).
   Offers only if the user gives one.
5. **Three hooks** — concrete, visible in frame one. Score them with the user's
   `ig-hooks` rules if available; otherwise pick the one with a visible
   result in the first second.
6. **Assumptions** — every `inferred` item you leaned on, one line each.

Mode A flows straight into mode B (story draft) in the same turn; the stop for
approval comes after the story draft, before any prompt.

## product.json example

```json
{
  "schema_version": "1.0",
  "product_id": "custom-name-hoodie",
  "name": "Custom Name Embroidered Hoodie",
  "model": "pod_custom",
  "reference_images": ["frames/product.jpg"],
  "design_files": ["frames/design.png"],
  "invariants": ["Name embroidered left chest, white thread, script font", "Hoodie colour heather grey"],
  "facts": [
    {"key": "personalization", "value": "Name printed/embroidered to order", "source": "user"},
    {"key": "colors", "value": "Grey, black, navy shown on listing", "source": "user"}
  ],
  "inferred": [
    {"key": "gift_buyer", "value": "Girlfriend buying for boyfriend, anniversary or Christmas"},
    {"key": "pain", "value": "Generic gifts feel thoughtless"}
  ],
  "unknown": ["fabric weight", "price", "shipping time"],
  "claims": [
    {"text": "Any name", "evidence": "personalization"},
    {"text": "Three colours", "evidence": "colors"}
  ]
}
```
