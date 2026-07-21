# Telemetry Exporter — install into GEKOKUJO

This is the **only** piece of GCL that lives inside the game. It is a non-invasive
autoload that listens to the game's existing `EventBus` and writes GCL telemetry
JSONL (see `../../docs/EVENT_SCHEMA.md`). It adds no gameplay logic and changes
no game state.

## Why it's safe (§2-1, §33)

- Reads **only** signals the game already emits (`EventBus`):
  `day_passed`, `action_executed`, `world_event`, `npc_state_changed`.
- Writes to `user://gcl_telemetry/` — never touches `res://` or save data.
- **Off by default.** It only runs when `GCL_TELEMETRY` is set in the environment
  or `gcl/telemetry_enabled` is `true` in Project Settings. Shipped player builds
  never enable it.

## Install

1. Copy `TelemetryExporter.gd` into the game repo, e.g.
   `res://scripts/tools/TelemetryExporter.gd`.
2. **Project Settings → Autoload** → add it with node name `TelemetryExporter`.
3. Enable it for a capture/soak run only:
   - Windows: `set GCL_TELEMETRY=1` before launching, **or**
   - add `gcl/telemetry_enabled = true` to a dev-only override.

## Run a headless simulation with telemetry

Reuse the existing soak harness (it already runs the strategic map headless):

```bat
set GCL_TELEMETRY=1
run_soak_map.bat 200
```

The JSONL lands in the Godot `user://` folder
(`%APPDATA%\Godot\app_userdata\<project>\gcl_telemetry\`). Copy it to
`workspace/telemetry/` on the GCL side, then:

```bash
python -m gcl.cli score --telemetry workspace/telemetry/session_XXXX.jsonl
```

## Enriching the stream (recommended, optional)

The richer the `result` / `data` dictionaries the game passes to
`action_executed` / `world_event`, the better GCL scores and narrates. The
high-value fields to include when you already have them:

- `cause_ids` — **the anti-fabrication backbone** (§21). Whenever an event was
  triggered by earlier events, pass their ids. GCL never invents causality; it
  can only report what you record here.
- `visual_priority` (0–100) — how filmable this moment is (§20/§26).
- `emotion_delta`, `relationship_delta` — power the Emotion/Transformation score.
- `witness_ids`, `location_id` — framing and camera targeting.

None of these are required; missing values are stored as `null`/`[]` per schema.
