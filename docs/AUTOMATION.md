# AUTOMATION — the unattended loop

Goal: produce and **schedule** a normal video with no human in the loop, while
respecting the brief's safety rails (Quality-Gate PASS only, 予約投稿 not instant
public, game never altered for YouTube — §28, §29, §33).

## The one command

```bash
python -m gcl.cli auto \
  --experiment content/experiments/food_shortage_glen.yaml \
  --telemetry  workspace/telemetry/<latest>.jsonl \
  --frames     <game>/field_screenshots/gcl_video \
  --mode       scheduled
```

Chain executed:

```
score → pick candidate → fact-anchored script → VOICEVOX narration (冥鳴ひまり)
  → SRT subtitles → assemble (video length matched to narration) → Quality Gate
  → packaging (title/description/chapters/thumbnail text) → publish
```

Gate decides publish:
- **PASS** → uploaded per mode (scheduled = private + future publishAt).
- **WARN** → stays private/local; a human reviews.
- **FAIL** → not published at all.

## Running it hands-off (Windows)

Automation runs on the game machine (Godot + VOICEVOX are local). **Do not put a
Claude session in the loop** — use a plain scheduled script so it runs free and
offline (§9). A nightly `gcl_auto.bat`:

```bat
@echo off
cd /d C:\path\to\gekokujo-content-lab
set PYTHONPATH=src

rem 1) capture fresh strategic-map footage from the game
call C:\path\to\Vagrant-Crown\capture_video.bat 300

rem 2) (optional) run a headless sim first with GCL_TELEMETRY=1 to refresh telemetry

rem 3) produce + schedule
python -m gcl.cli auto ^
  --experiment content\experiments\food_shortage_glen.yaml ^
  --telemetry  workspace\telemetry\session_latest.jsonl ^
  --frames     C:\path\to\Vagrant-Crown\field_screenshots\gcl_video ^
  --mode       scheduled
```

Register it in **Task Scheduler** (e.g. daily 02:00). The PC must be on at that
time (Godot capture can't run in the cloud).

## Ramp-up (recommended)

1. `mode: local_only` — inspect `video.mp4` + `report.json` + `description.txt`.
2. `mode: private` — confirm uploads land correctly on the channel.
3. `mode: scheduled` — let PASS videos queue as 予約投稿; review the schedule.
4. Add the Analytics learner (Phase 5) to tune plan/title/thumbnail/timing.

## Cadence guard (§12)
`publishing.schedule` + `prevent_same_day_publish` keep the queue from bunching.
Recommended: normal video ≈ weekly, BGM MV monthly — don't let automation
over-post (§2-6, §12).

## What still needs the game machine
- Real strategic-map capture (`capture_video.bat`) — Godot.
- VOICEVOX narration — local engine on `127.0.0.1:50021`.
Everything else (scoring, scripting, editing, gating, packaging, upload) is pure
Python and runs anywhere.
