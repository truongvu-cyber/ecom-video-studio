# Product analysis and auto-direction

How to read a product from its photo and name, and how to pick the video
direction when the user has not asked for one. Defaults assume a US audience on
Reels / TikTok / Shorts. Whatever the user states explicitly overrides the
matching row here; everything else still comes from this file.

## 1. Product card (fill from the photo + name, nothing invented)

| field | how to fill it |
| --- | --- |
| What it is | category and job in plain words ("12V heated car blanket") |
| Visible details | shape, colour, material, finish, parts, the one distinctive detail; only what the photo shows |
| Size cue | relative to a hand, a mug, a phone; say "unclear" if the photo has no scale |
| Text and logos on it | list them; keep them as on the photo (they come through the first frame best; small lettering drifts in video) |
| Where it lives | the ordinary place it is used: nightstand, car console, kitchen counter, desk, bathroom shelf, backpack |
| Who buys it (US) | one persona + one gift persona if it gifts well |
| The 3-second proof | the single visible moment that shows it works (wax turns glossy, ice slides off, steam rises, light fills the ceiling) |
| Season fit | today's date against the product: winter, holiday gift, back to school, summer, evergreen |
| Claims to avoid | safety, health, savings, "best", numbers the user has not measured |
| Photo as first frame | usable or not: ratio (Kling i2v inherits the photo ratio, so 9:16 is needed), clean background, angle, light. If not usable, write a reference-image prompt in Step 0 |

If the photo and the name disagree, or the product's use is not clear, ask one
question before going on. Otherwise do not ask; decide.

## 2. Pick the angle

Pick the first row that fits. The angle decides the story shape.

| the product... | angle | genre playbook | default style |
| --- | --- | --- | --- |
| fixes a visible, everyday annoyance (ice, cold coffee, mess, draft, tangled cables) | Problem -> solution demo | #3 | #2 UGC phone, or #8 bright lifestyle |
| makes a satisfying process (melting, pouring, glowing, clicking, foaming) | Satisfying / ASMR | #5 | #5 tabletop or #6 cozy |
| changes a room's mood (lights, projectors, candles, diffusers, decor) | Mood transformation: before dark/dull -> after glowing | #3 with mood shots | #6 cozy hygge or #10 neon night |
| is mostly bought as a gift (gadgets, cozy items, novelty) and the date is Oct-Dec | Gift angle: "the gift for the person who has everything" | #7 | #7 festive or #2 UGC |
| is personal care, beauty, wearable | UGC review / try-on | #1 or #19 | #2 UGC phone |
| is kitchen, food or drink | Food money shot + use | #18 / #5 | #5 tabletop or #6 cozy |
| is premium or design-led (jewellery, watches, high-end tech) | Hero product film | #6 | #4 luxury or #21 CGI |
| solves something in the car | In-car problem -> solution | #3 | #2 UGC phone (driver's seat) |
| is for pets or kids | Lifestyle moment with the reaction | #9 | #8 bright lifestyle |
| is tech or a tool that needs explaining | Explainer, step per clip | #16 | #22 motion graphics or #8 |
| none of the above | UGC review | #1 | #2 UGC phone |

Season can shift the style, not the angle: in Nov-Dec a winter or cozy product
gets style #6 or #7; gift-heavy products add one gift line to the script.

## 3. Defaults for the rest

| setting | default | change when |
| --- | --- | --- |
| model | Kling 3.0 image-to-video from the product photo | user names a tool; dialogue is the point -> Veo with reference images |
| ratio | 9:16 | user asks for feed (4:5) or YouTube (16:9) |
| length | 15-20 s, 4-5 clips | gift guides and explainers 25-30 s; ASMR 8-12 s |
| people | hands only, or one person seen partly | the angle needs a reaction or a review face |
| audio | voiceover + on-screen text in the edit; native audio only for one short line | user wants talking UGC or music only |
| language | English prompts; English VO and on-screen text for the US | user names another audience |
| hook | write 3, pick the most concrete one; product working or problem visible in frame one | user gives a hook |
| CTA | "Comment [WORD] for the link" or "Link in bio" | user gives an offer or shop CTA |

## 4. What to show the user before the prompts

Five lines at most, in the user's language:

1. What the product is and the 3-second proof you will build on.
2. Chosen direction: angle, style, model, length, and why in one clause.
3. The hook (and the two you did not pick, short).
4. Anything you could not see or had to assume (size, colour of the back, features).
5. Two alternative directions in one line each, so the user can say "đổi sang hướng 2".

Then write the prompts in the same turn. Do not wait for approval unless the
user asked to see the plan first, or an override contradicts the product (an
ASMR video for a product with no satisfying process): then say so and ask.
