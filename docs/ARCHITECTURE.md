# ARCHITECTURE — GEKOKUJO Content Lab

## Phase 0 finding (the headline)

**~60–70% of the substrate GCL needs already exists inside the GEKOKUJO game.**
GCL is therefore mostly a *connection + post-production* layer, not a from-scratch
build of 16 subsystems. This document maps every GCL module to the game code that
already backs it, based on a read of the `Sengokugekokuzyou/Vagrant-Crown` repo.

### What the game already provides

| GCL need (brief §) | Existing game code | Notes |
|---|---|---|
| World simulation / pseudo-player (§5, §6) | `scripts/world/pseudo_player/PseudoPlayerBrain.gd` (647 LOC), `PseudoPlayerManager.gd`, `UtilityEvaluator.gd`, `FragmentRegistry.gd`, `ActionRegistry.gd` | Utility-AI NPCs already live autonomously. This is the engine that generates emergent stories. |
| Telemetry hook (§15) | `scripts/world/pseudo_player/EventBus.gd` | Emits `day_passed`, `action_executed`, `world_event`, `npc_state_changed`. GCL only needs to subscribe. |
| Narrative source (§21) | `scripts/world/pseudo_player/NpcLifeNarrator.gd` | Already builds story sentences from `memory_log` as a **pure, side-effect-free function** — i.e. it already respects "no fabrication". |
| Event catalogue (§16) | `data/events/north_forest_events.json`, `scripts/world/event/{EventGenerator,WorldEventGenerator,NPCEventGenerator}.gd` | Structured events with `cause`/`outcome`/`rumor` links. |
| Rumor / faction / politics (§16) | `scripts/world/rumor/RumorSystem.gd`, `PoliticalSystem.gd`, `scripts/world/strategic/StrategicBattleSystem.gd` | The relationship/conflict substance for World Experiments. |
| Capture (§20, §24) | `scenes/tools/strategic_capture.tscn`, `capture_strategic.bat`, `_milmap_capture.bat` | Headless still capture of the strategic map already works (overview/mid/near). |
| Headless sim harness (§18) | `scenes/tools/soak_probe.tscn`, `run_soak_map.bat`, `scripts/tools/test/SoakTest.gd` | Runs the map headless for N seconds with logging — the "run many simulations" harness. |
| File logging to `user://` | `PseudoPlayerManager.gd` (writes `user://phase0a_debug.log`) | Proves the write path GCL telemetry uses. |
| World history view (§7) | `scripts/world/map/WorldHistoryPanel.gd`, `scripts/world/news/WorldNewsSystem.gd` | Basis for World History / Movie content. |

### What GCL adds (the actually-new work)

1. **Telemetry export** — a non-invasive autoload subscribing to `EventBus`,
   writing §15 JSONL. Lives in the game repo but ships OFF by default.
   → `godot_bridge/telemetry_export/TelemetryExporter.gd`
2. **Post-production pipeline (Python, this repo)** — detection, Content Score,
   fact-anchored script, FFmpeg editing, Quality Gate, packaging, publishing.
3. **Video-grade capture** — extend still capture to a numbered frame sequence /
   recorded clip (the strategic-map path first; 3D third-person in Early Access).

## Timeline reality (drives sequencing)

- **Demo (体験版) = strategic map (軍略マップ).** Everything filmable *now* is the
  strategic map — which is exactly what `strategic_capture` / `soak_probe` already
  render. So the first realistic video is a **World Experiment on the strategic
  map**, not a third-person BGM MV.
- **Early Access = 3D third-person.** BGM MV, Scenic Journey, and NPC Chronicle
  third-person re-shoots unlock here. GCL's camera presets (§20) and BGM MV
  Director (§11) are specced now, implemented when 3D lands.

Consequence: the brief's validation order A→B→C is inverted in practice to
**C (small strategic-map experiment) → A (third-person) → B (BGM MV)**.

## Data flow (v0.1, implemented)

```
GEKOKUJO game (headless soak run, GCL_TELEMETRY=1)
   │  EventBus signals
   ▼
TelemetryExporter.gd ──► user://gcl_telemetry/*.jsonl
   │  (copy to workspace/telemetry/)
   ▼
gcl.telemetry.reader ──► Event objects
   ▼
gcl.story.detector ──► StoryCandidate[]
   ▼
gcl.story.content_score ──► ranked candidates (§19 rubric)
   ▼
gcl.packaging (script_builder + titles)   ← fact-anchored, provenance per line
   ▼
gcl.editing.assembler ──► FFmpeg ──► workspace/renders/<job>/video.mp4
   ▼
gcl.quality.gate ──► PASS / WARN / FAIL  ← final authority, score cannot bypass
   ▼
workspace/renders/<job>/report.json
```

## Design rules baked into the code

- **No fabrication is enforced, not just documented.** Every asserted script line
  carries `source_event_ids`; the Quality Gate FAILs any asserted line without a
  source (`gcl/quality/gate.py :: content.no_fabrication`).
- **Causality only from recorded `cause_ids`** — the detector and script builder
  never invent links (§21).
- **The score never publishes.** It only ranks/routes; the Quality Gate decides
  (§19).
- **No hardcoded absolute paths.** All paths resolve from `config/` relative to
  the project root, overridable for the Windows box (§32).
- **Outputs never overwritten.** Each run gets a `job_id` directory (§32).
- **Game integrity is untouchable.** GCL reads telemetry and frames; it never
  writes to the game or its saves, and never tunes balance for YouTube (§29, §33).

## Module dependency sketch

```
telemetry ─┐
           ├─► story ─┐
config ────┤          ├─► packaging ─┐
           │          │              ├─► (cli orchestrates) ─► quality ─► report
editing ───┴──────────┴──────────────┘
```
`editing` depends only on FFmpeg discovery; `story`/`packaging`/`quality` are pure
Python over `Event`/`StoryCandidate` and are fully unit-tested.
