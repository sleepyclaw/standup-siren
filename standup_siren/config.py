from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path

APP_NAME = "standup-siren"
DEFAULT_RING_FILENAME = "ring.mp3"


def config_dir() -> Path:
    xdg = os.environ.get("XDG_CONFIG_HOME")
    base = Path(xdg).expanduser() if xdg else Path.home() / ".config"
    return base / APP_NAME


def config_path() -> Path:
    return config_dir() / "config.json"


def override_ring_path() -> Path:
    return config_dir() / DEFAULT_RING_FILENAME


@dataclass
class Settings:
    meeting_time: str = "10:00"
    offset_seconds: int = 10
    launch_on_login: bool = False
    verbose: bool = False


def load_settings() -> Settings:
    path = config_path()
    if not path.exists():
        return Settings()
    data = json.loads(path.read_text())
    return Settings(**{**asdict(Settings()), **data})


def save_settings(settings: Settings) -> None:
    path = config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(asdict(settings), indent=2) + "\n")
