#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT_DIR"

# PyInstaller expects SOURCE:DEST on macOS and Linux.
# Only Windows uses a semicolon separator.
DATA_SEP=':'

uv run pyinstaller \
  --noconfirm \
  --clean \
  --windowed \
  --onedir \
  --name standup-siren \
  --paths "$ROOT_DIR" \
  --add-data "assets/default-ring.mp3${DATA_SEP}assets" \
  --collect-submodules pystray \
  --collect-all pystray \
  --collect-all PIL \
  run_standup_siren.py

echo
printf 'Built bundle: %s\n' "$ROOT_DIR/dist/standup-siren"
