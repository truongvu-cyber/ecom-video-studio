# Genre playbooks

Each playbook gives a shot pattern, a default style (number from `styles.md`) and
the traps specific to that genre. Lengths assume a 9:16 Reel; scale the count of
clips to the target length. "Clip" means one generation.

Story shapes most playbooks reuse:

- **Hook -> Build -> Payoff -> CTA** (social default)
- **Problem -> Product -> Proof -> CTA** (ad default)
- **Atmosphere -> Reveal -> Climax -> Logo** (brand film, trailer)

---

## Product and social commerce

### 1. UGC review / testimonial
Style 2. 15-30 s, 2-4 clips.
1. Cold open mid-sentence with the product already in hand.
2. The one detail you can't see in the listing photos, shown in use.
3. A small human beat (a dry aside, a false start), then a casual ending.
- Run the coherence check: who is filming, where the product lives, why now.
- Flat offhand baseline with ONE genuine reaction. Constant excitement reads as
  an ad.
- Product handled and already in use, out of its box. A centered branded box
  is the strongest "paid ad" tell.
- One grip cue instead of a turntable spin: she turns it in her hand and pauses
  when the light catches the detail.
- End on a motion cutoff (arm lowering, frame drifting) or a held final pose,
  not both.

### 2. Unboxing
Style 2 or 8. 15-20 s.
1. Hands on the package, first tear. 2. The reveal moment, close. 3. First use
or first reaction. Hands only avoids face drift; keep the box plain.

### 3. Problem -> solution demo
Style 2 or 8. 15-30 s.
1. The problem visible in frame one (ice on glass, cold coffee, a draft lifting
a tissue). 2. Product applied. 3. The result, held long enough to see.
4. Optional CTA clip. The before must look truly bad and ordinary, not staged.

### 4. Before / after split
Style 8 or 5. 5-10 s, one clip.
`Split vertical composition: left half shows [before], right half shows [after],
identical framing and light on both, static locked-off camera.` Or chain two
clips with matched framing and a wipe in the edit.

### 5. Satisfying / ASMR product
Style 5 or 6. 5-15 s.
Macro, locked off or very slow push. One tactile process per clip: wax melting,
lid clicking, powder pouring, foam rising. Describe the sound: `soft crackle`,
`quiet click`, `no music`. Slow motion words, never fast.

### 6. Hero tabletop B-roll
Style 5, 4 or 21. 5 s per clip.
Orbit, push-in, top-down, texture macro, pour or splash. Keep 1-2 props that
explain the use. Product photo as the first frame.

### 7. Gift reaction / gift guide
Style 2 or 7. 15-30 s.
Gift guide: one clip per item, same framing, same hand, same surface, so the
cut feels like a list. Reaction: the unwrap from over the shoulder, then the
face. Wrapping and prints as the user wants them.

### 8. Comparison
Style 8. Split screen or alternating clips with identical framing; change only
the product.

### 9. Lifestyle / day-in-the-life
Style 1, 6 or 8. 15-30 s.
3-5 short moments in one day, same outfit and light logic (morning to night),
the product appearing naturally in two of them.

## Story and entertainment

### 10. Short film / narrative
Style 1 or any. 30-90 s.
Premise -> want -> obstacle -> turn -> final image. One location per clip. Write
emotion as an ordered chain (`surprise, eyes fill, one tear falls, small smile`)
and add a stop line if needed (`tears never fall, no crying, no smiling`).

### 11. Comedy skit
Style 2 or 3. Setup -> escalation -> punchline -> tag. Comedy lives in timing:
keep each clip one beat, leave a pause before the punch, react shot after it.

### 12. Music video
Style 10, 11, 13 or 17. Cut on the beat: give BPM and plan clips in multiples of
the bar length. Alternate performance shots with mood B-roll. Lip-sync only on
models with audio or a lip-sync tool.

### 13. Horror / thriller teaser
Style 12. Every event needs place + moment + visible result (`at 4s the
wardrobe door swings fully open, revealing darkness`). Slow creeping camera,
silence then a sharp sound. Keep the threat mostly unseen.

### 14. Fantasy / epic / xianxia
Style 26 or 23. Wide establishing with a small figure seen from behind avoids
face errors and sells scale. One focal element per frame. Describe creatures
part by part (antlers, long whiskers, scaled serpent body, four clawed legs);
a name alone gives the wrong animal.

### 15. Animated kids story
Style 15, 16 or 19. Character model sheet first. Bright, simple, one action per
clip, gentle camera. Narration in post.

## Information and service

### 16. Explainer / how-to
Style 22, 8 or 21. Step per clip, same angle for every step, hands not faces.
All labels and numbers in the edit.

### 17. Talking head / educator
Style 3 or 8. Medium shot, eye level, locked off with a slow push on key lines.
Veo or Kling 3.0 for speech; otherwise voiceover over B-roll.

### 18. Food / recipe
Style 5 or 6. Overhead flat lay for steps, 45-degree close-up for the money shot,
steam visible, warm window light. Liquids and pours in slow motion.

### 19. Fashion / lookbook
Style 1, 9 or 10. Same model sheet every clip. Walk toward camera, 360 orbit,
fabric detail macro. Jump cuts between outfits work on multi-shot models.

### 20. Travel / real estate / place
Style 13 or 8. Drone reveal -> walk-through -> detail -> golden hour closer.
For a long take say `single continuous shot, no cuts, always moving forward`.

### 21. Logo reveal / brand sting
Style 21 or 22. 3-5 s. Particles, light sweep or material morph that resolves to
a clean end frame. Build the real logo in the editor; the model makes the
motion around an empty space.

---

## Mapping script beats onto clips

- HOOK beat -> clip 1. Its first frame must already show the product working or
  the problem visible.
- MID beats -> demo / proof clips, one main action each.
- CTA beat -> a clean end clip with room for the overlay text in the top 15% or
  bottom 20% safe zones.
- `shotplan.py` does the packing; you choose the action and camera for each clip.
