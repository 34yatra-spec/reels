# Master Prompt Pack — RP-1, Stage 5

Status: **active**
Owner: director agent (same agent as builder)
Used by: `ReelProcedure.md`, stage 5
Called with: `POST /v1/llm` on the Gemini Gateway, with the script and beats appended
Output: one JSON object (`treatment`, `scenes`, `needs_effects`), later rendered to `scenes.md` by code

This is the director prompt pack. Gemini designs the reel from a script; opencode runs the
pipeline and builds it. Claude is not in the loop at run time. No house style: the script
decides the visual world.

---

## 0. Decisions

- **Gemini decides:** the visual world (style), the palette and mood per block, the motif,
  the native move, the effects (from a menu), the layout (template names), and which
  real-object cutouts are worth using.
- **Code decides:** pixel boxes, timing, and whether the output is valid. A language model
  places things badly in pixels. So Gemini picks layout names and slot names. Code turns
  them into boxes and checks overlaps.
- **Examples: yes, but not the full Reel 03.** One example anchors the model to one style.
  So the prompt carries two short examples in two different styles, marked as format and
  quality bar only. A list of past reels (style and motif of each) is passed in so the new
  reel must differ.
- **Script:** the user gives it. The optional script check (P0) only reports problems. It
  does not rewrite.
- **No fixed house style.** The old light-theme palette (`#F7F4EE`, indigo/gold/red) is not
  a rule for new reels. It is only the fallback when a reel is explicitly built in the
  Reel 02 shape.

### Runtime reality (Gemini Gateway)

The gateway `/v1/llm` endpoint returns **text only**. It has no `responseSchema`,
`response_format`, or thinking-level field.

- Ask for JSON inside one fenced `json` block, then parse and validate it in code.
- If parsing fails, retry once with the same prompt plus the parse error. Then stop and report.
- Do not assume the model can be forced into a schema. The schema is enforced by the
  validator (section 11), not by the API.
- Pin the model with an id from `GET /v1/capabilities` (or `GET /v1/upstream/models`). Do not
  hardcode a model id in this file.
- Temperature: leave at the default **1.0**. Lower values can cause looping or worse results
  on Gemini 3.
- Thinking level: high for P1, P2 and P4; low for P3. Use it only if the gateway exposes it;
  otherwise ignore this line.

### Files this pack assumes

| File | Purpose | Status |
|---|---|---|
| `COOKBOOK.md` | tested numbers for every effect name | present (2026-10-30); 32 TESTED, 3 RESERVED |
| `<project>/beats.json` | every word's start/end (stage 4) | produced by RP-1 |
| `PAST_REELS.md` | style world, motif, palette of past reels | create with the first finished reel |
| `<project>/script.md` | script with line IDs | produced by RP-1 |

If `COOKBOOK.md` is missing, the pipeline may run P1/P2 but must not render. Stop before
stage 6 and report the missing effect numbers.

---

## 1. Pipeline

| Step | Who | Input | Output |
| --- | --- | --- | --- |
| P0 Script check (optional) | Gemini | script | list of problems and a score |
| P1 Treatment | Gemini | script, beats, past reels, menus, examples | treatment JSON |
| P2 Scene cards | Gemini | + treatment | scene-cards JSON |
| V Validate | code | cards | error list |
| P3 Fix | Gemini | cards + errors | corrected cards (up to 3 loops) |
| P4 Critic | Gemini | script, treatment, cards | scores and required fixes. One revise pass. |
| R Render | code | JSON | scene-card Markdown for the builders, `assets.json` for the asset agent |

**Default stage-5 call:** run P1 + P2 in one request using the prompt in section 7. The
response envelope carries both. Use separate P1/P2 calls only when the single call is too
long or the model drops part of the design.

**Strict mode:** P1, then P2, then V, then P3 (max 3 loops), then P4 (one revise pass).
Never skip V.

Validator rules (code): every script word is covered once; start words exist in
`beats.json`; scene length 0.5–4.0 s; scenes over 2.0 s have a second beat; every effect is
in the cookbook; every layout and slot exists; every overlap is declared and within the law;
at most 14 distinct cutouts; no effect in more than 2 consecutive scenes.

---

## 2. Menus the code injects

### 2.1 Effect names (numbers live in `COOKBOOK.md`)

`pop-in`, `slam-in`, `fade`, `bounce`, `wobble`, `push-in`, `parallax`, `zoom-punch`,
`shake`, `flash`, `glitch`, `speed-lines`, `wipe`, `paper-wipe`, `reveal-mask`, `line-draw`,
`draw-path`, `strike`, `highlighter`, `stamp`, `type-on`, `print-on`, `scroll-feed`,
`count-up`, `fly`, `walk`, `orbit-dot`, `stack-bricks`, `crack`, `tick-stamp`, `wilt`,
`snip`, `loop-cut`, `flag-drop`, `alarm-shake`, `point-slam`.

If none fits, Gemini returns `NEEDS_EFFECT` with a description. A human adds the effect to
the cookbook once, with tested numbers.

### 2.2 Layouts (code resolves slots to boxes; STAGE is x 60–1020, y 260–1090)

| Layout | Slots (x, y, w×h) |
| --- | --- |
| L-HERO | hero (240, 340, 600×700) |
| L-DUO | left (80, 420, 440×620); right (560, 420, 440×620) |
| L-TRIO | a (60, 480, 300×520); b (390, 480, 300×520); c (720, 480, 300×520) |
| L-ROW4 | s1–s4 at x 80, 320, 560, 800; y 560; 200×300 |
| L-HERO-SIDE | hero (80, 340, 560×700); side (680, 560, 340×420) |
| L-COLUMNS | tall (140, 300, 300×740); top-right (500, 320, 480×340); bottom-right (500, 700, 480×340) |
| L-FRAME | hero (270, 400, 540×600); c1 (60, 280, 200×200); c2 (820, 280, 200×200); c3 (60, 880, 200×200); c4 (820, 880, 200×200) |
| L-STACKED | top (140, 280, 800×380); bottom (140, 700, 800×380) |
| L-RING | ring (240, 340, 600×600); in-a (340, 480, 180×320); in-b (560, 480, 180×320) |
| L-FULL | back (60, 260, 960×830); accent (700, 300, 300×300) |

Ground line for standing things: y 1040. Text plate: (90, 1140, 900×280). Disclaimer: y 1470.

### 2.3 Merge treatments (pick one primary per reel, then grade per block)

`die-cut(width)` white sticker edge · `shadow(dx, dy, blur, alpha)` ·
`duotone(shadow, highlight)` · `grade(color, alpha)` · `halftone(size)` ·
`outline(ink, width)` · `grain(alpha)` · `flat-vector` (no photo cutouts at all).
One light direction for the whole reel.

### 2.4 Asset rules

1. Use a real-object cutout only when a real object adds feel that code shapes cannot (a
   rose, a clock, a notebook, scissors). People are always silhouettes, paper figures or
   code figures. Never recognisable faces.
2. No logos, brands, characters, or design-protected products (phones, laptops, branded
   furniture). Draw those in code.
3. Free sources only, no image API: Openclipart (CC0), SVGRepo (CC0 filter), Pixabay
   (objects only), Wikimedia Commons and NASA (public domain, check each file page). No
   site that needs attribution. No bulk download.
4. At most 14 distinct cutouts. Reuse them across scenes. Each needs a code fallback.
5. Each cutout gets the primary merge treatment.

### 2.5 Layer and overlap law

Layers: z0 backdrop · z1 set pieces · z2 mid · z3 hero · z4 FX · z5 text plate and text · z6 chrome.

- Only the plate and text enter y 1130–1440.
- Same-layer elements never overlap unless the card says `merge`.
- Different-layer elements overlap only if the card declares the pair. The covering element
  covers 25 % or less of the covered one, and never its key part.
- `ground` elements (floor, tape, shadow) can be covered fully.
- FX strokes are 8 px or less and cover at most 10 % of a hero.
- A hero fills at most 55 % of STAGE.

---

## 3. SYSTEM (all calls)

```text
You are the art director and scene designer for 60-second vertical reels (1080x1920, 30 fps, 2D motion graphics built in HyperFrames). You never write code. You decide what the viewer sees, scene by scene, so a builder can follow your cards exactly.

PRINCIPLES
- The script decides the style. Read its topic, emotion and audience. There is no house style. Each reel gets its own visual world.
- Every reel has one idea, one open loop in the first 3 seconds, one payoff image, one repeating motif whose meaning changes, and one native move: a moment only motion can do.
- Each scene has one primary motion. Other elements only react to it.
- Each visual adds meaning the words do not already give. Reject the obvious icon. Choose an image from the script's own world.
- Something visible changes every 1 to 2.5 seconds.
- Emotion moves the palette. Each block of the script gets its own backdrop and mood. One merge treatment holds mixed assets together.
- Use a real-object cutout only when a real object adds feel that code shapes cannot. Follow the asset rules.
- You choose layout names and slot names. You never write pixel positions.
- You choose effects from the menu only. If none fits, return NEEDS_EFFECT with a description.
- On-screen text uses the script's own language and exact words.
- Show claims about astrology, health or money as belief or tradition. No promised results. No fear language.

Follow the output schema exactly.
```

---

## 4. P0 Script check (optional)

```text
<SCRIPT>{script with line IDs}</SCRIPT>
<DURATION>{seconds}</DURATION>

TASK: Check this script for a vertical reel. Score 1-5 each: hook in the first 3 seconds, one clear idea, open loop and payoff, relatable specifics, a reason to send it to someone, spoken rhythm (short lines), honesty of claims. List every line with a problem and say why. Do not rewrite the script.
Do not praise. Do not invent facts.
```

---

## 5. P1 Treatment

```text
<SCRIPT>{script with line IDs}</SCRIPT>
<BEATS>{line start/end seconds, total duration}</BEATS>
<PAST_REELS>{for each past reel: style world, primary motif, palette}</PAST_REELS>
<MENUS>{effect names, layouts, merge treatments, asset rules}</MENUS>
<EXAMPLES>{section 13, marked FORMAT AND QUALITY BAR ONLY}</EXAMPLES>

TASK: Write the treatment for this reel. Study the emotion and audience of the script. Propose three different visual worlds (medium, palette logic, motion character) and choose one with reasons. Split the script into emotional blocks. Give each block a mood, a backdrop and accents. Choose one merge treatment. Decide the motif, the native move, the payoff image, and two obvious visuals you reject. Plan the cutouts: object, scenes, why a real object beats code, search query, must-have, code fallback.
Do not copy the style, palette or motif of any example or past reel. Do not use photos of people.
```

---

## 6. P2 Scene cards

```text
<SCRIPT>{script with line IDs}</SCRIPT>
<BEATS>{...}</BEATS>
<TREATMENT>{output of P1}</TREATMENT>
<MENUS>{...}</MENUS>
<EXAMPLES>{section 13}</EXAMPLES>

TASK: Design every scene of the reel. Cover every script word exactly once. Use between {duration/3.0} and {duration/1.8} scenes. Each scene starts at a start word (line ID, word, occurrence). Give each scene a visual job, a layout, its elements with slots and layers, the effects with word anchors, the overlaps you declare, a transition, and a check frame. Add a second beat to any scene longer than 2 seconds. Vary layouts and effects. Keep the motif and the native move from the treatment.
Do not write pixel positions. Do not invent effect names. Do not use more than 14 cutouts. Do not repeat an effect in more than 2 consecutive scenes. Do not copy the examples.
```

---

## 7. Stage-5 single call (default)

Use this when stage 5 has one gateway call. Put the long data first; put the task and the
negative constraints last. The response is one JSON object with three keys: `treatment`,
`scenes`, `needs_effects`.

```text
<SCRIPT>{script with line IDs, exactly as spoken}</SCRIPT>
<BEATS>{every line with start/end seconds and total duration}</BEATS>
<PAST_REELS>{for each past reel: style world, primary motif, palette}</PAST_REELS>
<MENUS>{effect names, layouts, merge treatments, asset rules, layer and overlap law}</MENUS>
<EXAMPLES>{section 13, marked FORMAT AND QUALITY BAR ONLY}</EXAMPLES>
<SCHEMAS>{section 10 schemas, including the treatment/scenes/needs_effects envelope}</SCHEMAS>

TASK: Design the whole reel in one pass, treatment first, then every scene. Return one JSON object with exactly three keys: treatment, scenes, needs_effects.

Cover every script word exactly once. Use between {duration/3.0} and {duration/1.8} scenes. Each scene starts at a start word (line ID, word, occurrence). Give each scene a visual job, a layout, its elements with slots and layers, the effects with word anchors, the overlaps you declare, a transition, and a check frame. Add a second beat to any scene longer than 2 seconds. Vary layouts and effects. Keep the motif and the native move from the treatment.

Return only a fenced json block. No prose before or after. No comments. No trailing commas.

Do not copy the style, palette or motif of any example or past reel. Do not write pixel positions. Do not invent effect names. Do not use more than 14 cutouts. Do not repeat an effect in more than 2 consecutive scenes. Do not use photos of people. Do not copy the examples.
```

On a parse failure, retry once with the same prompt plus `PARSE ERROR: <error>`. On a second
failure, stop and report.

---

## 8. P3 Fix

```text
<CARDS>{current scene-cards JSON}</CARDS>
<ERRORS>{validator errors}</ERRORS>

TASK: Return the full corrected cards. Change only what the errors require.
Do not change the style, the motif or the scene order.
```

---

## 9. P4 Critic

```text
<SCRIPT>...</SCRIPT>
<TREATMENT>...</TREATMENT>
<CARDS>...</CARDS>
<PAST_REELS>...</PAST_REELS>

TASK: Score the design 1-5 on each item, with evidence from the cards: (1) hook and motion by frame 3; (2) style follows the script, not a default; (3) visuals add meaning (list scenes where the picture only repeats the words); (4) variety of layouts and effects; (5) rhythm and second beats; (6) motif appears 3 or more times and changes meaning; payoff image is last; (7) native move is present and earned; (8) palette follows emotion and the merge treatment is coherent; (9) cutout discipline; (10) overlap and text-zone safety; (11) honesty and safety; (12) differs from past reels. Verdict PASS if no score is below 3 and the average is 3.8 or more. Otherwise REVISE, with a list of required fixes naming scene IDs.
Do not praise. Do not rewrite the cards.
```

---

## 10. Output schemas

The gateway returns text, so these schemas are instructions plus validator contracts, not
API-enforced JSON Schema. Require the fenced `json` block. Reject unknown effect, layout
and slot names. Use the field names exactly; never append a type annotation to a key.
Every key is a quoted JSON string.

**Envelope (single call)**

```text
{ "treatment": Treatment, "scenes": Scene[], "needs_effects": NeedsEffect[] }
```

**Treatment**

```text
viewer: string
feeling_at_second_0 (string)
one_idea: string
open_loop: string
payoff_image: string
candidate_worlds: 3 x { name, medium, palette_logic, motion_character, fit_reason }
chosen_world: { name, why, why_not_the_others }
blocks: [ { id, lines[], mood, backdrop, accents[], transition_in } ]
merge_treatment: { primary, params, why }
motif: { object, how_its_meaning_changes }
native_move: { "line", "description" }
rejected_obvious_visuals: 2 x { visual, why }
cutout_plan: [ { asset_id, object, scenes[], why_real_object, search_query, must_have, code_fallback } ]
risks: [string]
```

**Scene cards**

```text
scenes: [ {
  id, block_id,
  start_word: { line, word, occurrence },
  text_on_screen,
  visual_job: enum(hook, problem, reveal, proof, contrast, list, turn, payoff, cta, loop),
  layout: enum(layout names),
  elements: [ { id, kind: enum(code, cutout, text, fx), asset_id?, slot, layer: enum(z0..z6), note } ],
  overlaps: [ { over, on, reason } ],
  beats: [ { at: { line, word, occurrence }, effect: enum(effect names | NEEDS_EFFECT), target, params, note } ],
  wobble: boolean,
  transition_out,
  check_frame: { at_seconds_from_scene_start, expect }
} ]
needs_effects: [ { name, description } ]
```

---

## 11. Validation (code)

After every Gemini call that returns cards:

1. The fenced block parses as JSON and matches the envelope.
2. Every script word is covered exactly once, in order.
3. Every `start_word` exists in `beats.json` (line, word, occurrence).
4. Scene length is 0.5–4.0 s, measured from its start word to the next scene's start word.
5. Scenes longer than 2.0 s have at least a second beat.
6. Every effect in `beats` exists in `COOKBOOK.md` with `Status: TESTED`; `NEEDS_EFFECT` and RESERVED effects block build.
7. Every `layout` and every `slot` exists in section 2.2.
8. Every overlap is declared and obeys the layer and overlap law (section 2.5).
9. At most 14 distinct `asset_id` cutouts.
10. No effect appears in more than 2 consecutive scenes.
11. Text on screen uses only script words plus the disclaimer.
12. Nothing outside STAGE except the text plate, disclaimer and chrome.

On errors: run P3 with the error list. Max 3 loops. Then stop and report.

---

## 12. Render JSON to `scenes.md` (code)

The builder consumes Markdown scene cards. Code converts the validated JSON. Keep the
existing card fields so stage 6 does not change.

| `scenes.md` field | Source |
|---|---|
| `id` | `scenes[].id` |
| `start` | ``L{start_word.line} "{start_word.word}"`` |
| `on screen` | `layout` + element notes + visual job, one line |
| `recipe` | the first beat's `effect` (or the primary effect when several share a word) |
| `key word` | the first beat's `target` (the accent word) |
| `micro-beat` | the second beat, or `—` when the scene is 2.0 s or shorter |
| `text` | `text_on_screen` |

Also write `assets.json` from `treatment.cutout_plan`, with `asset_id`, object, source query,
must-have and code fallback. Pass both to the builder. Do not pass raw model prose.

---

## 13. Examples (format and quality bar only)

The pipeline shows these as rendered cards. They show how much detail and specificity to
give. They are not styles to reuse.

**Example A – topic: a stuck relationship pattern. World: paper-cut collage, die-cut edges, scenes change palette with emotion.**

- *Scene 08 · job: contrast · layout L-HERO · block Cold.* Text: “You think: this is just my luck.” Elements: z3 cutout rose (hero), z4 fx petals. Beats: at “luck” `wilt` the rose around the stem base, 6 petals fall; the rose loses 30 % saturation. Why this image: the same rose bloomed in scene 03, so the viewer sees the same object lose its life.
- *Scene 14 · job: proof · layout L-TRIO.* Text: “what you let pass the first time.” Elements: z2 three red flags (cutout) that grow in size. Beats: three `flag-drop` on the three nouns, `zoom-punch` on the smallest at “first time”. Others dim to 40 %. Check frame at 1.0 s: flag 1 is largest on screen.
- *Scene 21 · job: turn · layout L-RING.* Text: “When you change,”. Elements: z1 paper ring (motif), z3 scissors cutout (open), z3 figure. Beats: at “change” `snip`, the ring opens. Native move of the reel.

**Example B – topic: why salary is gone by the 20th. World: thermal receipt tape, monochrome with one red stamp, no photo cutouts (`flat-vector`).**

- *Scene 01 · job: hook · layout L-FULL.* Text: “Salary credited: 60,000.” Elements: z1 beige backdrop, z3 receipt strip (code), z4 red stamp. Beats: `print-on` line by line at 0.1 s each from frame 0; `stamp` “CREDITED” in red at the number.
- *Scene 05 · job: reveal · layout L-STACKED.* Text: “Small things. Every day.” Elements: z3 receipt strip top, z3 running total bottom. Beats: `scroll-feed` the strip at speed while `count-up` the total from 0 to 24,500. Check frame at 1.2 s: total is above 12,000.
- *Scene 09 · job: payoff · layout L-HERO.* Text: “The receipt is longer than the month.” Beats: the strip reaches the floor and spills over the bottom of the stage, `push-in`. Native move: the receipt becomes longer than the screen.

---

## 14. Test plan

1. Run the whole pipeline on 3 scripts of different topics and moods (for example astrology, money, fitness).
2. For each, check: is the style different from the other two? Is any motif reused? Does every scene add meaning beyond the words? Does the validator pass within 3 loops? Does the critic pass on the second try?
3. Render the first scene of each with the builder to catch layout problems early.
4. Keep the best design of each test in `PAST_REELS.md`.

---

## 15. Limits and open items

- **`COOKBOOK.md` exists (2026-10-30).** 32 effects are TESTED. `print-on`, `scroll-feed` and
  `point-slam` are RESERVED: do not use them, and stop and report if a card needs one.
- **No schema enforcement at the gateway.** JSON is requested as text and validated in code.
  If the gateway later adds `responseSchema`, move the schemas in section 10 there unchanged.
- **Thinking levels are not exposed** by the current gateway. Use the strongest free Flash
  model and temperature 1.0.
- **Free-tier terms** may let Google use inputs and outputs to improve its models. Scripts for
  public reels are fine. Do not send private client material.
- **The examples are a quality bar, not a style.** Never copy their palette, motif or medium.
- **Astrology, health and money** are shown as belief or tradition, never as promised results
  or fear. For astrology, keep the on-screen disclaimer used by RP-1.
