"""VOICEVOX provider (§22) — talks to the local VOICEVOX Engine HTTP API.

VOICEVOX runs on the user's own machine (desktop app or `run.exe`), exposing an
HTTP server (default ``http://127.0.0.1:50021``). Free, offline, commercial-use
OK under the VOICEVOX terms — no monthly fee (§9). Credit "VOICEVOX:<speaker>" in
the video description as their terms require.

Flow per line:
    POST /audio_query?text=..&speaker=ID      -> query JSON
    (apply prosody overrides)
    POST /synthesis?speaker=ID  (body=query)  -> 16-bit PCM WAV bytes

The HTTP layer is injectable so tests run without a live engine.
"""
from __future__ import annotations

import json
import urllib.parse
import urllib.request

from .base import SynthesisRequest, TTSError, TTSProvider


def _default_get(url: str, timeout: float) -> bytes:
    with urllib.request.urlopen(url, timeout=timeout) as r:  # noqa: S310
        return r.read()


def _default_post(url: str, data: bytes | None, headers: dict, timeout: float) -> bytes:
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:  # noqa: S310
        return r.read()


class VoicevoxProvider(TTSProvider):
    name = "voicevox"

    def __init__(
        self,
        host: str = "http://127.0.0.1:50021",
        *,
        timeout: float = 30.0,
        http_get=_default_get,
        http_post=_default_post,
    ) -> None:
        self.host = host.rstrip("/")
        self.timeout = timeout
        self._get = http_get
        self._post = http_post

    def is_available(self) -> bool:
        try:
            self._get(f"{self.host}/version", 3.0)
            return True
        except Exception:  # noqa: BLE001 - reachability probe
            return False

    def audio_query(self, text: str, speaker: int) -> dict:
        qs = urllib.parse.urlencode({"text": text, "speaker": speaker})
        raw = self._post(f"{self.host}/audio_query?{qs}", None, {}, self.timeout)
        return json.loads(raw)

    def synthesis(self, query: dict, speaker: int) -> bytes:
        body = json.dumps(query).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        qs = urllib.parse.urlencode({"speaker": speaker})
        return self._post(f"{self.host}/synthesis?{qs}", body, headers, self.timeout)

    def synthesize(self, req: SynthesisRequest) -> bytes:
        if not req.text.strip():
            raise TTSError("empty narration text")
        try:
            query = self.audio_query(req.text, req.speaker)
        except Exception as e:  # noqa: BLE001
            raise TTSError(
                f"VOICEVOX audio_query failed ({self.host}): {e}. "
                "Is the VOICEVOX engine running?"
            ) from e
        # Prosody overrides — the calm documentary voice (§22).
        query["speedScale"] = req.speed
        query["pitchScale"] = req.pitch
        query["intonationScale"] = req.intonation
        query["volumeScale"] = req.volume
        query["prePhonemeLength"] = req.pre_silence
        query["postPhonemeLength"] = req.post_silence
        try:
            return self.synthesis(query, req.speaker)
        except Exception as e:  # noqa: BLE001
            raise TTSError(f"VOICEVOX synthesis failed: {e}") from e
