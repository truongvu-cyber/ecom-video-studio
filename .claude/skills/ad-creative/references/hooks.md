# Hooks — the key selling trigger and the first 2 seconds (user rule 2026-10-27)

Read this in Stage 1 (Product Truth) and Stage 2 (story draft). It is a rule file:
every project writes `product.json.key_trigger` first and builds the hook on it;
`creative_check.py` fails a project without it.

## 1. Why the hook is the whole ad

- On Meta the median **hook rate** (3-second plays ÷ impressions) across 479 video ads /
  $10.1M spend was ~21%; the top 10% were ≥45%. Median **hold rate** (ThruPlay ÷
  impressions) 4.6%. On TikTok the hook window is **2 s**, healthy 30%+, elite 40%+.
  (Biddyco 2026, Billo H1 2026, Sepia Lab / Skaler / Spark UGC benchmark pages.)
- Translation: **4 of 5 viewers are gone before second 3**. Whatever is not in frame 1 and
  the first cut does not exist for most of the audience. A sharp drop in the first seconds
  is a *hook* problem; a slow slide through the middle is a *retention* problem (Outlier
  Kit) — the Editor's re-hooks fix the second, only the story draft fixes the first.
- Motion's 2026 benchmark (~550k Meta ads, ~6k advertisers) ranks hook tactics by hit
  rate: the two winning clusters are **promotional / concrete** (newness, sale, price
  anchor, urgency — bottom of funnel) and **pattern-interrupt** (confession, bold claim,
  contrast, curiosity, warning — top of funnel). Nobody can predict the winner per product,
  which is why every project ships **3 hook variants of different types** (viral-playbook §10).
- Harmon Brothers (Squatty Potty, Purple): start by living with the product until the one
  demonstrable thing is found, then build a **repeatable test / demonstration** (the raw
  egg test, the suds test) and wrap it in humour. The demo is the hook; the joke is the
  wrapper. Hormozi: a hook is **call-out (who) + result + speed/ease + objection removed**;
  his value equation (dream outcome × likelihood ÷ time × effort) is what the first line
  has to signal. MrBeast: the first sentence and first shot **match the promise** of the
  title/thumbnail, then contrast and cuts every few seconds keep the curve flat.

## 2. The key selling trigger (`product.json.key_trigger`) — find it before anything else

The key trigger is the **one visible thing that makes this product worth money** — the
moment a buyer would screenshot. Not a feature list; one thing a camera can show in ≤3 s.

| product | key trigger (`what`) | 3-second proof (`proof_in_3s`) |
| --- | --- | --- |
| car door projector light | the logo appearing on the ground when the door opens | dark ground → door opens → logo blooms |
| World Series jersey | the season patches + the player name/number | macro on the patch; the back CONTRERAS 24 lifted out of the box |
| custom name hoodie | *your* name embroidered on it | the name being read on the chest |
| California tee | the print (place + year) | the print filling the frame on a body |
| mug with a photo | the photo on the mug | pouring reveals the photo |

How to find it (write the answers in `brief.md`):

1. **What did the buyer type to find this?** (jersey: "Contreras World Series jersey" — the
   patch and the name, not "blue shirt".) The search term names the trigger.
2. **What is in the product photo that a generic version lacks?** That delta is the trigger.
3. **What happens / changes when it is used?** (light turns on, name appears, lid opens.) If
   something *changes*, the change is the trigger and the hook is the change happening.
4. **What would the buyer show a friend first?** They point at the trigger.
5. **Which claim in `product.json.claims` has evidence?** The trigger must be provable on
   camera from the photo or the listing; "soft fabric" is not a trigger, "the patch" is.

`key_trigger` fields:

```json
"key_trigger": {
  "what": "the 2026 World Series and NL Champions patches and the CONTRERAS 24 lettering",
  "proof_in_3s": "the jersey lifted out of the box back-first so CONTRERAS 24 fills the frame, then a macro on the patch",
  "hook_types": ["result_first", "pov", "contrast"]
}
```

### 2b. Shot 1 is the trigger, not the arrival (user feedback 2026-10-27)

The mascot video opened on the mascot running out of the tunnel — a nice *entrance*, but
the thing the buyer wants (the patch) only arrived at second 7. With 2–3 s to hold a
viewer, **shot 1 shows what they want most and what we actually sell**, at full size:
the patch in macro, the name on the back filling the frame, the logo on the ground. Or a
deliberately impressive intro that *is* the trigger (the door opening and the logo
blooming). Never shot 1: a character walking in, an establishing shot, a box still closed
with nothing visible, a face before the product.

Mechanics: `product.json.key_trigger.hook_shot` names the shot (default `s01`); that shot
carries `trigger: true` in `production.json` and its picture is the `proof_in_3s`. The
character / scene can open shot 2. `creative_check.py` fails a hook shot without the flag
and a project whose first shot is not the trigger shot.

## 3. From trigger to hook — the matrix

Build the hook on the trigger, then pick **three different types** from this table for
the variants. "Type" means a different mechanism, not a different wording.

| type (Motion / playbook) | frame 1 shows | first text / line | fits when |
| --- | --- | --- | --- |
| **result_first** (demo) | the trigger already happening | "Open the door…" / "It's here" | the product has a visible effect or print |
| **contrast** (before–after) | the generic thing beside the trigger | "Regular door. My door." | the trigger is a difference |
| **pov** | the viewer's hands/view at the trigger | "POV: game night" | personal items, gifts, daily use |
| **callout** | a face at the lens naming the tribe **with the trigger in the same frame** (the door and its light, the jersey on the body) — a face alone is not a hook | "Chicago fans, watch my door." | fandom, niche identity |
| **curiosity** (wait-for-it) | the trigger hidden, hands mid-action | "Wait for the back" | reveals, unboxing, personalization |
| **bold_claim** / newness | the trigger + a concrete number or "new" | "60-second install" / "2026 patch" | a verifiable claim exists |
| **confession** / relatability | a person in the buyer's situation | "I bought three of these" (only if true) | UGC with a voice |
| **urgency** / sale | the trigger + the offer | "Series week only" (only with a real offer) | bottom of funnel, known price |
| **social_proof** / reaction | someone else reacting to the trigger | the friend's face | gifts, group products (only real reactions) |

Rules carried over from `viral-playbook.md`: the hook is **concrete** (a thing you can see),
**short** (≤7 spoken words, ≤4 on screen), **matches frame 1**, and never promises what is
not on screen. The payoff shot (where `music.drop_on` lands) is the trigger at full size.

## 4. Draft checklist additions (run with the playbook's checklist)

10. **Trigger test** — can a stranger say what the product does from frame 1 + the first
    text alone? If not, the trigger is not in the hook.
11. **Type test** — are the three variants three *types* from §3?
12. **Promise test** — does the payoff shot show exactly what the hook promised?

## Sources (read 2026-10-27)

- [Biddyco — Hook rate and hold rate benchmarks for Meta ads (2026)](https://www.biddyco.com/blog-posts/hook-rate-benchmarks-meta)
- [Billo — From hook rate to hold rate](https://billo.app/blog/hook-rate-to-hold-rate/)
- [Sepia Lab — Hook rate benchmarks](https://sepia-lab.com/en/blog/hook-rate-benchmarks) · [Skaler](https://skaler.app/blog/hook-rate-benchmarks-2026) · [Spark UGC](https://www.sparkugc.com/resources/hook-rate-benchmarks-2026)
- [Motion — Creative Benchmarks 2026: top hook tactics](https://motionapp.com/library/research/creative-benchmarks-2026/top-hook-tactics) · [top hook formats](https://motionapp.com/events/2026-creative-strategy-bootcamp/homebase/top-hook-formats) · [15 proven UGC ad hooks (Savannah Sanchez)](https://motionapp.com/library/talk/15-proven-ugc-ad-hooks-that-are-working-right-now-savannah-sanchez/)
- [Influee — 120 UGC hooks 2026](https://influee.co/blog/hooks) · [AdLibrary — ecommerce TikTok ad patterns](https://adlibrary.com/posts/best-ecommerce-tiktok-ads-examples) · [Stackmatix — hook-first 3 seconds](https://www.stackmatix.com/blog/tiktok-creative-best-practices-2026)
- [Social Media Examiner — Daniel Harmon on videos that sell](https://www.socialmediaexaminer.com/how-to-create-long-form-videos-sell-daniel-harmon/) · [Marketer Gems — Harmon Brothers strategy](https://www.marketergems.com/p/harmon-brothers-viral-ads-strategy)
- [Hormozi hook structure (secondary)](https://skillselion.com/skills/alexsmedile/hormozi-skills/hormozi-hooks) · [Outlier Kit — hooks and retention](https://outlierkit.com/resources/youtube-hooks-and-retention/) · [Descript — audience retention](https://www.descript.com/blog/article/audience-retention-on-youtube)
