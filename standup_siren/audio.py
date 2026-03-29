from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from .config import override_ring_path


def bundled_ring_path() -> Path:
    return Path(__file__).resolve().parent.parent / "assets" / "default-ring.mp3"


def resolve_ring_path() -> Path:
    override = override_ring_path()
    return override if override.exists() else bundled_ring_path()


def play_ring(verbose: bool = False) -> None:
    ring = resolve_ring_path()
    if not ring.exists():
        raise FileNotFoundError(f"ring file not found: {ring}")

    players = [
        ["ffplay", "-nodisp", "-autoexit", "-loglevel", "error", str(ring)],
        ["paplay", str(ring)],
        ["aplay", str(ring)],
        ["afplay", str(ring)],
    ]
    for cmd in players:
        if shutil.which(cmd[0]):
            if verbose:
                print("playing with:", " ".join(cmd))
            subprocess.Popen(cmd)
            return
    raise RuntimeError("no supported audio player found (ffplay, paplay, aplay, afplay)")
