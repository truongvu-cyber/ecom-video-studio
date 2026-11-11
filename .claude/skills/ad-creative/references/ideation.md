# Ideation — ten ideas before one direction (user request 2026-11-10)

A first idea is usually the one everybody has. The story draft is written only after a wide
pass: ten ideas from different families, cut down by fixed tests, scored, and the user picks.
Output: `projects/<id>/ideas.md`. This step comes after Product Truth and before the format.

## 1. Read first (every time)

```bash
.venv/bin/python scripts/taste.py show      # what the user approved, rejected and asked to change, in their words
.venv/bin/python scripts/styles.py list     # edit recipes we already have, with their verdicts
```

Plus `product.json` (`key_trigger`, facts, claims, unknown) and the `brief.md` of the last
five projects in `projects/` (to know what has been done).

## 2. Ten ideas, at least six families

One line per idea. Each idea names what the viewer sees in the first second and what
changes in the middle (the turn); an idea with no turn is a product shot, not an idea.

| family | the idea is built on | example for a door logo light |
| --- | --- | --- |
| **moment** | a real occasion when the product matters | tailgate night: every door in the row opens |
| **tribe** | who the buyer is and who they are not | "Dallas trucks only" — a rival fan's door stays dark |
| **gift** | the giver and the receiver's reaction | he opens the truck on his birthday and stops |
| **comparison** | this against the ordinary thing | regular door / my door |
| **expectation** | looks like nothing, turns into something | "it's just a door light" |
| **transform** | one action that changes the product's state | the zip that closes the star |
| **how** | the making, the install, the trick shown | 60-second install against a stopwatch |
| **social** | a comment, a question, a reaction, a dare | reply to "do u have the Cowboys??" |
| **borrowed** | a format from a reference or a trend, refilled | the cut and sound of a reference the user sent |
| **story** | a tiny narrative with a character who wants something | she borrows his truck and finds out he is a fan |
| **sense** | sound, texture, close detail, no words | the click, the glow on wet asphalt, nothing else |

Write each as:
`N · family · frame 1: … · turn: … · style: <recipe name or "mới"> · why this product: …`

## 3. Cut (an idea that fails any test is struck through, with the test named)

1. **Trigger:** frame 1 shows `key_trigger`, or hides it on purpose and says how (user rule 2026-10-27).
2. **Only this product:** swap in another product and the idea still works unchanged → it is generic, cut it.
3. **Truth:** it needs a claim that is not in `product.json.claims`, or shows the product doing what it cannot (three logos in a row from one door) → cut.
4. **Done already:** the same family *and* the same turn as one of the last five projects → cut, unless the user asked for a series.
5. **Taste:** it repeats something the taste log shows the user rejected → cut.

## 4. Score what is left (1–5 each, one honest line of reasoning)

| score | question |
| --- | --- |
| stop | would frame 1 stop a thumb with the sound off? |
| proof | does the picture itself prove the claim? |
| make | can it be made with 4–6 clips of 8 s, no person-through-object risk, no unreadable print? |
| new | how different is it from our last five and from the references we copied? |
| taste | how well does it match what the taste log says the user likes? |

## 5. Show the user and stop

In chat: the five best as a table (idea in one line, family, the five scores, total), your pick
and the reason in one sentence, and the ideas you cut with the test that cut them (one line
each). Ask them to choose up to three. The story draft (Stage 2) is written for the idea they
choose; the others stay in `ideas.md` for later videos of the same product.

When the user gives the direction themselves ("làm dạng bấm giờ", a reference video), the wide
pass is skipped: write `ideas.md` with that one idea and the line `direction given by the user`.
