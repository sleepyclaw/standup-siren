# AGENTS.md — Standup Siren Project Handoff

This file is for future agents working on this repository.
It explains what the app is, why the stack changed, what constraints matter, and what to do next.

## Maintenance rule for future agents

This file is **not static**.
If you work on the project, you should update `AGENTS.md` when any of the following changes:

- architecture decisions
- stack choices
- platform constraints
- confirmed build/runtime behavior
- important user preferences
- current status / next recommended steps
- known traps, mistakes, or dead ends

Think of `AGENTS.md` as the handoff brain for the repo.
Do not leave critical context trapped only in chat history or your own head.

When you finish meaningful work, update this file briefly so the next agent can continue with minimal archaeology.

## What this project is

**Standup Siren** is a tiny local desktop utility that plays dramatic intro music shortly before a daily team meeting.

Core idea:
- tray / menu-bar style utility
- local-first
- no backend
- no accounts
- Linux + macOS target
- minimal source code size
- open source, MIT

The intended user experience is playful and simple:
- install app
- it sits quietly
- shortly before the meeting, it plays a dramatic sting
- default sound should work out of the box
- power users may override the sound via a config directory file

## Non-goals

- No web app
- No server
- No cloud sync
- No authentication
- No complex calendar OAuth integration for MVP
- No framework bloat unless absolutely necessary

## Important product decisions already made

### 1) Tray-first UX
The app should primarily live in the tray / menu bar.
A tiny settings window is fine, but the product should feel like a background utility, not a big app window.

### 2) Default sound + optional override
Do **not** make custom sound selection the main UI.

Preferred behavior:
- bundle a default dramatic sound
- if user places a file at the config override path, use that instead

Expected override path on Linux:
- `~/.config/standup-siren/ring.mp3`

### 3) Scheduling direction
Current MVP target:
- one daily meeting time
- configurable seconds-before offset

Later target:
- local calendar import, likely `.ics`
- local event-title matching

Do not jump into Google Calendar / OAuth hell unless explicitly requested.

### 4) GitHub-first workflow
The human wants to track progress in GitHub, not via walls of code in chat.
Keep commits incremental and meaningful.

## Critical implementation constraint

### Debian 11 (Bullseye) compatibility matters
This is not optional.

A Tauri prototype was attempted first, but it was abandoned because the modern Tauri/Linux/WebKit stack expects a newer GLib/WebKit baseline than Debian 11 provides.

That means:
- do **not** casually pivot back to Tauri unless you have a concrete, tested Bullseye-compatible plan
- the current Python direction exists for a real reason, not personal taste

## Why the stack pivot happened

Initial plan:
- Tauri + tiny JS frontend

What went wrong:
- Tauri v2 / wry / webkit2gtk dependency chain wants newer Linux system libraries
- Bullseye only provides older GLib/WebKit packages
- installing more apt packages did not solve it
- pinning earlier Tauri versions still did not solve it

Result:
- repository pivoted to a Python prototype that is much more plausible on Debian 11

## Current chosen stack

Current implementation direction:
- Python 3.9+
- `uv` for dependency management and running
- `pystray` for tray behavior
- `Pillow` for icon/image work
- stdlib for config + scheduler logic
- ffmpeg-generated bundled default ring asset

Current repository intentionally avoids unnecessary framework complexity.

## Repository map

- `standup_siren/config.py`
  - config paths
  - settings dataclass
  - load/save config

- `standup_siren/scheduler.py`
  - next-trigger calculation logic

- `standup_siren/audio.py`
  - resolve bundled vs override ring
  - attempt playback via local system tools

- `standup_siren/app.py`
  - CLI entrypoint
  - self-test / init-config / test-sound commands

- `assets/default-ring.mp3`
  - bundled fallback sound

- `scripts/generate_default_ring.sh`
  - reproducibly generate the default sound

- `pyproject.toml`
  - Python project metadata and dependencies

## Current status

Working now:
- config path logic
- default config creation
- scheduler math
- bundled sound file exists
- sound resolution logic exists
- headless self-test works
- real tray/menu app skeleton exists
- tiny Tk settings window exists
- background scheduler loop updates trigger state and fires sound while running
- PyInstaller bundle build script exists
- packaged binary passes headless `--self-test`
- development uses `uv`

Not finished yet:
- verify tray icon works in a real desktop session
- harden duplicate-play protection across wake/resume/restart
- autostart integration
- macOS-specific app packaging polish
- `.ics` import

## Verified facts from development so far

- `uv sync` works on the target machine
- `uv run standup-siren --init-config` works
- `uv run standup-siren --self-test --verbose` works
- `./scripts/build_bundle.sh` produces `dist/standup-siren/`
- `./dist/standup-siren/standup-siren --self-test --verbose` works in headless context
- headless CLI modes remain usable after moving `pystray` import inside tray runtime
- sound playback path can launch a local player when available
- GUI tray testing is still limited by headless session context, not by immediate Python stack incompatibility

## How to run the project now

```bash
uv sync
uv run standup-siren --init-config
uv run standup-siren --self-test --verbose
uv run standup-siren --test-sound --verbose
```

## What the next agent should probably do

Recommended next implementation order:

1. **Build a real tray prototype**
   - make `pystray` lifecycle real
   - verify it works in an actual desktop session

2. **Add a tiny settings window**
   - daily meeting time
   - seconds-before offset
   - maybe verbose toggle
   - save config locally

3. **Add scheduler loop**
   - compute next trigger
   - sleep/check intelligently
   - avoid replay storms after wake/resume

4. **Improve logging**
   - add verbose logs
   - maybe log file in config dir

5. **Add autostart**
   - Linux first
   - macOS second

6. **Package it**
   - PyInstaller or similar
   - document artifacts clearly

7. **Then consider `.ics` import**
   - local file import only
   - title matching

## Guardrails for future changes

- Keep dependencies small.
- Keep code boring.
- Prefer robust local behavior over ambitious integrations.
- Test on Debian 11 before claiming success.
- Do not introduce a giant frontend stack for a toy utility.
- Do not reintroduce the original copyright mistake.

## License / attribution note

Earlier development accidentally put the human's personal name into copyright text.
That was corrected by rewriting history.
Do not repeat that mistake.

Use repository/project attribution style, not personal user attribution, unless explicitly asked.

## Communication note

When reporting progress to the human:
- keep it concrete
- prefer GitHub-visible progress
- mention what was actually tested versus what is still theoretical
- do not bluff runtime validation

## Updating project state after work

After completing meaningful tasks, future agents should usually update at least one of:
- `AGENTS.md` — durable context, decisions, traps, constraints, current state
- `BACKLOG.md` — current execution queue / checklist / priorities
- `README.md` — human-facing usage or build instructions when behavior changes

Rule of thumb:
- if the human would need to know how to run/use it → update `README.md`
- if another agent would need to know why/how/what changed → update `AGENTS.md`
- if the next chunk of work changed → update `BACKLOG.md`
