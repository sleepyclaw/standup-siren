from __future__ import annotations

import argparse
import os
import subprocess
import sys
import threading
import time
import tkinter as tk
from datetime import datetime
from tkinter import messagebox
from typing import Any

from PIL import Image, ImageDraw

from .audio import play_ring, resolve_ring_path
from .config import Settings, config_path, load_settings, save_settings
from .scheduler import next_trigger


class StandupSirenApp:
    def __init__(self, verbose: bool = False) -> None:
        self.verbose = verbose
        self.settings = load_settings()
        if verbose:
            self.settings.verbose = True
        self.icon: Any | None = None
        self.stop_event = threading.Event()
        self.settings_window: tk.Tk | None = None
        self.scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self.last_fired_key: str | None = None
        self.next_status_text = "Next trigger: calculating..."

    def log(self, *parts: object) -> None:
        if self.verbose or self.settings.verbose:
            print("[standup-siren]", *parts, flush=True)

    def run(self) -> int:
        import pystray

        self.icon = pystray.Icon(
            "standup-siren",
            self._build_icon_image(),
            "Standup Siren",
            menu=pystray.Menu(
                pystray.MenuItem(lambda item: self.next_status_text, None, enabled=False),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem(self._settings_menu_label, self._on_open_settings),
                pystray.MenuItem("Test sound", self._on_test_sound),
                pystray.MenuItem("Quit", self._on_quit),
            ),
        )
        self.scheduler_thread.start()
        self.log("starting tray app")
        self.icon.run()
        return 0

    def _build_icon_image(self) -> Image.Image:
        image = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.ellipse((8, 8, 56, 56), fill=(34, 36, 50, 255), outline=(255, 196, 0, 255), width=3)
        draw.arc((16, 16, 48, 48), start=200, end=340, fill=(255, 196, 0, 255), width=4)
        draw.rectangle((29, 20, 35, 36), fill=(255, 196, 0, 255))
        draw.ellipse((24, 34, 40, 50), fill=(255, 196, 0, 255))
        return image

    def _refresh_status(self) -> None:
        info = next_trigger(datetime.now(), self.settings.meeting_time, self.settings.offset_seconds)
        self.next_status_text = f"Next trigger: {info.trigger_at.strftime('%Y-%m-%d %H:%M:%S')}"
        self.log("next trigger", info.trigger_at.isoformat(), "meeting", info.meeting_at.isoformat())
        if self.icon is not None:
            self.icon.title = f"Standup Siren — {self.next_status_text}"
            self.icon.update_menu()

    def _scheduler_loop(self) -> None:
        self.log("scheduler loop started")
        while not self.stop_event.is_set():
            try:
                now = datetime.now()
                info = next_trigger(now, self.settings.meeting_time, self.settings.offset_seconds)
                due_key = info.trigger_at.strftime("%Y-%m-%dT%H:%M:%S")
                self.next_status_text = f"Next trigger: {info.trigger_at.strftime('%Y-%m-%d %H:%M:%S')}"
                if self.icon is not None:
                    self.icon.title = f"Standup Siren — {self.next_status_text}"
                    self.icon.update_menu()

                wait_seconds = (info.trigger_at - now).total_seconds()
                if wait_seconds <= 1 and self.last_fired_key != due_key:
                    self.log("triggering ring for", due_key)
                    self.last_fired_key = due_key
                    play_ring(verbose=self.verbose or self.settings.verbose)
                    time.sleep(1)
                    continue

                sleep_for = 1 if wait_seconds <= 5 else min(wait_seconds, 30)
                self.stop_event.wait(max(0.5, sleep_for))
            except Exception as exc:  # noqa: BLE001
                self.next_status_text = f"Error: {exc}"
                self.log("scheduler error:", repr(exc))
                if self.icon is not None:
                    self.icon.title = f"Standup Siren — {self.next_status_text}"
                    self.icon.update_menu()
                self.stop_event.wait(5)
        self.log("scheduler loop stopped")

    def _run_on_tk_thread(self, func) -> None:
        root = self.settings_window
        if root is None:
            return
        root.after(0, func)

    def _settings_menu_label(self, item: Any | None = None) -> str:
        return "Open config" if sys.platform == "darwin" else "Open settings"

    def _on_open_settings(self, icon: Any | None = None, item: Any | None = None) -> None:
        if sys.platform == "darwin":
            self._open_config_for_macos()
            return
        if self.settings_window is not None:
            self._run_on_tk_thread(lambda: (self.settings_window.deiconify(), self.settings_window.lift(), self.settings_window.focus_force()))
            return
        thread = threading.Thread(target=self._settings_window_mainloop, daemon=True)
        thread.start()

    def _open_config_for_macos(self) -> None:
        path = config_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            save_settings(self.settings)
        commands = [
            ["open", "-R", str(path)],
            ["open", str(path.parent)],
        ]
        last_error: Exception | None = None
        for cmd in commands:
            try:
                subprocess.Popen(cmd)
                return
            except Exception as exc:  # noqa: BLE001
                last_error = exc
        raise RuntimeError(f"failed to open config in Finder: {last_error}")

    def _settings_window_mainloop(self) -> None:
        root = tk.Tk()
        root.title("Standup Siren")
        root.resizable(False, False)
        root.protocol("WM_DELETE_WINDOW", lambda: self._close_settings_window(root))

        frame = tk.Frame(root, padx=12, pady=12)
        frame.pack(fill="both", expand=True)

        meeting_var = tk.StringVar(value=self.settings.meeting_time)
        offset_var = tk.StringVar(value=str(self.settings.offset_seconds))
        next_var = tk.StringVar(value=self._next_trigger_label())

        tk.Label(frame, text="Meeting time (HH:MM)").grid(row=0, column=0, sticky="w")
        tk.Entry(frame, textvariable=meeting_var, width=12).grid(row=1, column=0, sticky="we", pady=(2, 10))

        tk.Label(frame, text="Seconds before meeting").grid(row=2, column=0, sticky="w")
        tk.Entry(frame, textvariable=offset_var, width=12).grid(row=3, column=0, sticky="we", pady=(2, 10))

        tk.Label(frame, textvariable=next_var, justify="left").grid(row=4, column=0, sticky="w", pady=(0, 10))

        buttons = tk.Frame(frame)
        buttons.grid(row=5, column=0, sticky="we")

        def save() -> None:
            try:
                meeting_time = meeting_var.get().strip()
                self._validate_meeting_time(meeting_time)
                offset_seconds = int(offset_var.get().strip())
                if offset_seconds < 0:
                    raise ValueError("offset must be >= 0")
                self.settings.meeting_time = meeting_time
                self.settings.offset_seconds = offset_seconds
                save_settings(self.settings)
                self._refresh_status()
                next_var.set(self._next_trigger_label())
                messagebox.showinfo("Standup Siren", "Settings saved.")
            except Exception as exc:  # noqa: BLE001
                messagebox.showerror("Standup Siren", str(exc))

        def test_sound() -> None:
            try:
                play_ring(verbose=self.verbose or self.settings.verbose)
            except Exception as exc:  # noqa: BLE001
                messagebox.showerror("Standup Siren", str(exc))

        tk.Button(buttons, text="Save", command=save, width=10).pack(side="left")
        tk.Button(buttons, text="Test sound", command=test_sound, width=10).pack(side="left", padx=8)
        tk.Button(buttons, text="Close", command=lambda: self._close_settings_window(root), width=10).pack(side="left")

        self.settings_window = root
        root.mainloop()

    def _close_settings_window(self, root: tk.Tk) -> None:
        self.settings_window = None
        root.destroy()

    def _next_trigger_label(self) -> str:
        info = next_trigger(datetime.now(), self.settings.meeting_time, self.settings.offset_seconds)
        return (
            f"Next trigger: {info.trigger_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Meeting at: {info.meeting_at.strftime('%Y-%m-%d %H:%M:%S')}"
        )

    def _validate_meeting_time(self, meeting_time: str) -> None:
        hours, minutes = map(int, meeting_time.split(":"))
        if hours < 0 or hours > 23 or minutes < 0 or minutes > 59:
            raise ValueError("meeting time must be in HH:MM 24-hour format")

    def _on_test_sound(self, icon: Any | None = None, item: Any | None = None) -> None:
        self.log("manual sound test")
        play_ring(verbose=self.verbose or self.settings.verbose)

    def _on_quit(self, icon: Any | None = None, item: Any | None = None) -> None:
        self.log("quitting")
        self.stop_event.set()
        if self.settings_window is not None:
            self._run_on_tk_thread(self.settings_window.destroy)
        if self.icon is not None:
            self.icon.stop()



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

    app = StandupSirenApp(verbose=args.verbose)
    return app.run()


if __name__ == "__main__":
    raise SystemExit(main())
