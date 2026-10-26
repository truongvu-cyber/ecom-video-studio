# Deliverables of one run

All files live in `projects/<id>/`. Create the folder with
`refs/ frames/ clips/ edit/ out/`. The user puts the product photo and design
file in `frames/`.

## Step 1 — before approval

**`product.json`** (mode A, see `product-truth.md`) and **`brief.md`**:

```markdown
# <Product> — brief

## Phân tích sản phẩm
<product card, two buyers, three angles (recommended marked), season, hooks, assumptions>

## Video mẫu (only in mode C)
<beat table + notes from reference-video.md>

## Story draft — CHỜ DUYỆT
**Format:** Veo 3 · 9:16 · <N>s · 1 dialogue clip + <n> B-roll · style <#> · genre <#>
**Why this, here, now:** <coherence sentence>

| Shot | Clip | Time | Role | What we see | Spoken (c01) / sound | Overlay |
|---|---|---|---|---|---|---|
| s01 | c01 | 0-2.5s | hook | ... | "..." | ... |

**Chi phí gen:** <k> keyframes + <c> clips × 8s (Veo) · biến thể: <list with cost>
**Hướng khác:** 1) ... 2) ...
```

Stop here and ask for approval (or changes). Nothing below is written before
the user says yes.

## Step 2 — after approval

**`prompts.md`** in the shape of `output-template.md`, with these house changes.

**Language (user's rule):** everything a person reads — title, intro, table,
section headings, "what this shot shows", upload lists, checks, settings — is in
**Vietnamese**; everything pasted into a model — the fenced prompts and the lock
values — stays in **English**. Keep the parser markers: `### Keyframe N`,
`## Clip N · 8s · <tên cảnh tiếng Việt>`, `**Khung đầu:**`,
`**Lưu video thành:** cNN_a.mp4`, `**Phủ định (Negative):**`, lock labels
`**PRODUCT (sản phẩm):**` etc. Add one Vietnamese `**Cảnh:**` line per keyframe
and clip so the user knows what each prompt makes without reading English.
`projects/california-1850-tee/prompts.md` is the reference layout.

- Header table: Tool = Veo 3.1 · image = Nano Banana Pro.
- Locks: PRODUCT, CHARACTER, STYLE, **VOICE** (gender, age, accent, pace,
  energy), AUDIO, NEGATIVE.
- `### Keyframe N` for every clip, `**Save as:** keyframe_cN.png`.
- `## Clip 1 · 8s · Dialogue (A-roll)` with
  `**Generate with:** Veo Ingredients · **First frame:** none, references keyframe_c1.png + product photo + design file`.
  Ingredients has no first frame, so this prompt **does** paste the CHARACTER,
  PRODUCT and STYLE locks (stay under 200 words).
- `## Clip N · 8s · <role>` for B-roll with `**First frame:** keyframe_cN.png`.
- `**Save the video as:** cN_a.mp4` (second try `cN_b.mp4`) — these names are
  what the Editor matches.
- Replace "Voiceover / audio script" and "Edit guide" with one line:
  `Dựng: đưa clip vào projects/<id>/clips/ rồi chạy ad-editor.`

**`production.json`** (schema `schemas/production.schema.json`):

- `stage: "prompts_ready"`, `gen_model: {image: "nano-banana-pro", video: "veo-3"}`
- one shot per row of the story table, in timeline order
- dialogue shots: `file_pattern: "c01*.mp4"`, `audio_type: "dialogue"`,
  `dialogue` = exactly the line written in clip 1's prompt
- B-roll shots: `file_pattern: "cNN*.mp4"`, `audio_type: "sfx"` or
  `"music_only"`, `print_fidelity: "strict"` where the print must be legible
- `overlay` text only from approved claims or framing; `overlay_pos` `top`
  unless the keyframe puts a face or the print there
- `music`: `{"source": "auto", "mood": "...", "bpm_range": [..]}` unless the
  user gives a track

Then run the checks in SKILL.md Stage 6.
