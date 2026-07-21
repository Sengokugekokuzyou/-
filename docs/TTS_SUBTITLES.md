# TTS & Subtitles (§22, §23)

## TTS — pluggable providers (§22)

```
TTSProvider (src/gcl/tts/base.py)
├─ VoicevoxProvider     local HTTP engine — implemented
├─ MockProvider         silent WAV, offline — for dev/test/CI
├─ AivisProvider        future
└─ StyleBertVitsProvider future
```

No monthly fee, runs locally (§9). Default voice is **calm documentary** (§22):
`speed 0.95`, `intonation 0.9`. BGM MVs get no narration by default.

### VOICEVOX setup (your machine)

1. Install & launch the VOICEVOX app (or `run.exe`). It serves
   `http://127.0.0.1:50021`.
2. `config/tts.yaml` → `provider: voicevox`, set `host`, pick a `speaker` id.
3. Check the connection:
   ```bash
   python -m gcl.cli doctor        # shows: [ok] tts: voicevox reachable ...
   ```
4. Synthesize a script's narration standalone (fastest end-to-end test):
   ```bash
   python -m gcl.cli tts \
     --telemetry workspace/telemetry/sample_north_forest.jsonl \
     --experiment content/experiments/food_shortage_glen.yaml \
     --speaker 3 --out workspace/audio/narration.wav
   ```
   → `narration.wav` + `narration.srt`.

Credit `VOICEVOX:<speaker>` in the video description (their terms; `tts.credit`).

### In the render pipeline

`gcl render` narrates automatically when the engine is reachable
(`--narrate auto`, the default). Force with `--narrate on`, disable with
`--narrate off`. Offline demo/CI: `--tts-provider mock`. The narration WAV is
muxed as the video's audio track and its line timing is written to the report.

## Subtitles (§23)

`gcl.subtitles.write_srt` emits an SRT straight from narration timing — exact, no
forced alignment. Written as `subtitles.ja.srt` in the job folder.

Planned: ASS output, burned-in variant, no-subtitle variant, EN track. Placement
stays in a safe lower band so it never covers UI or the character (§23).

## Dependencies

None beyond the stdlib — `urllib` for HTTP, `wave` for audio concat. Keeps the
"no paid services / minimal deps" constraint (§9, §32).
