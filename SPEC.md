# Product Spec

## One-line idea
A tiny tray app that plays dramatic intro music shortly before a recurring daily meeting.

## User story
As a person with a daily standup or team meeting, I want my computer to play a dramatic countdown-style sting shortly before the meeting starts so I get a fun, impossible-to-ignore cue.

## Requirements

### Functional
- User can set a daily meeting time.
- User can set an offset in seconds before the meeting (default 10).
- App plays the audio exactly once per day for that scheduled event.
- User can press a test button to verify audio works.
- App uses a bundled default sound.
- Advanced users can override the sound by placing a file in the app config directory.
- App remembers settings between launches.
- App should resume scheduling after reboot/login.

### Non-functional
- Runs locally on macOS and Linux.
- Minimal code and minimal dependencies.
- Tray-first UX.
- No backend.
- No account system.
- Open-source friendly.

## Nice-to-have later
- local calendar `.ics` import and event-title matching
- multiple schedules
- weekday-only scheduling
- snooze button
- notification popup before playback
- tiny landing page with macOS/Linux download buttons

## Edge cases
- If app launches after today's trigger time, schedule for tomorrow.
- If audio file is missing, show clear error and do not crash.
- If computer sleeps through the trigger, play only if wake is still within a short grace window or just schedule next run.
- Handle timezone changes using system local time.
