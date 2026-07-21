"""TTS provider interface (§22).

All providers emit 16-bit PCM WAV bytes so downstream concatenation uses only the
stdlib ``wave`` module (no ffmpeg dependency in the TTS layer, no extra pip deps).
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


class TTSError(Exception):
    pass


@dataclass
class SynthesisRequest:
    text: str
    # Calm documentary tone by default (§22): slightly slower, flatter intonation.
    speaker: int = 3
    speed: float = 0.95          # speedScale
    pitch: float = 0.0           # pitchScale
    intonation: float = 0.9      # intonationScale (lower = calmer)
    volume: float = 1.0          # volumeScale
    pre_silence: float = 0.10    # seconds of lead-in
    post_silence: float = 0.35   # seconds of tail (natural pacing between lines)


class TTSProvider(ABC):
    name: str = "base"

    @abstractmethod
    def synthesize(self, req: SynthesisRequest) -> bytes:
        """Return WAV bytes (16-bit PCM) for the request text."""

    @abstractmethod
    def is_available(self) -> bool:
        """Cheap reachability check — used by `gcl doctor` and preflight."""
