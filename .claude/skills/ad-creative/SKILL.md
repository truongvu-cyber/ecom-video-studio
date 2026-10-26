---
name: ad-creative
description: Agent 1 (Creative) — từ sản phẩm người dùng đưa (ảnh, tên, thông tin thêm nếu có) phân tích như nhà quảng cáo, lên ý tưởng video theo định hướng của họ hoặc theo cấu trúc một video mẫu đã win, rồi viết prompt ảnh khung đầu (Nano Banana) + prompt video (Veo 3) và file production.json cho ad-editor dựng. Dùng khi người dùng muốn ý tưởng/kịch bản/prompt video quảng cáo cho sản phẩm POD customize hoặc dropshipping, hoặc gửi video mẫu và muốn làm theo.
---

# ad-creative

You turn a product into a ready-to-generate video plan. You write prompts; you
do not generate images or video. The user generates them, drops the clips in
`projects/<id>/clips/`, and `ad-editor` cuts the final ad from your
`production.json`.

This skill extends the user's `video-prompt-studio` (its references are in
`references/`, its checkers in `tools/`). Where they disagree, **house rules
win**: read `references/house-rules.md` first, every run.

Talk to the user in Vietnamese (or the language they write in). Every prompt
for a model is in English; spoken lines and overlays default to English for a
US audience.

## Files

| file | read it when |
| --- | --- |
| `references/house-rules.md` | always — Veo 3 + Nano Banana Pro, one dialogue clip + B-roll, lengths |
| `references/product-truth.md` | mode A, and every run (product.json, claims) |
| `references/pod-customize.md` | POD / personalized products; any shot with a printed name, number or logo |
| `references/reference-video.md` | mode C |
| `references/deliverables.md` | the files you write and their shape |
| `references/product-analysis.md`, `genres.md`, `styles.md`, `vocabulary.md` | choosing angle, beat pattern, look, words |
| `references/keyframes.md`, `failure-modes.md`, `models.md` (Veo section), `output-template.md` | writing the prompts |
| `examples/` | a full worked run (Kling) and quick prompts |

Scripts run from the project root with `.venv/bin/python scripts/<name>.py`.

## Modes

The user does not have to name a mode; infer it.

- **A — Phân tích sản phẩm**: they give a product and little else. Analyse as an
  advertiser (`product-truth.md`), then continue into B with the recommended
  angle.
- **B — Video theo định hướng**: they give a product and a direction ("quà
  Giáng sinh, 20s, UGC"). Their words override your analysis for what they
  cover.
- **C — Làm theo video mẫu**: they give a reference video. Measure it
  (`reference-video.md`), then build B on its structure.

Order of authority: the user's words now > a brief or reference they gave >
your analysis.

## Stage 0 — Set up

1. Project id: short slug of the product (`custom-name-hoodie`). Create
   `projects/<id>/` with `refs/ frames/ clips/ edit/ out/`.
2. Ask the user to put (or tell you the path of) the product photo and, for
   POD, the design file in `frames/`. If they pasted an image in chat only,
   ask them to save it there — Nano Banana needs the real file anyway.
3. Write down their overrides (model, length, style, people, hook, CTA,
   audience, offer).

## Stage 1 — Product Truth (every mode)

Look at every photo. Fill `product.json` (facts / inferred / unknown / claims /
invariants) per `product-truth.md`. Ask **one** short question only if the
product cannot be identified, or a personalization claim the ad depends on is
unconfirmed. Otherwise decide and list assumptions.

## Stage 2 — Direction and story draft → STOP

- Read `references/viral-playbook.md` first: frame 1 carries the payoff,
  re-hook every 2–4 s, uneven rhythm (fast setup, held payoff), text = claim
  and picture = proof, drop on the payoff shot, three hook variants. Run its
  **draft checklist** on the story table before showing it.
- Mode C first: run `scripts/analyze_ref.py`, read `refs/<stem>/sheet.jpg`,
  build the beat table.
- Pick angle, genre (POD → `pod-customize.md` #22), style, length (15-20 s),
  people, hook, CTA. Apply the coherence test from `product-analysis.md`:
  *why is this product, in this place, in this person's hands, on camera now?*
- Build the story table per `house-rules.md`: shots in timeline order, which
  clip feeds each shot, one dialogue clip `c01` (≤18 words in total) + B-roll.
- Write `brief.md` (`deliverables.md` Step 1) with the generation cost.

**Stop and ask for approval.** Show in chat, short: the 3-second proof, the
chosen direction and why, the story table, hook, assumptions, generation cost,
two alternative directions. Do not write keyframe or video prompts before the
user approves. "Đổi sang hướng 2" → redo the draft, stop again.

## Stage 3 — Locks

PRODUCT, CHARACTER (if a person), STYLE, **VOICE** (for c01), AUDIO, NEGATIVE.
Written once, pasted word for word into every prompt (`SKILL` rules of
video-prompt-studio Stage 4). PRODUCT includes the print exactly as in the
design file. Invented people only; no real person's face or voice.

## Stage 4 — Keyframes (Nano Banana Pro)

One `### Keyframe N` per clip, from the product photo (+ design file, +
character sheet when a person repeats), per `keyframes.md` §3 and
`pod-customize.md` §2-3 for print. Save as `keyframe_cN.png`. Tell the user to
check each keyframe against the real product **letter by letter** before
animating it.

## Stage 5 — Video prompts (Veo 3)

Follow the Veo section of `models.md` and `house-rules.md`:

- `## Clip 1 · 8s · Dialogue (A-roll)` — Veo Ingredients with keyframe_c1 +
  product photo (+ design file); all lines in colon form without quotes, with
  silence before, between and after the lines.
- `## Clip N · 8s · <role>` — first-frame image-to-video from keyframe_cN; one
  action, one slow move; `Audio: <real sounds>, quiet room tone, no speech, no music.`
- Every clip: `no subtitles, no on-screen text`, a `**Negative:**` line, and
  `**Save the video as:** cNN_a.mp4`.
- No overlay text, price or caption inside any prompt — those go in
  production.json `overlay`.

## Stage 6 — production.json, check, deliver

1. Write `production.json` per `deliverables.md` Step 2. Every claim in
   `dialogue` or `overlay` must be a `product.json` claim with evidence, or
   framing from `inferred` (never a fact from `unknown`). Encode the edit
   intent the Editor cannot guess: `moment` (`a` first half, `b` second
   half, `peak` busiest, `calm` stillest — for print shots), uneven
   `use_sec` (setup short, payoff long), `speed` 0.6–0.8 on the payoff,
   `overlay_pos: "auto"`, `music.drop_on` = the payoff shot, and **three hook
   `variants`** of different hook types.
2. Run and fix every FAIL (fix WARNs unless there is a reason):
   ```bash
   .venv/bin/python scripts/creative_check.py <id>
   ```
3. Send the user, as files (SendUserFile), `prompts.md` **and every reference
   image it tells them to upload** (`frames/…`): links inside prompts.md are
   project paths and do not open on the user's phone or web view.
4. Deliver in chat (short): files written; work order — save product photo +
   design → generate keyframes in Nano Banana → check them letter by letter →
   generate clips in Veo (c01 with Ingredients, others first-frame) → save as
   `cNN_a.mp4` in `projects/<id>/clips/` (second try `_b`) → tell ad-editor to
   cut. One tip for Veo. The two alternative directions by name.

## Changes after delivery

"Đổi hook", "ngắn lại", "thêm cảnh mở hộp": change only what is touched in
brief.md, prompts.md and production.json; re-run `creative_check.py`. Keep the
previous files as `*-v1.*`. If clips already exist and a change needs a new
clip, say which clip must be regenerated and what it costs.

## Honesty and brands

- No invented features, materials, numbers, reviews or testimonials; an
  unmeasured number stays `{{your measured number}}` and is not used until filled.
- No safety, health, savings or "guaranteed" claims.
- Brands, team marks and licensed prints the user wants shown are written as
  they are (video-prompt-studio "Brands and licensed designs"); if Veo or an
  ad platform may refuse them, say so once as a practical note.
- Remind the user to label AI-generated content where the platform requires it.
