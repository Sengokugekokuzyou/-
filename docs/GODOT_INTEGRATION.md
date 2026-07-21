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

## 2. Frame capture (to extend)

Today `strategic_capture.tscn` writes stills (overview/mid/near). For video, GCL
needs a **numbered frame sequence** (`frame_%05d.png`) or a recorded clip. Two
options, cheapest first:

1. **Frame-dump loop** — a capture scene that advances the sim by a fixed dt and
   calls `get_viewport().get_texture().get_image().save_png()` each step. Fully
   deterministic, resolution-controlled, headless-friendly. Recommended first.
2. **Godot Movie Maker mode** (`--write-movie`) — records the running scene to
   frames/audio at a fixed FPS. Good for real-time third-person capture in EA.

GCL consumes either: point `--frames` at the output directory. `tools/make_placeholder_frames.py`
emulates option 1 until the capture scene exists.

## 3. Re-simulation / replay (Phase 3)

`world_seed` + recorded events let GCL ask the game to re-run a scenario for
re-shooting (§17). See `REPLAY_DESIGN.md` for the staged approach (periodic save →
pre-event autosave → scenario re-run → approximate → full deterministic replay).

## Contract stability

If the game changes an `EventBus` signal signature, update **both**
`TelemetryExporter.gd` and `EVENT_SCHEMA.md`. GCL's reader tolerates missing
optional fields and unknown extra fields, so additive changes are safe without a
GCL release.
