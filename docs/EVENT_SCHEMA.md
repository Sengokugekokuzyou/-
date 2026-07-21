# EVENT_SCHEMA — telemetry contract (§15)

One JSON object per line (JSONL), UTF-8. Written by
`godot_bridge/telemetry_export/TelemetryExporter.gd`, read by
`gcl.telemetry.reader`. This file is the single source of truth; the Godot
exporter and `gcl/telemetry/schema.py` must both match it.

## Example

```json
{
  "event_id": "evt_0001842",
  "world_seed": 482913,
  "game_day": 38,
  "timestamp": 9284.51,
  "type": "npc_theft",
  "actor_id": "npc_0042",
  "target_id": "store_0003",
  "location_id": "north_village",
  "cause_ids": ["evt_0001731", "evt_0001794"],
  "witness_ids": ["npc_0012", "npc_0091"],
  "relationship_delta": -18,
  "emotion_delta": { "fear": 12, "guilt": 31 },
  "visual_priority": 72
}
```

## Fields

| Field | Type | Required | Meaning |
|---|---|---|---|
| `event_id` | string | ✅ | Unique, stable id (`evt_NNNNNNN`). |
| `world_seed` | int | ✅ | Seed of the world run — enables re-simulation (§17). |
| `game_day` | int | ✅ | In-game day. |
| `timestamp` | float | ✅ | Seconds since session start (ordering within a day). |
| `type` | string | ✅ | Event type (see list below). |
| `actor_id` | string \| null | ✅ | Who acted (`null` for ambient/world events). |
| `target_id` | string \| null | ✅ | Who/what was acted upon. |
| `location_id` | string \| null | ✅ | Where. Drives camera/framing. |
| `cause_ids` | string[] | ✅ | Ids of events that caused this one. **Empty is allowed; fabricated is not.** The anti-fabrication backbone (§21). |
| `witness_ids` | string[] | ✅ | NPCs who saw it. |
| `visual_priority` | int 0–100 | ✅ | How filmable this moment is (§20, §26). |
| `relationship_delta` | float \| null | — | Net relationship change. Powers Transformation score. |
| `emotion_delta` | object | — | `{emotion: magnitude}`. Powers Emotion score. |

Unknown extra fields are preserved verbatim (`Event.extra`) so the game can add
data ahead of GCL modelling it, with no schema migration.

## Recorded event types (§16)

Minimum set the game should emit. GCL tolerates any string; these are the ones the
detector/score/narrator understand today:

`birth, death, injury, recovery, marriage, divorce, friendship, hostility,
betrayal, romance, mentorship, rumor_spread, npc_theft, arrest, npc_exile,
npc_turned_bandit, faction_join, faction_leave, combat, raid, bandit_raid,
village_defense, construction, village_growth, village_decline, trade,
bankruptcy, food_shortage, famine, price_rise, population_change,
npc_role_change, village_chief_change, quest_spawn, quest_success, quest_fail,
wolf_relationship_change, item_acquire, location_discover`

Not every event needs to become a video (§16). The score decides relevance.

## Quality expectations

- **Record `cause_ids` wherever the game already knows the cause.** This is the
  single highest-value field: GCL can only report causality you record.
- **Set `visual_priority` honestly** — it directly affects Hook/Turning-Point
  selection and shot planning.
- A single malformed line is skipped and reported, never silently dropped
  (`gcl.telemetry.reader`), so data loss is visible.
