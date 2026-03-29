# Standup Siren

Tiny local tray app for Linux and macOS that plays dramatic intro music shortly before your team meeting.

## Goals

- local app, not web-hosted
- tiny codebase
- Linux + macOS
- open source under MIT
- built with Tauri + plain HTML/CSS/JS
- simple daily schedule
- starts with the computer and sits quietly until it's time

## MVP

- tray-first app with tiny preferences window
- set meeting time (daily)
- choose how many seconds before meeting to play (default: 10)
- bundled default dramatic sound
- optional power-user override via config dir ring file
- enable/disable launch on startup
- test sound button
- show next trigger time

## Architecture

- **Frontend:** tiny static HTML/CSS/JS settings UI
- **Shell:** Tauri with tray support
- **Scheduling:** lightweight JS timer with next-run calculation
- **Persistence:** small JSON config
- **Audio:** bundled default sound with config-dir override

## Why this stack

This keeps source size very small while still shipping native-ish local apps on macOS and Linux.

## License

MIT
