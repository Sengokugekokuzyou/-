"""Write an SRT from narration timing segments (§23).

Because the TTS stage already knows each line's start/duration in the final
track, subtitles are exact and free — no forced alignment needed.
"""
from __future__ import annotations

from pathlib import Path


def _ts(seconds: float) -> str:
    if seconds < 0:
        seconds = 0.0
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def write_srt(segments, out_path: str | Path) -> Path:
    """`segments` are tts.narration.Segment (start, duration, text)."""
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    for n, seg in enumerate(segments, start=1):
        start = getattr(seg, "start", 0.0)
        end = start + getattr(seg, "duration", 0.0)
        text = getattr(seg, "text", "")
        lines.append(str(n))
        lines.append(f"{_ts(start)} --> {_ts(end)}")
        lines.append(text)
        lines.append("")
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path
