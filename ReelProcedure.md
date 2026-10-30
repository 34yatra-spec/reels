# Reel Procedure — RP-1

Status: active
Name to call: **RP-1** (or "Reel Procedure")
Owner: the same agent (director + builder)
Use when: "make a reel", "run RP-1", "follow the reel procedure"

This is the named pipeline for one reel. It is **not** `/kaggle/working/PIPELINE.md`.
Do not use the old master pipeline unless the user explicitly asks for it.

---

## 0. One-line summary

**Input → script → Gemini voice → word beats → scene cards → HyperFrames build → check → render → timing report.**

---

## 1. Inputs the user may give

Any one of these is enough to start:

| Input | What the agent does |
|---|---|
| A link (YouTube, Instagram, article) | Download it, extract audio, transcribe, then write an improved script |
| An audio/video file | Transcribe, then write an improved script |
| A topic or idea | Write the script from the topic |
| A finished script | Skip writing; go to voice |
| Storyboard / scene cards | Use them as the build source; do not invent new scenes |
| A master prompt | Read `ReelMasterprompt.md`; use it at stage 5 to generate scene cards |

Ask only for what is missing. Defaults:

- Language: Hindi
- Length: 55–60 s
- Voice: male, Gemini `Charon`
- Look: light theme (`#F7F4EE`), 1080×1920, 30 fps
- Output: `renders/<slug>-final.mp4`

---

## 2. Stages

| # | Stage | Output | Target time |
|---|---|---|---|
| 0 | Intake | confirmed brief | 1 min |
| 1 | Acquire | source audio + transcript | 2–10 min |
| 2 | Script | `script.md` | 5–10 min |
| 3 | Voice | `assets/hi-voice.wav` | 2–4 min |
| 4 | Timing | `beats.json` | 3–5 min |
| 5 | Scene cards | `scenes.md` | 5–15 min |
| 6 | Build | `index.html` + `compositions/` | 10–20 min |
| 7 | Verify | lint + snapshots + `check --json` | 3–5 min |
| 8 | Render | final MP4 | 2–3 min |
| 9 | Report | timings + paths + checks | 1 min |

---

## 3. Stage details

### Stage 0 — Intake

Confirm only: language, length, voice, look, and whether the user already has a script
or scene cards. If the user gave a storyboard, do not replace it.

### Stage 1 — Acquire

If the user gives a link:

```bash
pip install -q yt-dlp          # if missing
yt-dlp -x --audio-format wav -o audio/source.%(ext)s "<link>"
```

If the link cannot be downloaded, ask for the file. Do not guess content.

Transcribe with the Gemini Gateway:

```bash
curl -s -X POST "$BASE/v1/stt?lang=hi" \
  -H "Authorization: Bearer $TOKEN" \
  -H "content-type: audio/wav" \
  --data-binary @audio/source.wav
```

Decide the audio:

- Keep the source audio if it is clean and in the right voice.
- Otherwise generate a new voice with Gemini TTS (stage 3).

Record the decision in one line in the project notes.

### Stage 2 — Script

Write an improved version of the source. Keep the meaning; improve the hook, pace,
and ending. For a 55–60 s reel use about 14–16 lines.

Required structure:

1. Hook in the first 3 s.
2. Reason / turn in layers.
3. Self-test or recognition beat.
4. Payoff.
5. One clear send/save ask.

If the topic is astrology, add the on-screen line
`ज्योतिष मान्यता पर आधारित` and promise no results.

Save:

- `script.md` — lines, meaning, timing estimate, voice direction.
- `audio/script_lines.txt` — one line per script line, exactly as spoken.

**The script text is the truth. Transcription only gives times.**

### Stage 3 — Voice

Use the Gemini Gateway. Put the delivery direction in `style`, not in `text`.

```bash
POST /v1/tts
{"text": "<full script>", "voice": "Charon", "style": "<direction>"}
```

Rules:

- One request for the whole script. This keeps one voice and one mood.
- Generate 2 takes. Check duration before choosing.
- Duration gate: 56.0–59.5 s. Discard outliers.
- Output 24 kHz is fine; normalise to 48 kHz mono.
- Trim leading silence so the first word starts within 0.1 s.
- Save as `assets/hi-voice.wav`.

Normalise:

```bash
ffmpeg -i take.wav -af "silenceremove=start_periods=1:start_threshold=-50dB,loudnorm=I=-14:TP=-1.5:LRA=11" -ar 48000 -ac 1 assets/hi-voice.wav
```

### Stage 4 — Timing

**Do not use Whisper for Hindi.** It is slow and inaccurate.

Use this method:

1. `ffmpeg silencedetect` → speech chunks.
2. Send each chunk to Gemini `/v1/stt?lang=hi`.
3. Map chunk text to script lines.
4. Place words inside each chunk by relative character weight.
5. Write `beats.json` with every word's start and end.

Reusable script: `_template/tools/make_beats.py`.

### Stage 5 — Scene cards

Two paths:

**A. The user gave storyboard / scene cards.** Use them. Do not rewrite the story.
Validate them against the build rules below.

**B. The user gave no scenes.** Run the master prompt with the extracted script:

```bash
POST /v1/llm
{"prompt": "<contents of ReelMasterprompt.md>\n\nSCRIPT:\n<script>"}
```

The master prompt lives at `ReelMasterprompt.md`.
If that file is empty, use the Reel 02 scene shape
(hook → problems → reveal → self-test → remedy → payoff → send) and read
`_template/compositions/` for the implemented recipes.

Every scene card must name:

- scene id and start word (line id + first word);
- what is on screen;
- the visual recipe used;
- the key word and its colour;
- the second visible change (micro-beat) for any scene longer than 2.0 s.

Validate before build:

- every start word exists in `beats.json`;
- on-screen text uses only script words plus the disclaimer;
- light background, no black frames;
- nothing outside the safe zone;
- one scene per card.

Save as `scenes.md`.

### Stage 6 — Build

Copy the Reel 02 builder as the starting point:

```bash
cp _template/tools/build.py tools/build.py
```

Adapt it to the new `beats.json` and scene cards.

HyperFrames rules that must hold:

- 1080×1920, 30 fps.
- Root `data-duration` = audio length + 0.1 s.
- One `scene-NN.html` per card; mount from `index.html` with `data-composition-src`.
- Every word span: `class="clip"`, `data-start`, `data-duration` to **scene end**.
- `window.__timelines["scene-NN"]` registered; `TL.seek(0)`.
- Visuals in `.cam`; text, badge, disclaimer outside `.cam`.
- Frame 0 must not be empty; the last frame should match frame 0 for replay.
- Use only the recipes in the scene cards. If a scene needs a new recipe, stop and report.

### Stage 7 — Verify

```bash
hyperframes lint
hyperframes snapshot -o snapshots --at <key times>
hyperframes check --json
```

Pass conditions:

- lint: 0 errors.
- `check`: `ok: true`; runtime/layout/contrast/audio 0 errors.
- snapshots: text readable, no overlap, frame 0 and last frame correct.

Fix once. Re-check once. Do not render to make a decision.

### Stage 8 — Render

```bash
hyperframes render -o renders/<slug>-final.mp4 -q delivery -w 4
```

Verify:

```bash
ffprobe -v error -show_entries format=duration,size -show_entries stream=codec_name,width,height,r_frame_rate,channels -of json renders/<slug>-final.mp4
```

### Stage 9 — Report

End with:

- output path and specs;
- what passed and what did not;
- a timing table: TTS, transcription, build, check, render, total.

---

## 4. Guardrails

1. **Do not use `/kaggle/working/PIPELINE.md`** unless the user asks.
2. **All LLM / TTS / STT goes through the Gemini Gateway.**
3. **No Whisper for Hindi.** Use chunk-STT + script alignment.
4. **Script text is the truth.** STT gives times only.
5. **Word spans last to scene end.** Otherwise earlier words vanish.
6. **Frame 0 is the thumbnail.** It must show the hook, not an empty background.
7. **Ask when the brief is ambiguous** (voice, length, theme, whether to keep source audio).
8. **Record lessons** in `lessons learnt.md` after the render.

---

## 5. Reuse assets

| Asset | Path |
|---|---|
| Builder template | `_template/tools/build.py` |
| Beat builder | `_template/tools/make_beats.py` |
| Lessons | `_template/lessons learnt.md` |
| Fonts | `_template/assets/fonts/` |
| Toolchain bootstrap | system repo tools/bootstrap.sh |
| Master prompt | `ReelMasterprompt.md` |

---

## 6. Timing log format

| Stage | Time |
|---|---|
| Intake + acquire | |
| Script | |
| TTS + normalise | |
| Transcription | |
| Beats | |
| Scene cards | |
| Build + snapshots + check | |
| Render | |
| **Total** | |
