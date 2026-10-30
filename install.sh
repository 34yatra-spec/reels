#!/usr/bin/env bash
# Reels installer — idempotent. Called by opencode after the system is installed.
set -uo pipefail

WORK="${WORK:-/kaggle/working}"
REELS="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
fail=0

if [ -f "$WORK/tools/bootstrap.sh" ]; then
  source "$WORK/tools/bootstrap.sh" >/dev/null 2>&1 || true
else
  echo "WARN: system toolchain missing — run /kaggle/working/system/install.sh first"
fi

if ! command -v yt-dlp >/dev/null 2>&1; then
  echo "[reels] installing yt-dlp"
  pip install -q yt-dlp || true
fi

chk() {
  local label="$1"; shift
  if "$@" >/dev/null 2>&1; then
    echo "  OK   $label"
  else
    echo "  MISS $label"
    fail=1
  fi
}

echo "[reels] verifying"
chk "yt-dlp"            command -v yt-dlp
chk "node 22.14.0"      bash -c 'node -v 2>/dev/null | grep -q v22.14.0'
chk "hyperframes 0.8.214" bash -c 'hyperframes --version 2>/dev/null | grep -q 0.8.214'
chk "chrome browser"    bash -c 'test -n "${HYPERFRAMES_BROWSER_PATH:-}" && test -x "$HYPERFRAMES_BROWSER_PATH"'
chk "ffmpeg"            command -v ffmpeg
chk "ffprobe"           command -v ffprobe
chk "python libs"       python3 -c 'import numpy, PIL, scipy, requests, soundfile, soxr'
chk "ReelProcedure.md"  test -f "$REELS/ReelProcedure.md"
chk "ReelMasterprompt.md" test -f "$REELS/ReelMasterprompt.md"
chk "COOKBOOK.md"       test -f "$REELS/COOKBOOK.md"
chk "template"          test -d "$REELS/_template"
chk "fonts"             bash -c "test -n \"\$(find '$REELS/_template/assets/fonts' -name '*.woff2' 2>/dev/null | head -n1)\""

if [ -n "${WORKER_TOKEN:-}" ]; then
  if curl -fsS -H "Authorization: Bearer $WORKER_TOKEN" \
       "https://gemini-gateway.31yatra.workers.dev/v1/capabilities" >/dev/null 2>&1; then
    echo "  OK   gateway reachable"
  else
    echo "  WARN gateway not reachable (token set)"
  fi
else
  echo "  WARN WORKER_TOKEN not set — gateway calls will fail"
fi

if [ "$fail" -ne 0 ]; then
  echo "[reels] MISSING items above"
  exit 1
fi
echo "[reels] OK"
