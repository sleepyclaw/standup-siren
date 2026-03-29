# TASKS.md — Standup Siren

Short execution checklist for future agents.
Update this file when priorities change or when a task is completed.

## Current priority order

### 1. Real tray prototype
- [ ] wire actual `pystray` icon lifecycle
- [ ] verify tray icon works in a real desktop session
- [ ] add basic menu entries: open settings, test sound, quit

### 2. Tiny settings UI
- [ ] add a small settings window
- [ ] edit meeting time
- [ ] edit seconds-before offset
- [ ] save config locally
- [ ] show next trigger time

### 3. Scheduler loop
- [ ] background loop computes next trigger
- [ ] play sound once per event/day
- [ ] avoid duplicate playback after wake/resume/restart
- [ ] expose useful verbose logs

### 4. Sound behavior
- [ ] keep bundled default sound
- [ ] support config-dir override at `~/.config/standup-siren/ring.mp3`
- [ ] handle missing/invalid override gracefully

### 5. Autostart
- [ ] Linux autostart support
- [ ] macOS autostart support

### 6. Packaging
- [ ] choose PyInstaller strategy
- [ ] add build config
- [ ] document build artifacts clearly

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
