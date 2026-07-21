# GEKOKUJO Content Lab (GCL)

Simulate many GEKOKUJO worlds, detect the **few** events worth publishing, and
turn them into **fact-based** third-person RPG videos and BGM music videos for the
Shirokuro Games channel.

> Core principle (§2): *don't mass-publish — mass-simulate, and publish only the
> high-value few.* Never fabricate facts the game didn't record (§21). Never let
> automation touch the game's balance for the sake of YouTube (§29).

This repo is the Content Lab. It is **decoupled from the game**: the only contract
is the telemetry JSONL the game emits and the frames/audio it captures. The single
piece that lives inside the game is a non-invasive telemetry exporter
(`godot_bridge/telemetry_export/`).

## Status — v0.1 (Phase 1 spine working)

The end-to-end spine runs today:

```
telemetry JSONL → detect candidates → Content Score → pick →
fact-based script + title candidates → FFmpeg assemble → Quality Gate → job report
```

## Quickstart

```bash
pip install -r requirements.txt            # PyYAML + imageio-ffmpeg (+ dev extras)
export PYTHONPATH=src

python -m gcl.cli doctor                    # check ffmpeg / font / config

# Rank story candidates from a telemetry stream:
python -m gcl.cli score \
  --telemetry workspace/telemetry/sample_north_forest.jsonl

# Produce a finished video from captured frames (demo uses placeholder frames):
python tools/make_placeholder_frames.py --out workspace/raw_capture/demo_frames \
  --seconds 4 --fps 30 --caption "北方森林 / Glen Village"

python -m gcl.cli render \
  --experiment content/experiments/food_shortage_glen.yaml \
  --telemetry  workspace/telemetry/sample_north_forest.jsonl \
  --frames     workspace/raw_capture/demo_frames
# → workspace/renders/<job_id>/{video.mp4, narration.wav, subtitles.ja.srt, report.json}
```

`--dry-run` prints the FFmpeg command without executing (§32).

### Narration (VOICEVOX, §22)

With the local VOICEVOX app running (`http://127.0.0.1:50021`), `render` narrates
automatically. Test it directly:

```bash
python -m gcl.cli doctor          # shows whether VOICEVOX is reachable
python -m gcl.cli tts \
  --telemetry workspace/telemetry/sample_north_forest.jsonl \
  --experiment content/experiments/food_shortage_glen.yaml \
  --speaker 3 --out workspace/audio/narration.wav
```

Offline (no engine): add `--tts-provider mock` / `--provider mock`. See
[`docs/TTS_SUBTITLES.md`](docs/TTS_SUBTITLES.md).

### Full automation (produce → schedule)

One command runs the whole chain and schedules a 予約投稿 (PASS-gated, never
instant-public):

```bash
python -m gcl.cli auto \
  --experiment content/experiments/food_shortage_glen.yaml \
  --telemetry  workspace/telemetry/sample_north_forest.jsonl \
  --frames     <game>/field_screenshots/gcl_video \
  --mode       scheduled
```

Run it nightly via Task Scheduler for hands-off operation — see
[`docs/AUTOMATION.md`](docs/AUTOMATION.md) and
[`docs/YOUTUBE_WORKFLOW.md`](docs/YOUTUBE_WORKFLOW.md) (one-time free OAuth).

## Layout

| Path | What |
|---|---|
| `src/gcl/telemetry/` | Read the game's event JSONL (`EVENT_SCHEMA.md`) |
| `src/gcl/story/` | Candidate detection + Content Score (§19) |
| `src/gcl/packaging/` | Fact-anchored script (§21) + title candidates (§25) |
| `src/gcl/editing/` | FFmpeg discovery + frame assembler (§24) |
| `src/gcl/quality/` | Quality Gate (§27) |
| `godot_bridge/telemetry_export/` | Drop-in Godot autoload — the game-side hook |
| `content/` | Experiment / BGM definitions |
| `config/` | All tunables (no hardcoded paths, §32) |
| `docs/` | Architecture, schemas, specs |

## Documentation

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — Phase 0 findings: what the game
  **already** provides vs. what GCL adds
- [`docs/IMPLEMENTATION_PLAN.md`](docs/IMPLEMENTATION_PLAN.md) — phased plan
- [`docs/EVENT_SCHEMA.md`](docs/EVENT_SCHEMA.md) — telemetry contract (§15)
- [`docs/TTS_SUBTITLES.md`](docs/TTS_SUBTITLES.md) — VOICEVOX narration & subtitles (§22, §23)
- [`docs/GODOT_INTEGRATION.md`](docs/GODOT_INTEGRATION.md) — how the game and GCL talk
- [`docs/REPLAY_DESIGN.md`](docs/REPLAY_DESIGN.md) — re-shoot strategy (§17)
- [`docs/BGM_MV_SPEC.md`](docs/BGM_MV_SPEC.md) — BGM music video pipeline (§8–11)
- [`docs/QUALITY_GATE.md`](docs/QUALITY_GATE.md) — checks & verdicts (§27)
- [`docs/AUTOMATION.md`](docs/AUTOMATION.md) — the unattended produce→schedule loop
- [`docs/YOUTUBE_WORKFLOW.md`](docs/YOUTUBE_WORKFLOW.md) — publishing + OAuth (§28)
- [`docs/CONFIG_REFERENCE.md`](docs/CONFIG_REFERENCE.md) — every config key

## Constraints honored

No paid APIs, no monthly services (§9). Local + free + commercial-use-OK tooling
only. FFmpeg via a bundled binary; TTS will use VOICEVOX (Phase 1 continuation).
