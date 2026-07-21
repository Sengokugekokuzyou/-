# REPLAY_DESIGN (§17)

Goal: after a headless simulation surfaces an interesting event, return to just
before it and **re-shoot** it with cameras — rather than relying on real-time
recording of the first run.

## Staged approach (do NOT block on full determinism, §17)

Implement in this order; each stage is independently useful:

1. **Periodic save** — the sim autosaves every N in-game days. Cheapest; lets GCL
   reload near an event.
2. **Pre-event autosave** — when the game emits a high-`visual_priority` event,
   snapshot immediately before it. Enables tight re-entry.
3. **Scenario re-run** — re-launch from `world_seed` + a scripted setup to
   reproduce the situation approximately. Good enough for most re-shoots.
4. **Approximate reproduction** — reload the nearest save and let the sim run;
   accept minor divergence.
5. **Full deterministic replay** — seed + RNG state + full world state restored
   for frame-exact reproduction. Highest cost; last.

GCL only needs the `world_seed` (already in every event) and a save/reload entry
point. The exporter records the seed; the game side provides the reload hook.

## Information to restore for a faithful re-shoot (§17)
world seed · in-game time · weather · NPC positions/states · relationship values ·
event state · RNG state · combat state · camera target · animation state.

Stages 1–3 cover most content; stages 4–5 are refinements for flagship pieces.

## GCL side (Phase 3)
- A `replay` command that, given an `event_id`, asks the game to reload the nearest
  pre-event save, sets a camera preset (§20), and dumps a frame sequence for the
  window `[event_day-1 .. event_day+1]`.
- Vertical re-framing for Shorts is a re-shoot with a portrait camera, not a crop
  (§24).
