# GODOT_INTEGRATION — how the game and GCL talk

The link is **files on disk**, chosen as the simplest stable method (§14: "最初は
最も安定する単純な方式を選んでください"). No sockets, no long-running RPC in v0.1.

```
GEKOKUJO (Godot 4.6)                     GCL (Python)
─────────────────────                    ─────────────
EventBus signals                         
   ↓                                     
TelemetryExporter.gd  ──►  user://gcl_telemetry/*.jsonl  ──►  workspace/telemetry/
strategic_capture.tscn ─►  frame PNG sequence            ──►  workspace/raw_capture/
                                                              ↓
                                                         gcl.cli render → MP4
```

## 1. Telemetry export (implemented)

`godot_bridge/telemetry_export/TelemetryExporter.gd` is a drop-in autoload. See
its `README.md` for install. Key properties:

- Subscribes to the **existing** `EventBus` singleton
  (`scripts/world/pseudo_player/EventBus.gd`) — adds no gameplay logic.
- Writes §15 JSONL to `user://gcl_telemetry/`.
- **OFF unless** `GCL_TELEMETRY` env var is set or `gcl/telemetry_enabled` project
  setting is true — shipped builds never run it (§2-1, §33).

Run a headless simulation with telemetry via the existing soak harness:

```bat
set GCL_TELEMETRY=1
run_soak_map.bat 200
```

## 2. Frame capture (implemented for the strategic map)

`strategic_capture.tscn` writes stills; the new **`strategic_video_capture.tscn`**
(script `scripts/tools/StrategicVideoCapture.gd`, launcher `capture_video.bat`)
writes a **numbered frame sequence** (`frame_%05d.png`) — exactly what GCL's
assembler consumes. It reuses the still-capture's non-destructive setup (guards
off at runtime only, SafeMode lightweight, lights/env untouched) and adds a slow
cinematic push-in (overview → mid) with the hero+wolf proxies, so the footage
reads as the real軍略マップ, not a debug view. Calm move, no fast cuts (§11).

Run it (on the game machine):

```bat
capture_video.bat 300           :: 300 frames (~10s) → C:\Godot\capture\video
set GEKO_CAPTURE_SIM=1           :: optional: let the world sim evolve across frames
```

It copies frames to `field_screenshots\gcl_video`; point GCL at that dir:

```bash
python -m gcl.cli render --experiment content/experiments/food_shortage_glen.yaml \
  --telemetry workspace/telemetry/sample_north_forest.jsonl \
  --frames <path>/field_screenshots/gcl_video
```

Env knobs: `GEKO_CAPTURE_OUT`, `GEKO_CAPTURE_FRAMES`, `GEKO_CAPTURE_SETTLE`,
`GEKO_CAPTURE_SIM`, `GEKO_STRATEGIC_REGION`. `tools/make_placeholder_frames.py`
still stands in for offline demos.

For Early-Access 3D third-person capture, **Godot Movie Maker mode**
(`--write-movie`) records the running scene at a fixed FPS — same `--frames`
contract on the GCL side.

## 3. Re-simulation / replay (Phase 3)

`world_seed` + recorded events let GCL ask the game to re-run a scenario for
re-shooting (§17). See `REPLAY_DESIGN.md` for the staged approach (periodic save →
pre-event autosave → scenario re-run → approximate → full deterministic replay).

## Contract stability

If the game changes an `EventBus` signal signature, update **both**
`TelemetryExporter.gd` and `EVENT_SCHEMA.md`. GCL's reader tolerates missing
optional fields and unknown extra fields, so additive changes are safe without a
GCL release.
