# Mode C — follow a winning reference video

Copy the **structure**, not the content: number of beats, beat lengths, cut
rhythm, hook type, camera language, where the offer and CTA land. Never reuse
the reference's footage, music, captions, voice or exact wording, and never
recreate a real person from it.

## 1. Get the reference into the project

The user downloads the video and puts it in `projects/<id>/refs/`. Do not
download from TikTok/Instagram yourself.

## 2. Measure it

```bash
.venv/bin/python scripts/analyze_ref.py <project-id> refs/<file>.mp4
```

Writes `refs/<stem>/analysis.json` (scene cuts with start/end, words with
timestamps, cuts per second, speech share, music BPM if any) and
`refs/<stem>/sheet.jpg` (one frame per scene, labelled with time). Read the
sheet image yourself. For anything the frames do not answer (what happens
inside a long scene, tone of voice), use `/watch` on the file in **local**
mode.

## 3. Beat table (put it in brief.md)

| # | time | length | beat role | shot (size, angle, move) | what happens | spoken / on-screen | sound |
| --- | --- | --- | --- | --- | --- | --- | --- |

Roles: hook, problem, demo, personalize, proof, lifestyle, offer, cta.
Then one line each: hook type (question, reveal, reaction, result-first),
pacing (average shot length), where the product first appears, CTA wording
style.

## 4. Map to the user's product

- Keep: beat count (±1), each beat's length (±0.5 s), the hook type, the order
  of roles, the camera language, the CTA position.
- Replace: product, person, place, every line (rewritten for the user's
  product, within `product.json` claims), overlays.
- Fit to the house rules: the reference's spoken lines all go into the single
  dialogue clip `c01` (≤18 words); its other shots become B-roll clips. If the
  reference has more talking than fits, keep the hook line and the CTA line,
  and turn the rest into overlay text.
- Note in brief.md what could not be matched (e.g. the reference uses 12 fast
  cuts; we use 7 because each needs its own Veo clip).
