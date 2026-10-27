# Ecom ad anatomy — structure, proof, CTA (our rules, built from US DTC/retail practice)

Read after `hooks.md` in Stage 2. `hooks.md` decides the first 2 seconds; this file decides
everything after them and how the ad ends. Sources at the end; the numbers quoted are
vendor/agency data and are used as direction, not as truth.

## 1. What the top US ecom creative teams agree on

1. **The whole persuasion arc fits in 15–30 s** on TikTok/Reels: hook → the thing → why it
   works → proof → one action. Anything that does not move the viewer one step closer to
   buying is cut (AdLibrary, Stackmatix, MHI).
2. **One ad = one idea = one action.** Multiple benefits or multiple CTAs lose both.
3. **Native beats polished.** "Ugly" ads — handheld, phone light, lo-fi captions, a person
   talking to the lens, raw unboxing — win on cold traffic because they look like the feed.
   Founder/creator-shot video is rated the strongest format; polished brand film the weakest
   for hook rate (Favoured, Curtis Howland, MHI tables ~62–64% hook rate for problem/
   testimonial openers vs ~44% for polished).
4. **Proof early, not last.** A review line, a count, a before/after or a repeatable test
   placed in the first 10 s lifts completion (claim attributed to Meta by vendors —
   unverified, but every practitioner does it). Harmon Brothers' whole method is a *test
   the viewer could repeat* (raw egg, suds, spoon).
5. **Test the opening, keep the body.** 3–5 hooks on the same body + CTA, let the platform
   pick (Motion, Billo, AdLibrary). We ship 3 (`variants`).
6. **Clear, single CTA, said three ways**: spoken (when there is a voice), on screen, and the
   platform button. "Shop now" wins for ≤$50 impulse items; "Learn more" tests better above
   $50; "link in bio" only when the ad runs from a creator profile (Spark/organic) — a dark
   ad has no bio (TikAdTools, Sagum).

## 2. The five structures we use (pick one in the brief, name it in `production.json.spec.structure`)

| structure | spine (times for a 15–20 s ad) | best for | our formats |
| --- | --- | --- | --- |
| `result_first` | 0–2 trigger happening → 2–6 how it got there → 6–12 details/proof → 12–15 trigger again big + CTA | visible-effect products (lights, prints, transformations) | hype_montage, demo_steps |
| `problem_solution` | 0–3 the annoyance, visible → 3–5 the product appears → 5–12 it working + one proof → 12–15 CTA | gadgets, fixes, gifts that solve "what do I buy him" | ugc_dialogue, demo_steps |
| `unbox_reveal` | 0–2 box/tissue, trigger half-hidden → 2–5 reveal (drop) → 5–11 try-on / details → 11–15 full look + CTA | apparel, personalised items, gifts | hype_montage, calm_lofi |
| `us_vs_them` | 0–2 generic vs ours side by side → 2–8 three visible differences → 8–12 the trigger alone → CTA | POD with a better print/patch, upgraded accessories | hype_montage |
| `three_reasons` | 0–2 "3 reasons" + trigger → 3 × (reason slam + 3 s proof shot) → CTA | products with 3 concrete, showable facts | demo_steps, ugc_dialogue |

Every structure keeps the playbook rules: payoff shot on the drop, re-hook every 2–4 s,
uneven rhythm, text = claim / picture = proof.

## 3. The proof ladder (climb as high as the product allows)

demonstration on camera (the trigger happening) > repeatable test (the viewer could do it)
> before/after or side-by-side > real reaction of another person > a real review line or a
count > a bare claim. A video that only claims is the weakest video. Never invent reviews,
counts or reactions; if there is nothing real, stay on demonstration.

## 4. CTA rules (our fixed form)

1. **One action**, the same words in every variant of a project (`brand.default_cta` or the
   project's CTA line). ≤ 4 words on screen: "Get yours — link ↓", "Shop now ↓",
   "Personalize yours ↓".
2. **Timing**: the CTA shot is the **last 2 s**; ads over 20 s also carry a quiet mid-CTA
   (the CTA pill for ~1.5 s at ~60 % of the runtime, on a shot where the product fills the
   frame). Never a CTA before the payoff.
3. **Picture under the CTA** = the trigger at full size or the person pointing/looking at
   the lens; never a black end card, never a logo-only frame.
4. **Platform wording**: dark ads → "Shop now / link below"; creator-posted (Spark, organic)
   → "link in bio" is allowed; price ≥ $50 → "See it ↓" / "Learn more" style softer line.
5. **Offer only when real**: a discount, bundle or deadline goes in the CTA line only if the
   user gave it (`product.json` facts). No "today only" without a real end date.
6. With a voice: the spoken CTA is the last line, short ("Link's below."), ≥ 0.8 s of hold
   after it so the platform's own button has time to register.

## 5. Writing the story table with this file

1. `key_trigger` → hook type (hooks.md §3) → frame 1.
2. Pick the structure (§2) that gets the trigger on screen soonest and proven best (§3).
3. Fill the shots per the structure's spine; mark which shot is *proof* and which is the
   *payoff* (`music.drop_on`).
4. CTA per §4; three variants = three hook types, same body, same CTA.
5. Run the playbook checklist + hooks.md §4 (trigger / type / promise tests).

## Sources (read 2026-10-27)

- [AdLibrary — DTC ad intelligence: creative frameworks 2026](https://adlibrary.com/posts/dtc-ad-intelligence-creative-frameworks-2026) · [Best DTC Meta ads examples 2026](https://adlibrary.com/posts/best-dtc-meta-ads-examples-2026) · [Best ecommerce TikTok ads patterns](https://adlibrary.com/posts/best-ecommerce-tiktok-ads-examples)
- [Stackmatix — Ecommerce Facebook ads strategy 2026](https://www.stackmatix.com/blog/ecommerce-facebook-ads-strategy-2026) · [Hook-first 3 seconds](https://www.stackmatix.com/blog/tiktok-creative-best-practices-2026)
- [MHI Growth Engine — Best DTC ad hooks 2026](https://mhigrowthengine.com/blog/best-dtc-ad-hooks-2026/) · [Problem-solution ad format](https://mhigrowthengine.com/blog/problem-solution-ad-format-dtc/)
- [Favoured — Ugly ad creative 2026](https://favoured.co.uk/ugly-ad-creative-2026/) · [Curtis Howland — $100M on Meta in DTC](https://newsletter.curtishowland.com/p/ive-spent-100m-on-meta-ads-in-the) · [Aura — 12 creative formats](https://www.auraads.co/post/12-creative-formats-dtc) · [Tower33 — format and hook teardown](https://tower33.com/articles/best-dtc-advertising-examples/)
- [TikAdTools — TikTok ads CTAs](https://tikadtools.com/blog/tiktok-ads-cta/) · [Sagum — CTA phrases for TikTok ads](https://sagum.com/2026/07/12/what-are-effective-call-to-action-phrases-for-tiktok-ads-3/)
- [Reloop — ecommerce video ads full-funnel](https://reloop.so/blog/article/ecommerce-video-ads/) · [SwipeReel — ecommerce video ads that convert](https://blog.swipereel.app/ecommerce-video-ads-create-convert-2026)
- Harmon Brothers / Hormozi / Motion / benchmark sources: see `hooks.md`.
