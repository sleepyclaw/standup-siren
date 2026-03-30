from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path

APP_NAME = "standup-siren"
DEFAULT_RING_FILENAME = "ring.mp3"
CONFIG_README_FILENAME = "README.txt"


def config_dir() -> Path:
    xdg = os.environ.get("XDG_CONFIG_HOME")
    base = Path(xdg).expanduser() if xdg else Path.home() / ".config"
    return base / APP_NAME


def config_path() -> Path:
    return config_dir() / "config.json"


def override_ring_path() -> Path:
    return config_dir() / DEFAULT_RING_FILENAME


def config_readme_path() -> Path:
    return config_dir() / CONFIG_README_FILENAME


def config_readme_contents() -> str:
    return f"""Standup Siren config directory

Files you may see here:
- config.json  -> app settings
- {DEFAULT_RING_FILENAME} -> optional custom sound override
- {CONFIG_README_FILENAME} -> this file

Custom sound override:
- To use your own sound, place a file named `{DEFAULT_RING_FILENAME}` in this directory.
- Recommended format: mp3
- If `{DEFAULT_RING_FILENAME}` is missing, Standup Siren uses its bundled default sound.

Current override path:
- {override_ring_path()}

Notes:
- Replace the file if you want a different sound.
- Restart the app if your platform does not pick up the new file immediately.
"""


def ensure_config_support_files() -> None:
    directory = config_dir()
    directory.mkdir(parents=True, exist_ok=True)
    readme = config_readme_path()
    if not readme.exists():
        readme.write_text(config_readme_contents())


@dataclass
class Settings:
    meeting_time: str = "13:00"
    offset_seconds: int = 58
    launch_on_login: bool = False
    verbose: bool = False


def load_settings() -> Settings:
    ensure_config_support_files()
    path = config_path()
    if not path.exists():
        return Settings()
    data = json.loads(path.read_text())
    return Settings(**{**asdict(Settings()), **data})


def save_settings(settings: Settings) -> None:
    ensure_config_support_files()
    path = config_path()
    path.write_text(json.dumps(asdict(settings), indent=2) + "\n")
