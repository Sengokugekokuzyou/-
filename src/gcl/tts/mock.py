"""Offline mock TTS — a silent WAV whose length tracks the text.

Lets the whole pipeline (and CI) run with no VOICEVOX engine present. Produces a
valid 16-bit PCM mono WAV so concatenation and probing behave exactly like real
output. Never used for a published video — only dev/test/dry paths.
"""
from __future__ import annotations

import io
import wave

from .base import SynthesisRequest, TTSProvider

SAMPLE_RATE = 24000  # matches VOICEVOX default output
SEC_PER_CHAR = 0.12  # rough JA speaking pace


class MockProvider(TTSProvider):
    name = "mock"

    def is_available(self) -> bool:
        return True

    def synthesize(self, req: SynthesisRequest) -> bytes:
        chars = max(1, len(req.text.strip()))
        dur = req.pre_silence + chars * SEC_PER_CHAR / max(req.speed, 0.1) \
            + req.post_silence
        n = int(dur * SAMPLE_RATE)
        buf = io.BytesIO()
        with wave.open(buf, "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SAMPLE_RATE)
            w.writeframes(b"\x00\x00" * n)  # silence
        return buf.getvalue()
