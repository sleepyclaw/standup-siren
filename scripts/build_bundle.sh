#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT_DIR"

case "$(uname -s)" in
  Darwin)
    DATA_SEP=';'
    ;;
  *)
    DATA_SEP=':'
    ;;
esac

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
