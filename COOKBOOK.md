# COOKBOOK — tested effect numbers

Status: **living document**
Last updated: 2026-10-30
Owner: the agent that builds the reel
Used by: `ReelMasterprompt.md` (section 2.1), the validator, and every builder

Every effect name Gemini may use must exist here with **tested numbers**. An effect without
tested numbers is not allowed in a scene card. When a new effect is written or first used in a
rendered reel, add it here in the same pass. Never leave a used effect undocumented.

Sources currently in the book:

- `shani-ka-daur/` (Reel 02, Hindi, light theme)
- `wahi-insaan-papercut/` (Reel 03, paper-cut)
- `planet-sabotage/` (Hindi, dark astrology)
- `chalkline-03-rewire/` (English, chalkline)

---

## 0. Status key

| Status | Meaning | Allowed in cards? |
|---|---|---|
| **TESTED** | Rendered in a real reel; numbers below are the numbers used. | yes |
| **PARTIAL** | Motion exists but not in the exact form named (or not rendered). | no |
| **RESERVED** | Menu name only. No implementation yet. | no |

If a card needs a PARTIAL or RESERVED effect, stop and return `NEEDS_EFFECT` with a
description. Build it once, render it, then promote it to TESTED.

## 1. Conventions

- All times are seconds. `at` is **scene-relative**.
- All durations are the actual tween duration; holds are separate.
- Eases are GSAP names (`power1.out`, `power2.inOut`, `back.out(1.6)`, `steps(14)`, `none`).
- `cam` is the camera group. Only `shake`, `zoom-punch`, `push-in` touch `cam`.
- Text plate is `z5`; FX is `z4`; nothing below `z4` may cover the plate.
- `amp` means shake amplitude in px; `from` means the starting scale.
- Stroke widths stay at or below 8 px unless the source says otherwise.
- Do not rescale a TESTED effect by more than ±20 %. If a scene needs more, build a variant
  and add it as a new entry.

---

## 2. Effect index

| # | Effect | Status | Primary use | First tested in |
|---|---|---|---|---|
| 1 | `pop-in` | TESTED | small element / word entrance | Reel 02 S01 |
| 2 | `slam-in` | TESTED | hero entrance | Reel 02 S08 |
| 3 | `fade` | TESTED | dim, exit, background | Reel 02 |
| 4 | `bounce` | TESTED | falling object settles | Reel 02 S07 |
| 5 | `wobble` | TESTED | paper/collage idle texture | Reel 03 |
| 6 | `push-in` | TESTED | camera leans into a beat | Reel 03 S14 |
| 7 | `parallax` | TESTED | depth in a starfield / crowd | planet-sabotage S01 |
| 8 | `zoom-punch` | TESTED | stress a word | planet-sabotage S01 |
| 9 | `shake` | TESTED | impact | Reel 02 |
| 10 | `flash` | TESTED | impact frame | Reel 02 |
| 11 | `glitch` | TESTED | digital break | planet-sabotage S01 |
| 12 | `speed-lines` | TESTED | fast travel | Reel 03 S22 |
| 13 | `wipe` | PARTIAL | straight screen wipe | not built |
| 14 | `paper-wipe` | TESTED | scene transition | Reel 03 S03 |
| 15 | `reveal-mask` | TESTED | text / object reveal | Reel 03 S07 |
| 16 | `line-draw` | TESTED | single stroked path | Reel 02 S03 |
| 17 | `draw-path` | TESTED | long path + trace head | chalkline S05 |
| 18 | `strike` | TESTED | cancel / cross out | Reel 02 S03 |
| 19 | `highlighter` | TESTED | accent word | Reel 03 |
| 20 | `stamp` | TESTED | verdict card | Reel 03 S02 |
| 21 | `type-on` | TESTED | display word | chalkline S14 |
| 22 | `print-on` | RESERVED | receipt / line-by-line print | not built |
| 23 | `scroll-feed` | RESERVED | tape / feed motion | not built |
| 24 | `count-up` | TESTED | number / meter | Reel 02 S14 |
| 25 | `fly` | TESTED | paper plane / object | Reel 03 S23 |
| 26 | `walk` | TESTED | figure crosses ground | Reel 03 S22 |
| 27 | `orbit-dot` | TESTED | dot circles a motif | Reel 03 S17 |
| 28 | `stack-bricks` | TESTED | build / accumulate | Reel 02 S19 |
| 29 | `crack` | TESTED | break a shape | Reel 03 S18 |
| 30 | `tick-stamp` | TESTED | mark an item done | Reel 02 S09 |
| 31 | `wilt` | TESTED | motif loses life | Reel 03 S08 |
| 32 | `snip` | TESTED | cut a ring / bond | Reel 03 S21 |
| 33 | `loop-cut` | TESTED | break a cycle | Reel 03 S22 |
| 34 | `flag-drop` | TESTED | red flags land | Reel 03 S13 |
| 35 | `alarm-shake` | TESTED | clock / alarm rings | Reel 03 S15 |
| 36 | `point-slam` | RESERVED | pointer hits a spot | not built |

Totals: **32 TESTED, 1 PARTIAL, 3 RESERVED**.

---

## 3. Entries

### 1. pop-in — TESTED

- **Does:** small element enters with a soft overshoot.
- **Target:** any element at `z2`–`z4`; text words.
- **Params:** `scale: .85 -> 1`, `y: 24 -> 0`, `opacity: 0 -> 1`, `duration: .12`, `ease: back.out(1.6)`, origin `50% 50%` (paper-cut uses `50% 55%`).
- **Group stagger:** `.10`–`.15` per item. Text words: use their own word start, not a fixed stagger.
- **Tested:** Reel 02 S01/S11; Reel 03 S01–S03; planet-sabotage every scene's words.
- **Source:** `shani-ka-daur/tools/build.py:462`, `wahi-insaan-papercut/tools/build.py:341`, `planet-sabotage/compositions/scene-01.html:74`.
- **Rules:** never on `cam`; do not combine with `slam-in` on the same element.

### 2. slam-in — TESTED

- **Does:** hero arrives hard and stops.
- **Target:** hero element at `z3`/`z4`.
- **Params:** `scale: 1.35 -> 1` (large hero `1.4`–`1.8`), `opacity: 0 -> 1`, `duration: .14` (large `.18`), `ease: power4.out`.
- **Tested:** Reel 02 S08 (`1.6`, `.14`), S16 (`1.5`, `.14`); Reel 03 S20 (`1.8`, `.18`).
- **Source:** `shani-ka-daur/tools/build.py:463`, `wahi-insaan-papercut/tools/build.py:342`, `planet-sabotage/compositions/scene-01.html:73`.
- **Rules:** one hero per scene; not for body text; pair with `shake` only if impact is the point.

### 3. fade — TESTED

- **Does:** opacity change; no transform.
- **Target:** any layer.
- **Params:** `opacity: 0 -> 1` or `1 -> 0`, `duration: .1`–`.6`, `ease: none` for exits, `power2.out` for dims.
- **Tested:** Reel 03 S07 (`reveal` pairs with fade), S14 dims `.2`; chalkline captions `.2` in / `.2` out, dims `.7`.
- **Source:** `chalkline-03-rewire/index.html:509`, `674`–`676`; `wahi-insaan-papercut/tools/build.py` scene dims.
- **Rules:** never the only motion in a scene longer than 1 s; never used to hide a bad cut.

### 4. bounce — TESTED

- **Does:** object falls, rebounds twice, settles.
- **Target:** object at `z2`/`z3` (die, brick, ball).
- **Params:** drop `y: -420 -> 0`, `.2`, `power2.in`; rebound `-60 -> 0`, `.12`, `power1.out`; rebound `-24 -> 0`, `.08`, `power1.in`; settle `scale 1.12 -> 1`, `.1`.
- **Walk bob variant:** `y: -8`, `.2`, `repeat: 5`, `yoyo: true`, `sine.inOut`.
- **Tested:** Reel 02 S07; Reel 03 S22 (walker bob).
- **Source:** `shani-ka-daur/tools/build.py:318`–`326`; `wahi-insaan-papercut/tools/build.py:888`–`894`.
- **Rules:** max two rebounds; total `.55`–`.65`; the ground line is y 1040.

### 5. wobble — TESTED

- **Does:** paper pieces breathe with tiny jitter.
- **Target:** cutout/paper element wrapper only.
- **Params:** four CSS variants; `translate` max `1.2 px`, `rotate` max `.55 deg`; periods `.26`, `.30`, `.34`, `.38 s`; `steps(1,end)` infinite.
- **Tested:** Reel 03 (S01, S02, S03, S05, S08, S13, S16, S17).
- **Source:** `wahi-insaan-papercut/tools/build.py:326`–`333`.
- **Rules:** only when the card says `wobble: true`; never on text, plate, or FX; never on every element in a scene.

### 6. push-in — TESTED

- **Does:** camera slowly moves closer.
- **Target:** `cam`.
- **Params:** `scale: 1 -> 1.03`–`1.10`, `duration: .25`–`.5`, `ease: power2.inOut`; long hold variant `1 -> 1.06` over the whole scene with `power1.inOut`.
- **Tested:** Reel 03 S14 (`1.10`, `.25`), S17 (`1.06`, `.3`), S24 (`1.03`, `.5`); planet-sabotage S31 (`1.06`, whole scene).
- **Source:** `wahi-insaan-papercut/tools/build.py:733`, `783`, `922`; `planet-sabotage/compositions/scene-31.html:96`.
- **Rules:** max `1.10`; one per scene; origin at the subject, not always `540 640`.

### 7. parallax — TESTED

- **Does:** layers drift at different speeds, giving depth.
- **Target:** 2–3 background/mid layers; one foreground layer.
- **Params:** same duration as the scene, `ease: none`; tested star speeds over `2.32 s`: `13.92`, `32.48`, `64.96 px` (ratio 1 : 2.33 : 4.67). Crowd variant: background `x: 0 -> 280`, `1.3 s`, `power1.inOut`; foreground walker `x: 0 -> 400`, `1.2 s`, `none`.
- **Tested:** planet-sabotage S01; Reel 03 S22.
- **Source:** `planet-sabotage/compositions/scene-01.html:81`–`83`; `wahi-insaan-papercut/tools/build.py:888`–`894`.
- **Rules:** back layer slower than front; no reversal mid-scene; max 4 layers.

### 8. zoom-punch — TESTED

- **Does:** camera snaps closer on a stressed word, then releases.
- **Target:** `cam`.
- **Params:** `scale: 1 -> 1.12`, `.16`, `power3.out`; back `1.12 -> 1`, `.3`, `power2.inOut`. Hero variant: `1 -> 1.12`, `.08`, then back `.1`.
- **Tested:** planet-sabotage S01; Reel 02 S08 (`1.08`, `.2`/`.3`).
- **Source:** `planet-sabotage/compositions/scene-01.html:72`; `shani-ka-daur/tools/build.py:327`–`334`.
- **Rules:** max `1.12`; one per scene; never two consecutive scenes.

### 9. shake — TESTED

- **Does:** camera jitters on impact.
- **Target:** `cam`.
- **Params:** random `x/y = ±amp*k`, `k` decays `1 -> 0`; `n = max(3, round(dur*30))` steps of `1/30 s`; return to 0 in one frame. `amp: 3`–`14`; `dur: .08`–`.25`. Planet variant adds `rotation: ±amp*.05`.
- **Tested:** Reel 02 S02 (`6`,`.2`), S06 (`7`,`.2`), S15 (`8`,`.2`); Reel 03 S02 (`8`,`.2`), S16 (`10`,`.25`), S20 (`12`,`.25`); planet-sabotage S20 (`14`,`.25`).
- **Source:** `shani-ka-daur/tools/build.py:464`, `wahi-insaan-papercut/tools/build.py:343`, `planet-sabotage/compositions/scene-01.html:73`.
- **Rules:** `amp <= 14`; `dur <= .25`; never on the text plate; not in two consecutive scenes.

### 10. flash — TESTED

- **Does:** one impact frame over the whole stage.
- **Target:** full-frame overlay at `z4` (below plate).
- **Params:** `opacity: 0 -> .85`–`.9`, `.034`, `none`; then `-> 0`, `.067`, starting at `at + .034`. Color per world (ink `#14141A`, white `#FFFFFF`, world accent).
- **Tested:** Reel 02 S02/S15; planet-sabotage S01/S20.
- **Source:** `shani-ka-daur/tools/build.py:465`, `planet-sabotage/compositions/scene-01.html:74`, `wahi-insaan-papercut/tools/build.py:351`.
- **Rules:** one per scene; never over the plate; do not use on every impact.

### 11. glitch — TESTED

- **Does:** short digital break.
- **Target:** stage group + glitch bars.
- **Params:** 3 frames of `x: ±7`, `1/30 s` each; back to `0`, `1/30 s` at `at + .1`; bars `opacity: .85 -> 0`, `.14`.
- **Tested:** planet-sabotage S01.
- **Source:** `planet-sabotage/compositions/scene-01.html:79`.
- **Rules:** max 3 frames; not consecutive scenes; never on the plate or text.

### 12. speed-lines — TESTED

- **Does:** lines streak across the frame to sell speed.
- **Target:** full-frame FX layer `z4`.
- **Params:** lines `x: -900 -> 900` (or reverse), `opacity: .55 -> 0`, `.2`, `power2.in`/`power2.out`, stagger `.004`. Static variant: `opacity: 0 -> 1`, `.1`; out `.2` at `1.0`.
- **Tested:** planet-sabotage (every scene's `speed()`); Reel 03 S22.
- **Source:** `planet-sabotage/compositions/scene-01.html:78`; `wahi-insaan-papercut/tools/build.py:288`, `888`–`894`.
- **Rules:** only during motion; strokes `<= 3 px`; cover `<= 10 %` of the hero (FX law).

### 13. wipe — PARTIAL

- **Does:** straight-edge panel sweeps the frame.
- **Params (inherited):** `xPercent: 0 -> -112`, `.18`, `power3.inOut`; hide at `.19`.
- **Why partial:** the rendered implementation uses the ragged paper edge (see `paper-wipe`). The straight-edge version is not built yet.
- **Source:** `wahi-insaan-papercut/tools/build.py:324`, `939`–`940`.
- **Rules:** do not use until built and rendered. Use `paper-wipe` for paper worlds.

### 14. paper-wipe — TESTED

- **Does:** torn-paper panel sweeps to the next scene.
- **Target:** full-frame panel `z70`.
- **Params:** `xPercent: 0 -> -112`, `.18`, `power3.inOut`; `display: none` at `.19`. Panel color = next block's backdrop. Ragged edge via `clip-path` polygon (`.wipe` class).
- **Tested:** Reel 03 S03/S06/S09/S13/S15/S19/S21/S23.
- **Source:** `wahi-insaan-papercut/tools/build.py:324`–`325`, `939`–`940`.
- **Rules:** transitions only, never inside a beat; one per scene boundary.

### 15. reveal-mask — TESTED

- **Does:** element appears left-to-right through a mask.
- **Target:** text block or single object.
- **Params:** `clipPath: inset(0 100% 0 0) -> inset(0 0% 0 0)`, `.35`–`.55`, `steps(14)`.
- **Tested:** Reel 03 S07 (`.35`), S24 (`.55`).
- **Source:** `wahi-insaan-papercut/tools/build.py:349`, `616`–`634`, `910`–`933`.
- **Rules:** left-to-right only; no full-stage reveal unless it is the scene transition.

### 16. line-draw — TESTED

- **Does:** single stroked path draws itself.
- **Target:** `path`, `circle`, `line`, `ellipse`, `polyline`, `polygon`, `rect`.
- **Params:** `strokeDasharray = L`, `strokeDashoffset: L -> 0`, `.25`–`.7`, `power2.out` (chalkline uses `.3`–`.7`, `power1.inOut`).
- **Tested:** Reel 02 S03/S04/S08/S09; Reel 03 S09/S11; chalkline S01.
- **Source:** `shani-ka-daur/tools/build.py:466`, `wahi-insaan-papercut/tools/build.py:344`, `chalkline-03-rewire/index.html:505`–`508`.
- **Rules:** stroked paths only; no fill animation; stroke `<= 8 px`.

### 17. draw-path — TESTED

- **Does:** long multi-segment path draws, optionally with a trace head.
- **Target:** road, arrow, waveform, door panel.
- **Params:** `strokeDashoffset: L -> 0`, `.6`–`1.5`, `power1.inOut`; optional `stroke-width: 2 -> 5`; trace head `t: 0 -> 1`, same duration; 5-dot trail.
- **Tested:** chalkline S05 (`1.5`), S06 (`1.0`), S13 (`1.05`).
- **Source:** `chalkline-03-rewire/index.html:542`–`544`, `557`–`558`.
- **Rules:** use for paths longer than ~400 px; trace head only when the draw direction matters.

### 18. strike — TESTED

- **Does:** a line crosses something out.
- **Target:** struck word or tag.
- **Params:** `scaleX: 0 -> 1`, origin left, `.12`–`.2`, `power3.out`; width variant `0 -> 190 px`, `.35`, `power2.inOut`.
- **Tested:** Reel 02 S03/S09; Reel 03 S18; chalkline S10 (`width 190`, `.35`).
- **Source:** `shani-ka-daur/tools/build.py:292`–`299`, `335`–`342`; `wahi-insaan-papercut/tools/build.py:788`–`804`; `chalkline-03-rewire/index.html:607`.
- **Rules:** stroke `<= 8 px`; only over text/tag; one per scene.

### 19. highlighter — TESTED

- **Does:** marker block sweeps behind an accent word.
- **Target:** inline `<i class="hl">` behind the word.
- **Params:** `scaleX: 0 -> 1`, `.15`, `power2.out`; block `opacity: .34`, `top: .10em`, `bottom: .14em`, `left/right: -.05em`, `border-radius: 3px`.
- **Tested:** Reel 03 (every accent word).
- **Source:** `wahi-insaan-papercut/tools/build.py:320`–`323`, `417`, `468`.
- **Rules:** one accent per card; `z-index: -1` behind text.

### 20. stamp — TESTED

- **Does:** verdict card hits the page.
- **Target:** card / tag at `z3`/`z4`.
- **Params:** `scale: 1.5`–`1.8 -> 1`, `rotation: -8 -> 0` (or `-8 -> -4`), `opacity: 0 -> 1`, `.12`–`.22`, `power4.out`; optional `shake(6, .12)`.
- **Tested:** Reel 03 S02 (`1.8`, `.12`), chalkline S10 (`1.7`, `.22`, `-8 -> -4` + jitter), Reel 02 S16 (`1.5`, `.14`).
- **Source:** `wahi-insaan-papercut/tools/build.py:347`, `550`–`554`; `chalkline-03-rewire/index.html:600`–`605`; `shani-ka-daur/tools/build.py:384`–`390`.
- **Rules:** text `<= 3` words; never on the plate; pair with one shake at most.

### 21. type-on — TESTED

- **Does:** display word types in letter by letter.
- **Target:** Latin display words only.
- **Params:** per letter `opacity: 0 -> 1`, `x: ±6`, `y: ±4`, `scale: 1.3 -> 1`, `.18`, `power3.out`, stagger `.045`. Caption variant: word `opacity: 0 -> 1`, `.12`, `none`, stagger `.24`.
- **Tested:** chalkline S14 (`REWIRE`).
- **Source:** `chalkline-03-rewire/index.html:657`–`669`, `674`–`676`.
- **Rules:** `<= 12` letters; Latin only; not for Devanagari conjuncts.

### 22. print-on — RESERVED

- **Does (planned):** receipt / line-by-line print, one line every `.1 s` from frame 0.
- **Status:** no implementation. The pack's Example B is a format example, not code.
- **Closest tested parts:** `reveal-mask` per line + `stamp`.
- **Rules:** do not use until built and rendered.

### 23. scroll-feed — RESERVED

- **Does (planned):** tape/feed moves continuously while a total counts.
- **Status:** no implementation.
- **Closest tested parts:** `parallax` (continuous drift) + `count-up`.
- **Rules:** do not use until built and rendered.

### 24. count-up — TESTED

- **Does:** number (and optional bar) counts to a value.
- **Target:** text number and/or meter fill.
- **Params:** object `{v: from} -> {v: to}` with `onUpdate`; `.22`–`2.0`; `power3.out`, `power2.out`, or `power1.inOut`. Bar: `scaleX: from/100 -> to/100`, same duration; color change `.12` at end.
- **Tested:** Reel 02 S01 (`20 -> 100`, `.55`), S06 (`0 -> 62`, `.8`), S14 (`0 -> 99`, `2.0`); planet-sabotage meter (`0 -> 100`, `.25`).
- **Source:** `shani-ka-daur/tools/build.py:275`–`282`, `310`–`317`, `369`–`376`; `planet-sabotage/compositions/scene-01.html:76`.
- **Rules:** integer only; `<= 2.0 s`; bar and number share a start time.

### 25. fly — TESTED

- **Does:** object travels on an arc to a target.
- **Target:** paper plane, object at `z4`.
- **Params:** `x -> dx` and `y -> dy` over `.7`, `power1.inOut`; arc: `y -> dy - arc` over `.35`, `power2.out`, then `-> dy` over `.35`, `power2.in`; `arc: 150`–`180`.
- **Tested:** Reel 03 S23 (`460, -280`, `.7`, `180`).
- **Source:** `wahi-insaan-papercut/tools/build.py:348`, `897`–`909`.
- **Rules:** physical objects only; never text; landing point must be on-stage.

### 26. walk — TESTED

- **Does:** silhouette crosses the ground with a small bob.
- **Target:** silhouette figure at `z3`; ground at y 1040.
- **Params:** `x: 0 -> 400`, `1.2`, `none`; bob `y: -8`, `.2`, `repeat: 5`, `yoyo: true`, `sine.inOut`.
- **Tested:** Reel 03 S22.
- **Source:** `wahi-insaan-papercut/tools/build.py:888`–`894`.
- **Rules:** feet on the ground line; no walk cycle required; one walker per scene.

### 27. orbit-dot — TESTED

- **Does:** dot circles a motif.
- **Target:** 26 px dot, `z4`.
- **Params:** `rotation: 0 -> 360`, `1.4`, `repeat: 1`, `none`, origin `-130px 165px` (paper-cut). Ring variant: `rotation: 0 -> 145` over the whole scene, `none`, `svgOrigin: 540 700`.
- **Tested:** Reel 03 S17; planet-sabotage S31.
- **Source:** `wahi-insaan-papercut/tools/build.py:783`–`785`; `planet-sabotage/compositions/scene-31.html:97`.
- **Rules:** one orbit per scene; never over text; dot stays inside STAGE.

### 28. stack-bricks — TESTED

- **Does:** bricks/boxes stack in sequence.
- **Target:** bricks at `z2`/`z3`; ground line.
- **Params:** `y: -200 -> 0`, `.16`–`.18`, `power4.in`; stagger `.06`–`.10`; `shake(4, .08)` per hit; optional settle `scaleY: .85 -> 1`, `.1`.
- **Tested:** Reel 02 S19 (7 bricks, `.06`); Reel 03 S04 (`-260`, `.2`), S05 (`.18`).
- **Source:** `shani-ka-daur/tools/build.py:400`–`404`; `wahi-insaan-papercut/tools/build.py:574`–`606`.
- **Rules:** max 7 pieces; stagger `<= .10`; last brick must land by the scene's second beat.

### 29. crack — TESTED

- **Does:** fracture lines appear on a shape.
- **Target:** 2–5 crack paths at `z4`.
- **Params:** `opacity: 0 -> 1`, `.05`; `strokeDashoffset: L -> 0`, `.12`, `power2.out`, stagger `.02`; stroke `5`–`6`; pair with `shake(3–7, .1–.2)`.
- **Tested:** Reel 03 S07/S18; planet-sabotage S20.
- **Source:** `planet-sabotage/compositions/scene-01.html:77`; `wahi-insaan-papercut/tools/build.py:616`–`634`, `788`–`804`.
- **Rules:** 2–5 paths; never full-screen; one shake per crack event.

### 30. tick-stamp — TESTED

- **Does:** checkmark lands on an item.
- **Target:** tick glyph, `z4`.
- **Params:** `opacity: 0 -> 1`, `.06`; `scale: 1.2 -> 1` (or `.55` for small ticks), `.12`–`.15`; optional full stamp `1.8 -> 1`, `.12`.
- **Tested:** Reel 02 S09/S16/S18; Reel 03 S23.
- **Source:** `shani-ka-daur/tools/build.py:335`–`342`, `384`–`390`, `397`–`399`; `wahi-insaan-papercut/tools/build.py:897`–`909`.
- **Rules:** tick `44`–`60 px`; one per item; max 14 ticks.

### 31. wilt — TESTED

- **Does:** motif object loses life; petals fall.
- **Target:** hero object + 6–8 petal pieces.
- **Params:** object `rotation: 0 -> 4`, `1.4`, `sine.inOut`; petals `y: +520 + (i%4)*90`, `x: (i-3)*36`, `rotation: 20 + i*17`, `opacity -> 0`, `1.1`, `power1.in`, stagger `.08`; image `saturate(.7)`.
- **Tested:** Reel 03 S08.
- **Source:** `wahi-insaan-papercut/tools/build.py:635`–`651`.
- **Rules:** 6–8 petals; only on the reel's motif object; once per reel.

### 32. snip — TESTED

- **Does:** scissors cut a ring; the bond opens.
- **Target:** scissors + ring + confetti.
- **Params:** open/closed swap at the word, `.1` apart; split `opacity: 0 -> 1`, `.05`; `shake(8, .2)`; ring `rotation: -3`, `.15`; 8 confetti pieces `y: 420 + (i%3)*90`, `x: (i-4)*40`, `rotation: i*40`, `opacity -> 0`, `.8`, `power1.in`.
- **Tested:** Reel 03 S21.
- **Source:** `wahi-insaan-papercut/tools/build.py:841`–`869`.
- **Rules:** one snip per reel; the cut must change the motif's meaning; `<= 8` pieces.

### 33. loop-cut — TESTED

- **Does:** a cycle/loop breaks and becomes a line.
- **Target:** ring/loop + strip + walker.
- **Params:** ring `scaleY: 1 -> .02`, `.25`, `power2.in`; ring `opacity -> 0`, `.05`; strip `scaleX: 0 -> 1`, `.5`, `power2.out`; walker `x: 0 -> 400`, `1.2`, `none`; speed lines in `.1`, out `.2`.
- **Tested:** Reel 03 S22.
- **Source:** `wahi-insaan-papercut/tools/build.py:870`–`896`.
- **Rules:** only for cycle/loop motifs; not for text or the plate.

### 34. flag-drop — TESTED

- **Does:** red flags land in a row.
- **Target:** 3 flags at `z2`.
- **Params:** `y: -300 -> 0`, `.18`, `power4.in`, `rotation: 4 -> 0`, stagger `.15`; `shake(4, .08)` per flag.
- **Tested:** Reel 03 S13.
- **Source:** `wahi-insaan-papercut/tools/build.py:709`–`722`.
- **Rules:** max 3 flags (pack example); stagger `<= .15`; flags stay behind the figures.

### 35. alarm-shake — TESTED

- **Does:** clock/alarm rings hard.
- **Target:** clock object at `z2`/`z3`.
- **Params:** `scale: .9 -> 1`, `.18`, `back.out(1.5)`; `rotation: 0 -> 6`, `.05`, `repeat: 23`, `yoyo: true`, `none` (about `1.2 s`).
- **Tested:** Reel 03 S15.
- **Source:** `wahi-insaan-papercut/tools/build.py:738`–`754`.
- **Rules:** `<= 1.5 s`; only on a clock/alarm object; never on text.

### 36. point-slam — RESERVED

- **Does (planned):** a pointer/arrow hits a spot and slams it.
- **Status:** no implementation.
- **Closest tested parts:** `slam-in` on the pointer + `shake`.
- **Rules:** do not use until built and rendered.

---

## 4. Helper name map (builders)

Existing builders use shorter helper names. Map them to the menu before writing a card.

| Helper in code | Menu name |
|---|---|
| `pop` | `pop-in` |
| `slam` | `slam-in` |
| `punch` | `zoom-punch` |
| `shake`, `shakeEq` | `shake` |
| `flash` | `flash` |
| `draw` | `line-draw` / `draw-path` |
| `spin` | `orbit-dot` (only when used as an orbit) |
| `drift` | `parallax` |
| `stampit` | `stamp` |
| `fly` | `fly` |
| `reveal` | `reveal-mask` |
| `meter` | `count-up` |
| `cracks` | `crack` |
| `speed` | `speed-lines` |
| `glitch` | `glitch` |
| `wipejs` (paper) | `paper-wipe` |

---

## 5. How to add a new effect

Do this in the same session that writes or first uses the effect. Do not defer.

1. **Build it once** in a reel with real numbers.
2. **Render it** and check: `hyperframes lint`, `hyperframes check --json: ok`, snapshot at the
   effect's peak.
3. **Append an entry** at the end of section 3 with:
   - `name`
   - `Status: TESTED`
   - `Does` (one sentence)
   - `Target` (layer / element type)
   - `Params` (exact from → to, duration, ease, stagger, limits)
   - `Tested` (reel + scene)
   - `Source` (`file:line`)
   - `Rules` (safety limits)
4. **Update the index** in section 2 and the totals line.
5. **Update `ReelMasterprompt.md` section 2.1** only if the name is not already in the menu.
   Keep the two copies of `ReelMasterprompt.md` in sync.
6. **If a RESERVED effect is still unused,** leave it RESERVED. Do not promote it without a
   render.

### Template

```text
### N. <name> — TESTED

- **Does:** <one sentence>
- **Target:** <layer / element>
- **Params:** <from -> to>, <duration>, <ease>, <stagger/limits>
- **Tested:** <reel> <scene>
- **Source:** `<file>:<line>`
- **Rules:** <max values / safety>
```

---

## 6. Change log

| Date | Change |
|---|---|
| 2026-10-30 | Created. Imported 32 TESTED effects from Reels 02/03, planet-sabotage and chalkline. Marked `wipe` PARTIAL; `print-on`, `scroll-feed`, `point-slam` RESERVED. |
