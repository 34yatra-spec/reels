# Lessons Learnt — Reel 02 "Shani ka daur"

Date: 2026-10-29
Project: `Reel 02 shani-ka-daur`
Toolchain: `/kaggle/working/tools` (Node 22.14.0, HyperFrames 0.8.214, Chrome Headless Shell 152)

This file records what worked, what failed, and what to do next time.

## 1. Toolchain after a Kaggle restart

**Problem.** `/kaggle/working` restored the files, but the restore removed:
- the execute bit on `tools/node22/bin/node` and on `chrome-headless-shell`;
- the CLI symlinks in `tools/hf/node_modules/.bin/` (they became empty files or disappeared).

`source tools/bootstrap.sh` then printed `node v20.19.0 | hyperframes ` (empty version).

**Fix.**
```bash
chmod +x /kaggle/working/tools/node22/bin/node
chmod +x /kaggle/working/tools/chrome/chrome-headless-shell/linux-*/chrome-headless-shell-linux64/chrome-headless-shell
ln -sf ../hyperframes/bin/hyperframes.mjs /kaggle/working/tools/hf/node_modules/.bin/hyperframes
```

**Permanent fix.** `tools/bootstrap.sh` now self-heals the execute bits and the
`hyperframes` symlink on every source. `tools/firstsetup.md` was updated to match.

**Lesson.** Treat exec bits and symlinks as lost on every restore. Check them first,
before installing anything.

## 2. Gemini Gateway TTS (male Hindi)

- Use `POST /v1/tts` with `voice: "Charon"` for a calm male Hindi voice.
- Put delivery direction in `style`, not in `text`. The model did not speak the
  English style instruction (verified with STT).
- Generate the whole script in **one** request. This keeps one voice and one mood.
- Generate 2 takes. Check duration before listening. Take 1 was 56.17 s (good);
  take 2 was 88.57 s (too slow, discarded). Same text and style can give very
  different pacing.
- Gate: 56.0–59.5 s. Normalise to 48 kHz mono, then pad to the target.
- Trim leading silence so the first word starts within 0.1 s.

## 3. Word timing (the expensive lesson)

**Do not use Whisper `small` for Hindi word timing.**
- It took **8m43s** on a 56 s clip.
- The `--json` output was partly corrupted.
- It merged a 27 s span into one word, so most word times were unusable.

**Use this instead.**
1. Detect silence gaps with `ffmpeg silencedetect`.
2. Cut the audio at the gaps into speech chunks.
3. Send each chunk to Gemini `POST /v1/stt?lang=hi` (~2m20s for 41 chunks).
4. Map chunk text to script lines. The script text is the truth.
5. Place words inside each chunk by relative character weight.

This gave clean line boundaries (for example L2 starts at 4.43 s, not the 3.4 s
estimate in the scene cards).

## 4. HyperFrames authoring

- **Word spans must last to the scene end.** If `data-duration` ends at the next
  word, earlier words vanish. Set `duration = scene_end - word_start`.
- **`draw()` must handle SVG groups.** `getTotalLength()` exists only on `<path>`.
  Iterate `root.querySelectorAll('path')` when the target is a `<g>`.
- **Do not put Python helpers in JS.** `rel(...)` inside an f-string emitted
  `rel is not defined`. Compute times in Python and write numbers.
- **Tick/icon helpers need real `id`s.** Passing an id as `class` causes
  `GSAP target not found`.
- **Frame 0 must not be empty.** Start S01 at `0.0` and force the first word
  visible. Social players use frame 0 as the thumbnail.
- **Last frame should match frame 0.** For a seamless replay, overlay a
  full-screen copy of the frame-0 layout in the last 0.3 s.
- **Snapshot before render.** `hyperframes snapshot` took ~13 s and caught:
  missing words, figures overlapping card labels, and dots placed in the wrong card.
- `hyperframes check` took ~24 s and must return `ok: true`.

## 5. Verification used

- `hyperframes lint` → 0 errors (23 density warnings).
- `hyperframes check --json` → `ok: true`, runtime/layout/contrast/audio 0 errors.
- `hyperframes snapshot` → reviewed 14 key frames.
- `ffprobe` on the final MP4 → 1080×1920, 30 fps, 56.17 s, H.264 + AAC 48 kHz stereo.
- Loudness: −12.8 LUFS integrated, −1.2 dBTP.

## 6. Timings (task start 11:40:26 → final 12:05:18)

| Stage | Time |
|---|---|
| Gateway check + TTS tests + 2 full takes + normalise | 2m 05s |
| Transcription total | 12m 28s |
| — Whisper `small` (discarded) | 8m 43s |
| — Gemini chunk-STT (used) | 2m 20s |
| `beats.json` alignment | 1m 36s |
| Build 23 scenes + snapshots + fixes + final check | 6m 23s |
| Render (engine 1m 50s) | 2m 20s |
| **Total** | **24m 52s** |

Without the Whisper detour, the same reel should take about 16 minutes.

## 7. Reuse checklist

1. Source `tools/bootstrap.sh`; confirm `hyperframes --version` is 0.8.214.
2. Generate TTS with Charon in one request; check duration; normalise.
3. Silence-split, then Gemini STT per chunk. Skip Whisper.
4. Build `beats.json`; keep the script as the source of truth.
5. Build scenes; keep every word visible to scene end.
6. `lint` → `snapshot` → `check` → `render -q delivery -w 4`.
7. Verify the MP4 with `ffprobe`.

## 8. Tools change made

- `tools/bootstrap.sh`: restores execute bits on Node and Chrome, and recreates the
  `hyperframes` / `hyperframes-localize-fonts` symlinks.
- `tools/firstsetup.md`: documents the self-heal and adds a troubleshooting row.
