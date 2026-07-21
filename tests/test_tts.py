import io
import json
import wave

from gcl.tts import MockProvider, synthesize_script
from gcl.tts.base import SynthesisRequest
from gcl.tts.voicevox import VoicevoxProvider
from gcl.tts.factory import get_provider
from gcl.packaging.script_builder import ScriptLine
from gcl.subtitles import write_srt


def _wav_seconds(data: bytes) -> float:
    with wave.open(io.BytesIO(data), "rb") as w:
        return w.getnframes() / w.getframerate()


def test_mock_provider_duration_tracks_text():
    p = MockProvider()
    short = p.synthesize(SynthesisRequest(text="短い"))
    long = p.synthesize(SynthesisRequest(text="これはかなり長い文章になっています"))
    assert _wav_seconds(long) > _wav_seconds(short)


def test_voicevox_applies_prosody_and_calls_endpoints():
    calls = {}

    def fake_get(url, timeout):
        calls["get"] = url
        return b"0.14.0"

    def fake_post(url, data, headers, timeout):
        if "/audio_query" in url:
            calls["query_url"] = url
            return json.dumps({"speedScale": 1.0, "accent_phrases": []}).encode()
        # /synthesis — capture the body the provider sent
        calls["synth_body"] = json.loads(data)
        # return a tiny valid wav
        buf = io.BytesIO()
        with wave.open(buf, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000)
            w.writeframes(b"\x00\x00" * 2400)
        return buf.getvalue()

    prov = VoicevoxProvider(http_get=fake_get, http_post=fake_post)
    assert prov.is_available() is True
    out = prov.synthesize(SynthesisRequest(text="こんにちは", speaker=5, speed=0.9,
                                           intonation=0.8))
    assert _wav_seconds(out) > 0
    # prosody overrides made it into the synthesis body (§22 calm voice)
    assert calls["synth_body"]["speedScale"] == 0.9
    assert calls["synth_body"]["intonationScale"] == 0.8
    assert "speaker=5" in calls["query_url"]


def test_voicevox_unavailable_when_get_raises():
    def boom(url, timeout):
        raise OSError("connection refused")
    prov = VoicevoxProvider(http_get=boom)
    assert prov.is_available() is False


def test_synthesize_script_concats_and_times(tmp_path):
    script = [
        ScriptLine("Hook", "一日目、事件が起きた", ("e1",)),
        ScriptLine("Question", "何が起きたのか", ()),
        ScriptLine("Steam CTA", "", ()),   # empty → skipped
    ]
    res = synthesize_script(MockProvider(), script, tmp_path / "n.wav",
                            gap_seconds=0.1)
    assert res.wav_path.exists()
    assert len(res.segments) == 2                    # empty line skipped
    assert res.segments[0].start == 0.0
    assert res.segments[1].start > res.segments[0].duration  # sequential + gap
    assert _wav_seconds(res.wav_path.read_bytes()) > 0


def test_srt_written(tmp_path):
    script = [ScriptLine("Hook", "一行目", ("e1",))]
    res = synthesize_script(MockProvider(), script, tmp_path / "n.wav")
    srt = write_srt(res.segments, tmp_path / "n.srt")
    body = srt.read_text(encoding="utf-8")
    assert "00:00:00,000 -->" in body
    assert "一行目" in body


def test_factory_selects_mock():
    prov = get_provider({"tts": {"provider": "mock"}})
    assert prov.name == "mock"
