# Standup Siren

Tiny local tray app for macOS and Linux that plays dramatic intro music shortly before your team meeting.

Standup Siren is intentionally small:
- no backend
- no account system
- no cloud dependency
- tray-first UX
- bundled default sound, with optional local override later

## Status

Early scaffold. The repo currently has the app shell and tray structure in place. Scheduler, persistence, sound playback, and autostart are being added incrementally.

## 1) Run locally

### Prerequisites

You need a normal Tauri development setup:
- Node.js 20+
- Rust stable toolchain
- Tauri system dependencies for your OS

Official setup docs:
- <https://v2.tauri.app/start/prerequisites/>

### Install dependencies

```bash
npm install
```

### Start in development mode

```bash
npm run dev
```

This should launch the app locally with the current tray/window scaffold.

## 2) Build locally

Build a local production bundle with:

```bash
npm run build
```

Tauri will produce platform-specific desktop artifacts.

## 3) How to use the built app / what artifacts Tauri provides

After a successful build, artifacts are produced under:

```bash
src-tauri/target/release/bundle/
```

Typical outputs depend on platform:

### macOS
Usually one or more of:
- `.app`
- `.dmg`

### Linux
Usually one or more of:
- `.deb`
- `.AppImage`
- executable bundle output depending on installed tooling

You can install/open the artifact for your platform and then run Standup Siren like a normal desktop app.

## Planned behavior

MVP target:
- tray-first app
- tiny preferences window
- daily meeting time
- configurable offset in seconds
- bundled default dramatic sound
- optional config-dir override for custom sound
- local config persistence
- launch on login
- show next trigger time
- test sound button

Later:
- local `.ics` calendar import
- event title matching
- releases and tiny download landing page

## Sound override plan

Default users should not need to configure anything.

Later, advanced users will be able to override the bundled sound by placing a file such as `ring.mp3` in the app config directory.

## Development notes

- Keep dependencies small.
- Keep frontend minimal.
- Prefer simple local logic over complicated integration.
- Test locally before pushing.

## License

MIT
