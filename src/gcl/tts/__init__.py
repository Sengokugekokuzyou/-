"""Text-to-speech (§22).

Pluggable provider structure so the engine can be swapped without touching the
pipeline:

    TTSProvider
    ├─ VoicevoxProvider     (implemented — local HTTP, free, no monthly fee §9)
    ├─ AivisProvider        (future)
    └─ StyleBertVitsProvider(future)

BGM MVs get no narration by default (§22).
"""

from .base import TTSProvider, SynthesisRequest, TTSError
from .voicevox import VoicevoxProvider
from .mock import MockProvider
from .factory import get_provider
from .narration import synthesize_script, NarrationResult

__all__ = [
    "TTSProvider",
    "SynthesisRequest",
    "TTSError",
    "VoicevoxProvider",
    "MockProvider",
    "get_provider",
    "synthesize_script",
    "NarrationResult",
]
