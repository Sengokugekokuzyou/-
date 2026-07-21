"""Read the game's telemetry JSONL into ``Event`` objects.

Robust by design (§32 "resumable", "log each step"): a single malformed line
never aborts the whole run — it is collected and reported. UTF-8 only.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .schema import Event


class ReaderError(Exception):
    pass


@dataclass
class ReadResult:
    events: list[Event]
    skipped: list[tuple[int, str]]  # (line_number, reason)

    @property
    def ok(self) -> bool:
        return bool(self.events)


def read_events(path: str | Path, *, strict: bool = False) -> ReadResult:
    """Parse a ``.jsonl`` telemetry file.

    strict=True raises on the first bad line; otherwise bad lines are skipped and
    surfaced in ``skipped`` so the caller (and Quality Gate) can see data loss
    instead of silently dropping it.
    """
    p = Path(path)
    if not p.exists():
        raise ReaderError(f"telemetry file not found: {p}")

    events: list[Event] = []
    skipped: list[tuple[int, str]] = []
    with p.open("r", encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, start=1):
            line = line.strip()
            if not line or line.startswith("//"):
                continue
            try:
                raw = json.loads(line)
                events.append(Event.from_dict(raw))
            except (json.JSONDecodeError, ValueError) as exc:
                if strict:
                    raise ReaderError(f"{p}:{lineno}: {exc}") from exc
                skipped.append((lineno, str(exc)))

    events.sort(key=lambda e: (e.game_day, e.timestamp))
    return ReadResult(events=events, skipped=skipped)
