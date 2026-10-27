# Formats — the fixed presets every project is built from

A project is one of four formats. The format decides the clip design, the
shot lengths, the edit settings and the music search; the creative work is
choosing the format and writing what happens inside it. Put the choice in
`production.json` as `format` so `creative_check.py` can verify the rest.

## 1. Choosing the format

| the product / direction | format |
| --- | --- |
| user asks for talking, review, "UGC", or the hook is a spoken line | `ugc_dialogue` |
| user asks for hype, rap, "gang gang", fast cuts, streetwear / sports flex | `hype_montage` |
| user asks for chill, aesthetic, lo-fi, calm, gift mood, no talking | `calm_lofi` |
| product needs an install / use / how-to shown (gadgets, tools, kits) | `demo_steps` |

Default when the user gives no direction: products with a visible trick →
`demo_steps`; apparel and gifts → `ugc_dialogue`.

Projects made before the presets existed (Milwaukee jersey) carry no
`format`; `creative_check` reports that instead of guessing one. Every new
project must have one.

## 1b. Generation tools (user rule, 2026-10-27)

Images: **Nano Banana 2.1** in Flow. Clips: **Omni 1.1 Flash**, mode
**Thành phần** (ingredients: keyframe + product photo + design file), 8 s,
9:16, downloaded at 1080p. Prompts keep the Veo-style structure from
`models.md` (subject → action → camera → light → audio, colon-form dialogue,
"no subtitles"); only the tool changes. `references/flow-runbook.md` has the
click-by-click procedure.

## 2. The presets

| setting | `ugc_dialogue` | `hype_montage` | `calm_lofi` | `demo_steps` |
| --- | --- | --- | --- | --- |
| clips | 1 dialogue clip + 3–4 B-roll | 4 B-roll | 4 B-roll | 4 B-roll |
| clip design | B-roll: one action, one slow move | **two actions per clip** (0–4 s / 4–8 s), camera settles between them | one slow action per clip | two actions per clip (two steps, or step + result) |
| shots | 5–7 | 8 | 4–6 | 8 |
| total | 15–20 s | 13–16 s | 14–16 s | 13–16 s |
| `use_sec` | dialogue: words ÷ 2.5 + 0.5; B-roll 2–4 | 1.2–2.2; payoff 2–2.5 | 3–4 | steps 1.2–1.6; reveal 2–2.5 |
| `moment` | B-roll `peak`, print `calm` | `a` / `b` by half; payoff `peak`; print `calm` | `calm` for print, `peak` otherwise | `a` / `b` by half |
| `speed` | 1.0 | payoff 0.6–0.8 | 1.0 | reveal 0.75, steps 1.0–1.2 |
| `audio.keep_native` | true | false | true (ambience under the music) | false (true only if the user wants the real sounds) |
| `captions` | on, `word-highlight` | off | off | off |
| `text_style` | `pill` | `bold` | `pill` | `bold` |
| `fx` | none | `hype`, intensity 0.8–1.0, sfx on | none | `hype`, intensity 0.6–0.8, sfx on |
| overlays | hook + CTA only | one slam per shot, ≤ 4 words | hook, one mid-video line, CTA | numbered steps + reveal lines |
| `music.mood` | by vibe: "warm upbeat hip hop" / "chill lofi" | "hard trap drill" or "ny drill rap" or "hype sports anthem" | "chill lofi indie" (+ scene word: surf, cozy) | "upbeat bouncy hip hop" |
| `music.bpm_range` | 85–120 | 85–160 | 75–95 | 85–110 |
| `music.drop_on` | payoff shot (or CTA) | payoff shot | `none` or payoff | the reveal shot |
| `overlay_pos` | `auto` | `auto` | `auto` | `auto` |
| `variants` | 3 hooks (overlay + first spoken line variants in prompts) | 3 hook slams | 3 hook lines | 3 hook slams |

## 3. Colour rule (text accent)

`text_style.color` = the product's signature colour, read from
`product.json` invariants: the print or lettering colour on apparel (gold on
the Milwaukee and NYK jerseys), the logo's dominant colour on a projector or
badge (Cubs red), the brand colour when there is one. Fallback:
`brand/brand.json` accent. The highlighted `*word*` is always white (ink).
Never pick a colour that is not already on screen.

## 4. Character rule

- The character is the inferred buyer from `product.json` (`self_buyer` for
  flex/lifestyle angles, the gift *recipient* for gift angles), described as
  an ordinary person.
- Never someone who could pass for a real athlete, celebrity or the person a
  name on the product refers to (different sex, age or build, everyday
  clothes). This is what got the first NYK clip refused.
- One recurring character per video (plus out-of-focus friends at most).
  Hands-only shots need no character lock.
- Name the character in the lock (`CHARACTER - Maya`) so prompts refer to
  "the woman", never to the name.

## 4b. World rule — the person and the place belong to the product (user rule 2026-10-27)

A product that carries a team, a brand or a fandom (a Dodgers door light, a
Cubs jersey, a Swiftie tote) is sold to a fan. The fan and their surroundings
must look like it, or the product floats in a generic world.

- `product.json` gets `world`: `{"name": "Dodgers", "cues": ["Dodger blue cap",
  "white jersey with blue script", "blue-and-white pennant on the wall",
  "stadium parking lot at dusk"]}` — at least two visual cues, written as
  things a camera can see (colours, garments, objects, places), never the
  team name inside a model prompt when the name itself would be refused
  (then describe the colours and shapes only).
- The **CHARACTER lock** uses at least one cue on the person (cap, jersey,
  hoodie, scarf, wristband, colours).
- Every **STYLE lock** (one per setting) uses at least one cue in the setting
  (a pennant, a poster, a flag on the garage wall, a car in the team colour,
  a game-day crowd far behind) — a small, out-of-focus one is enough.
- `creative_check.py` FAILs a project with `world` whose CHARACTER or STYLE
  locks contain none of the cues. Hands-only shots keep the sleeve or
  wristband cue.
- The product's own print is still the only legible text/logo in frame; cues
  are colours and shapes, never a second readable logo next to the product.

## 5. Music keyword rule

`music.mood` is a search string as well as a label. Build it as
`<energy> <genre> [<scene>]` from the preset row, e.g. "hard trap drill",
"chill lofi indie surf", "upbeat bouncy hip hop". Do not reuse the exact
string of an earlier project if a different track is wanted: the library
picker matches on these words first.

## 6. File naming

| thing | name |
| --- | --- |
| project | `projects/<product-slug>/` (lowercase, hyphens) |
| product images | `frames/product.<ext>`, `frames/design.png`, extra views `frames/product_<view>.<ext>` |
| character sheet | `frames/<name>_sheet.png` |
| keyframes | `frames/keyframe_cN.png` |
| clips | `clips/cNN_a.mp4`, retries `_b`, `_c` |
| outputs | `out/final_<id>.mp4`, `out/final_<id>_<variant>.mp4`, `out/preview_<id>.mp4` |
| previous renders | `out/v1/`, `out/v2/` … (the Editor moves them automatically) |

## 7. What stays creative

Within the preset, the agent still decides: the angle and hook type, what
each half of each clip shows, the exact words, the order of shots, which
shot is the payoff, which three hooks to test. Those decisions are judged by
`viral-playbook.md`'s checklist, and the checklist result goes into
`brief.md` so the user can see why.
