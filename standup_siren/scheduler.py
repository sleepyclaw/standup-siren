from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class TriggerInfo:
    meeting_at: datetime
    trigger_at: datetime


def next_trigger(now: datetime, meeting_time: str, offset_seconds: int) -> TriggerInfo:
    hours, minutes = map(int, meeting_time.split(":"))
    meeting_at = now.replace(hour=hours, minute=minutes, second=0, microsecond=0)
    trigger_at = meeting_at - timedelta(seconds=offset_seconds)
    if trigger_at <= now:
        meeting_at = meeting_at + timedelta(days=1)
        trigger_at = meeting_at - timedelta(seconds=offset_seconds)
    return TriggerInfo(meeting_at=meeting_at, trigger_at=trigger_at)
