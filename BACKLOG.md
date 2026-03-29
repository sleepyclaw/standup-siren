# TASKS.md — Standup Siren

Short execution checklist for future agents.
Update this file when priorities change or when a task is completed.

## Current priority order

### 1. Real tray prototype
- [x] wire actual `pystray` icon lifecycle
- [ ] verify tray icon works in a real desktop session
- [x] add basic menu entries: open settings, test sound, quit

### 2. Tiny settings UI
- [x] add a small settings window
- [x] edit meeting time
- [x] edit seconds-before offset
- [x] save config locally
- [x] show next trigger time

### 3. Scheduler loop
- [x] background loop computes next trigger
- [x] play sound once per event/day while app remains running
- [ ] avoid duplicate playback after wake/resume/restart
- [x] expose useful verbose logs

### 4. Sound behavior
- [ ] keep bundled default sound
- [ ] support config-dir override at `~/.config/standup-siren/ring.mp3`
- [ ] handle missing/invalid override gracefully

### 5. Autostart
- [ ] Linux autostart support
- [ ] macOS autostart support

### 6. Packaging
- [x] choose PyInstaller strategy
- [x] add build config
- [x] document build artifacts clearly
- [x] smoke-test packaged binary in headless `--self-test` mode
- [ ] validate packaged tray app in a real desktop session

### 7. Calendar follow-up
- [ ] design local `.ics` import flow
- [ ] match events by title
- [ ] keep it local-only for MVP+

## Known constraints
- Debian 11 compatibility matters
- avoid Tauri unless compatibility situation materially changes
- keep dependencies small
- keep commits incremental and visible on GitHub

## Done recently
- [x] repo pivoted from Tauri to Python prototype
- [x] switched Python workflow to `uv`
- [x] added agent-oriented project handoff in `AGENTS.md`
