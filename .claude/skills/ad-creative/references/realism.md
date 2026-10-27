# Realism and physical logic for people in clips (user rule 2026-10-27)

Applies to **every prompt** (keyframe or clip) in which a person, a hand or a
face appears. The user's words: people must look like real people, and every
action must obey ordinary physics — no one walks through a car door, a hand
does not pass through a panel, an object does not float. Scenes that break
this are failed clips, whatever else is right about them.

## 1. The REALISM lock (paste word for word)

Written once in the locks section of `prompts.md` as **REALISM**, pasted into
every prompt that contains a person, after CHARACTER/STYLE:

```
Real human being filmed on a phone: natural skin with pores and slight unevenness, real eyes with reflections, hair with individual strands, clothing that creases and hangs with weight. Every movement obeys physics: feet stay on the ground, weight shifts before a step, hands grip objects with correct finger placement and stay on their surfaces, bodies and clothes keep clear of the car, the door, the ground and each other, objects keep their size and weight. One continuous action at real speed.
```

Bans ("no beauty filter", "no plastic skin") stay out of the lock and go in the
negative (§4): `prompt_lint` counts "no …" phrases. The lock plus the blocking
sentences may push a clip past lint's 200-word sweet spot; that warning is
accepted for person clips, nothing else is cut to make room.

## 2. Blocking rule — say where bodies are relative to solid things

Veo/Omni break physics most often when the prompt leaves a path ambiguous
("walks up to him" next to a car = walks through the door). So every person
clip states, in this order:

1. **Where each person starts** relative to the solid objects in frame
   (`standing on the driver's side, outside the open door, one step back from
   the sill`).
2. **The path** of any movement, around obstacles, not across them
   (`walks around the back of the car and stops beside him, on the open side
   of the door`). Never write a destination without a path when something
   solid is between.
3. **Which hand does what, on which surface** (`right hand holds the unit flat
   against the lower door panel; left hand presses the centre`).
4. **The camera does not move through anything** either.

Forbidden verbs without a stated path: *walks up, comes over, steps in, leans
in, reaches across, runs to* when a door, a window, a table or another person
is between start and end.

## 3. Action logic checklist (run on every person clip before delivery)

| check | pass when |
| --- | --- |
| cause → effect | the result shown has a visible cause (door closes → logo goes dark; hand peels → liner comes off) |
| one body, one place | nobody is in two places; a person who walked in did not also start in frame |
| hands match the object | number of hands, grip and object size agree with the keyframe and the real product (`install_steps_*.png`) |
| door / car geometry | people stand on the ground outside the car or sit inside it; a door is either open or closed; nobody passes the sill |
| eye line | a person reacting to something looks at it |
| time | an 8 s clip holds one or two actions at real speed; no teleport between halves |
| gender / count | the prompt says how many people and who they are (`his friend, a man in his 30s`) so the model does not add or swap people |

## 4. Negative words for person clips (append to the clip's negative)

`plastic skin, airbrushed, beauty filter, uncanny face, extra fingers, fused fingers, distorted hands, extra limbs, body passing through the car or door, clipping through objects, floating objects, morphing, duplicated person, teleporting, sliding feet, warped background`

## 5. Quality pass after generation

`scripts/takes_sheet.py` / `edit/qc/takes.jpg` at 1 frame per second: look
for intersections (a limb inside the door, a hand inside the panel), a
person who appears or vanishes between frames, feet off the ground, changed
face. One failed frame in the part the Editor would use = regenerate with the
blocking rewritten (§2), not with a longer negative.
