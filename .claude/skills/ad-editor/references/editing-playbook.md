# Editing playbook — how short-form editors think, mapped to this pipeline

The scripts land cuts on beats and keep speech whole. What they cannot do is
*choose*: which second of a clip, how long to hold, where the text goes, when
to slow down. This file is for those choices. Read it before setting
`moment`, `override`, `speed`, `overlay_pos` or `fx`.

## 1. Every cut must earn its place

A cut is a promise of new information. Before placing one ask: what does the
viewer see after the cut that they could not see before? New subject, new
angle, new scale (wide → close), new state (off → on). Two consecutive shots
of the same thing from the same distance are one shot — merge them or drop
one. The tool that shows this fastest is `edit/qc/sheet.jpg`: read it as a
comic strip; any two adjacent panels that look alike are a problem.

## 2. Start on action, not before it

Veo clips open with a quarter second of settling and often a slow first
second. The viewer should land *inside* motion: the hand already peeling, the
door already swinging. `moment: "peak"` finds the busiest window;
`moment: "b"` jumps to the second action; a manual `override.src_in` does the
rest. The only shot allowed to start calm is a deliberate hold on the product.

## 3. Rhythm: fast, fast, fast, hold

Even 2-second shots feel like a slideshow. Build runs: three short shots
(1 beat or 2 beats each) into one long one (4 beats) on the shot that
matters — the reveal, the print close-up, the reaction. In `production.json`
that is simply uneven `use_sec` values; the beat snapper keeps the cuts on
the grid. The payoff shot may also run at `speed: 0.6–0.75` (slow motion) so
the hold feels intentional rather than long.

## 4. Where the drop goes

The drop is the loudest moment; put the strongest *picture* there
(`music.drop_on`), not the CTA. If the track has no usable drop within the
video length (`drop_on: "none"`), make the strongest picture land on a
downbeat that starts a new bar instead.

## 5. Text placement

Text competes with the product for the eye. Rules in order:
1. Never over a face, the print, the logo or the hands doing the action.
2. Prefer the emptiest band of the frame (`overlay_pos: "auto"` measures
   edge density and picks it; override when it guesses wrong).
3. Slam the text on the cut or on the downbeat right after it, never mid-shot
   for no reason.
4. One idea per slam, ≤ 4 words; the highlighted `*word*` is the one the
   viewer must read if they read nothing else.
5. The CTA button sits where the product is *not*; on a shot where the product
   fills the bottom, send it to the top.

## 5b. Fonts — one voice per video, chosen by format (user rule 2026-10-27)

Research (TikTok Sans / Montserrat / Bebas guides, Verizon motion team): bold sans-serifs
survive compression and small screens; a condensed face fits a long hook in a tall
column; a serif only large and sparing; contrast (box, stroke, shadow) matters as much
as the face; type is *cut in* or moved slightly, never flown around while someone reads.
Our presets (`text_style.preset`, rendered by `render.py`):

| preset | face (macOS local) | entrance | use for | never for |
| --- | --- | --- | --- | --- |
| `bold` | Impact, 16 px stroke, tilted | slam + jitter | hype_montage slams, sports/streetwear | calm, luxury, long lines |
| `condensed` | Futura Condensed ExtraBold, tall column | drop from above | hype/demo hooks of 3–4 words, numbers ("60 SEC") | more than 2 lines |
| `box` | Arial Black on a solid accent box | push from left | demo_steps step labels, lists, "3 reasons" | emotional lines |
| `pill` | Inter on a dark pill | fade-up | ugc_dialogue hook + CTA under captions | hype |
| `marker` | Chalkboard SE (hand-written) | scribble pop | UGC "notes", gifts, kids, relatable | product specs, numbers |
| `serif` | Didot Bold, large, airy | slow fade with tracking | calm_lofi, gifts, premium/luxury | fast cuts, slams |

Rules: one preset per video (the CTA may differ only in colour); the `*word*` is the one
the viewer must read; ≤ 4 words per slam; a 4-word slam stays ≥ 1.7 s; keep every line
inside the safe zone and off the face/print (§5). `creative_check` warns when the preset
is outside the format's set.

## 6. Cut effects and sound effects

`fx: hype` adds flash, punch, shake and beat pulses; `fx.sfx` adds a whoosh
before and an impact on every cut and a riser into the drop. Use them for
hype/montage formats. Do **not** use them on calm formats (lo-fi, ASMR,
gift reveals): there the cut itself is the effect and the best transition is
a plain cut on the beat. `intensity` 0.6 is a good middle ground for
"energetic but not aggressive".

## 6b. Transitions — the right one for the cut (user rule 2026-10-27)

Every cut has a transition INTO the next shot (`shots[].transition`, else the Editor
assigns one from `build_timeline.TRANSITION_CYCLE`). Two neighbouring cuts never use the
same effect; the first frame has none (the hook needs nothing in front of it).

| transition | what it does | use when | avoid when |
| --- | --- | --- | --- |
| `cut` | nothing — the cut on the beat is the effect | UGC, calm, any shot where the picture itself changes enough | — |
| `flash` | white hit + small punch | montage cuts on the downbeat, sports/hype | print close-ups (it bleaches the lettering for 3 frames) |
| `whip` | fast horizontal rush with blur | change of place (tunnel → field, bedroom → street) | two shots of the same place |
| `zoom` | punch-in from blur | into the payoff / drop, into a detail (patch, name) | twice in a row |
| `slide` | vertical push | into the CTA, into a step in a list | emotional beats |
| `glitch` | jittered offsets + inverted flicker | hype/streetwear once or twice per video, on a slam | kids, gifts, calm, print shots |
| `dip` | dip to black | calm/luxury scene change, end of an act | fast formats |

`fx.preset`: `hype` = transitions + decaying shake after flash/whip/zoom/glitch + beat
pulses; `clean` = transitions only; `none` = plain cuts. Speed ramps (`speed` 0.6–0.8)
only on the payoff; a ramp everywhere reads as cheap. J-cuts: in UGC, let the next line
start ~0.2 s before the cut when the words run across two shots.

## 7. Printed products: protect the lettering

Video models redraw text whenever the surface turns or the camera whips.
What this means for the cut:
- Use the clip's *calm* windows for print shots (`moment: "calm"`), never the
  half where the person is turning around.
- When a person turns 180°, the other side of the garment is often wrong
  (the NYK jersey showed BRUNSON on the front after the turn). Cut away
  before the turn completes, or use the turn only when the print is out of
  frame.
- Print close-ups: no flash/punch landing on the letters is fine, but keep the
  shake low (`intensity ≤ 0.7`) so letters do not smear.
- Always check `edit/qc/print_*.jpg` against the product photo before
  delivery; the pipeline marks these shots REVIEW on purpose.

## 8. Speed

- Install steps, walking, B-roll with nothing to admire: 1.0–1.3 (crisp).
- Reveal, reaction, print glint, confetti: 0.6–0.8 (slow-mo). Below 0.6 the
  24 fps source starts to stutter.
- Never change speed inside a dialogue shot when the voice is kept.

## 9. Endings

The last shot has the product in frame and a reason to re-watch: a question
on screen, the first frame's subject returning, or motion that is cut
mid-way. The CTA overlays it; it never gets a shot of its own. A black or
empty last frame is the worst possible ending for completion rate.

## 10. The QC eye, in order

1. Thumb test on frame 1 (`sheet.jpg`, first panel): would you stop?
2. Panel-to-panel: anything repeated, anything with no new info?
3. Text over faces/print/hands?
4. Print letters correct in every strict shot?
5. Cuts on beat (`cuts` in `edit-plan.json`), drop on the right shot?
6. Loudness within target, peaks limited (`edit-report.md`).
7. Watch the real file once if you can (`/watch` local); the sheet cannot show
   stutter, smear or a flash that is too long.

## 11. Variants

Every project renders its hook variants (`variants[]` with
`overlay_overrides`). Three variants should differ in *hook type* (result-first
vs POV vs call-out), not just wording. Report them as separate files so the
user can post all three and compare 3-second hold rate.
