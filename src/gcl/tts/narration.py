"""Turn a script (list of ScriptLine) into one narration WAV + timing segments.

Timing segments are reused later for subtitle generation (§23): each line's
start/duration in the final track are known here. Concatenation uses only the
stdlib ``wave`` module, so this stage needs neither ffmpeg nor extra pip deps.
"""
from __future__ import annotations

import io
import wave
from dataclasses import dataclass, field
from pathlib import Path

from .base import SynthesisRequest, TTSProvider


@dataclass
class Segment:
    index: int
    section: str
    text: str
    start: float          # seconds into the final track
    duration: float

    def as_dict(self) -> dict:
        return {
            "index": self.index, "section": self.section, "text": self.text,
            "start": round(self.start, 3), "duration": round(self.duration, 3),
        }


@dataclass
class NarrationResult:
    wav_path: Path
    segments: list[Segment] = field(default_factory=list)

    @property
    def total_duration(self) -> float:
        return sum(s.duration for s in self.segments)


def _read_wav(data: bytes) -> tuple[int, int, int, bytes]:
    with wave.open(io.BytesIO(data), "rb") as w:
        return (w.getnchannels(), w.getsampwidth(), w.getframerate(),
                w.readframes(w.getnframes()))


def synthesize_script(
    provider: TTSProvider,
    script_lines: list,
    out_path: str | Path,
    *,
    speaker: int = 3,
    speed: float = 0.95,
    intonation: float = 0.9,
    gap_seconds: float = 0.15,
) -> NarrationResult:
    """Synthesize every script line and concatenate into ``out_path``.

    Lines with empty text are skipped. All synthesized clips must share the same
    WAV format (they do, coming from one provider).
    """
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    nchannels = sampwidth = framerate = None
    frames = bytearray()
    segments: list[Segment] = []
    cursor = 0.0

    for i, line in enumerate(script_lines):
        text = getattr(line, "text", "").strip()
        section = getattr(line, "section", "")
        if not text:
            continue
        req = SynthesisRequest(text=text, speaker=speaker, speed=speed,
                               intonation=intonation)
        ch, sw, fr, pcm = _read_wav(provider.synthesize(req))
        if framerate is None:
            nchannels, sampwidth, framerate = ch, sw, fr
        elif (ch, sw, fr) != (nchannels, sampwidth, framerate):
            raise ValueError("inconsistent WAV format across TTS segments")

        dur = len(pcm) / (framerate * sampwidth * nchannels)
        segments.append(Segment(i, section, text, cursor, dur))
        frames += pcm
        cursor += dur

        # Inter-line gap of silence for pacing.
        if gap_seconds > 0:
            silence = int(gap_seconds * framerate) * sampwidth * nchannels
            frames += b"\x00" * silence
            cursor += gap_seconds

    if framerate is None:
        raise ValueError("no narratable lines in script")

    with wave.open(str(out_path), "wb") as w:
        w.setnchannels(nchannels)
        w.setsampwidth(sampwidth)
        w.setframerate(framerate)
        w.writeframes(bytes(frames))

    return NarrationResult(wav_path=out_path, segments=segments)
