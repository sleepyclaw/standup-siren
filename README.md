# Standup Siren

Tiny local tray-style app for Linux and macOS that plays dramatic intro music shortly before your team meeting.

This project is now targeting a Debian-11-friendly Python implementation instead of Tauri, because current Tauri Linux requirements are a bad fit for Bullseye.

## Status

Prototype in progress.
Current repo state includes:
- config handling
- scheduler logic
- bundled default ring
- headless self-test mode
- early Python app scaffold

Tray GUI wiring is the next step.

## 1) Run locally

### Debian 11 / Linux prerequisites

```bash
sudo apt-get update && sudo apt-get install -y \
  python3-venv python3-pip python3-tk python3-pil python3-pil.imagetk \
  python3-gi python3-gi-cairo gir1.2-gtk-3.0 libcairo2-dev \
  libgirepository1.0-dev ffmpeg
```

### Create env and install Python deps with uv

```bash
uv sync
```

### Run headless self-test

```bash
uv run standup-siren --init-config
uv run standup-siren --self-test --verbose
```

### Test sound playback

```bash
uv run standup-siren --test-sound --verbose
```

## 2) Build locally

Planned packaging path: PyInstaller driven via `uv`.

Packaging config is not finalized yet in this commit, but development now uses `uv` instead of pip/venv instructions.

## 3) How to use the built app / expected artifacts

Planned artifacts:

### macOS
- `.app`
- possibly `.dmg` later

### Linux
- standalone folder bundle from PyInstaller
- one-file build optional later if it behaves well

## Config

Config file:

```bash
~/.config/standup-siren/config.json
```

Custom sound override path:

```bash
~/.config/standup-siren/ring.mp3
```

If no override exists, the bundled default ring is used.

## License

MIT
