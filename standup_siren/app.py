from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime

from .audio import play_ring, resolve_ring_path
from .config import Settings, load_settings, save_settings
from .scheduler import next_trigger


def run_self_test(verbose: bool = False) -> int:
    settings = load_settings()
    info = next_trigger(datetime.now(), settings.meeting_time, settings.offset_seconds)
    print("settings:", settings)
    print("ring:", resolve_ring_path())
    print("next trigger:", info.trigger_at.isoformat())
    print("meeting at:", info.meeting_at.isoformat())
    if verbose:
        print("display:", os.environ.get("DISPLAY", ""))
    return 0


def run_test_sound(verbose: bool = False) -> int:
    play_ring(verbose=verbose)
    return 0


def run_init_config() -> int:
    settings = load_settings()
    save_settings(settings)
    print("initialized config")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="standup-siren")
    parser.add_argument("--self-test", action="store_true", help="run headless config/scheduler checks")
    parser.add_argument("--test-sound", action="store_true", help="play the configured ring once")
    parser.add_argument("--init-config", action="store_true", help="create default config if missing")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    if args.init_config:
        return run_init_config()
    if args.self_test:
        return run_self_test(verbose=args.verbose)
    if args.test_sound:
        return run_test_sound(verbose=args.verbose)

    print("GUI/tray mode prototype is not wired yet in this commit.")
    print("Use --self-test or --test-sound for now.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
