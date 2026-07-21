"""Subtitles (§23). SRT now; ASS / burn-in / EN in later increments.

Placement rule (§23): subtitles sit low but must not cover on-screen UI or the
character — the burn-in filter uses a safe lower band above the title area.
"""
from .srt import write_srt

__all__ = ["write_srt"]
