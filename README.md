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
- real tray app skeleton with menu entries
- tiny Tk settings window for meeting time + offset
- background scheduler loop that updates next trigger text
- PyInstaller-based Linux/macOS bundle build script
- packaged binary smoke-tested in `--self-test` mode

For contributor/internal project context, see `AGENTS.md` and `BACKLOG.md`.

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

Packaging now uses PyInstaller via `uv`.

Build a bundle:

```bash
uv sync
./scripts/build_bundle.sh
```

Expected output directory:

```bash
dist/standup-siren/
```

Main executable:

```bash
dist/standup-siren/standup-siren
```

Smoke-test the built binary without launching the tray UI:

```bash
./dist/standup-siren/standup-siren --self-test --verbose
```

## 3) How to use the built app / expected artifacts

Current build artifact:

### Linux
- standalone folder bundle from PyInstaller at `dist/standup-siren/`
- launch with `./dist/standup-siren/standup-siren`

### macOS
- same PyInstaller-driven build path is intended
- `.app` packaging is not wired yet in this commit

Notes:
- the bundled default ring is included inside the build output
- packaged `--self-test` mode was verified in headless context
- actual tray behavior still needs validation in a real desktop session

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
