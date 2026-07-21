"""Select a TTS provider from config (§22, §32 config-driven)."""
from __future__ import annotations

from .base import TTSProvider
from .mock import MockProvider
from .voicevox import VoicevoxProvider


def get_provider(cfg: dict) -> TTSProvider:
    """`cfg` is the merged config; reads the ``tts`` section.

        tts:
          provider: voicevox        # voicevox | mock
          host: "http://127.0.0.1:50021"
    """
    tts = (cfg or {}).get("tts", {}) if isinstance(cfg, dict) else {}
    name = str(tts.get("provider", "voicevox")).lower()
    if name == "mock":
        return MockProvider()
    if name == "voicevox":
        return VoicevoxProvider(
            host=tts.get("host", "http://127.0.0.1:50021"),
            timeout=float(tts.get("timeout_seconds", 30.0)),
        )
    raise ValueError(f"unknown tts provider: {name}")
