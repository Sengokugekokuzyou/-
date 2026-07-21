"""Event schema — a 1:1 Python mirror of the JSONL the game emits.

The canonical definition lives in ``docs/EVENT_SCHEMA.md`` and must stay in sync
with ``godot_bridge/telemetry_export/TelemetryExporter.gd``. Keeping this a plain
dataclass (no validation framework) keeps the dependency surface tiny, which the
project brief (§9 "no monthly-fee services", §32 non-functional reqs) asks for.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

# §15: these must always be present. Event-specific fields may be null / empty.
REQUIRED_FIELDS = (
    "event_id",
    "world_seed",
    "game_day",
    "timestamp",
    "type",
    "actor_id",
    "target_id",
    "location_id",
    "cause_ids",
    "witness_ids",
    "visual_priority",
)


@dataclass(frozen=True)
class Event:
    """One recorded world event.

    ``cause_ids`` is the anti-fabrication backbone (§21): the Narrative Builder
    is only ever allowed to assert causality that the game itself recorded here.
    """

    event_id: str
    world_seed: int
    game_day: int
    timestamp: float
    type: str
    actor_id: str | None
    target_id: str | None
    location_id: str | None
    cause_ids: tuple[str, ...] = ()
    witness_ids: tuple[str, ...] = ()
    visual_priority: int = 0
    relationship_delta: float | None = None
    emotion_delta: dict[str, float] = field(default_factory=dict)
    # Anything the game adds that we do not model yet is preserved verbatim so
    # future stages can use it without a schema migration.
    extra: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "Event":
        missing = [f for f in REQUIRED_FIELDS if f not in raw]
        if missing:
            raise ValueError(
                f"event {raw.get('event_id', '<no id>')} missing required "
                f"fields: {', '.join(missing)}"
            )
        known = set(REQUIRED_FIELDS) | {"relationship_delta", "emotion_delta"}
        return cls(
            event_id=str(raw["event_id"]),
            world_seed=int(raw["world_seed"]),
            game_day=int(raw["game_day"]),
            timestamp=float(raw["timestamp"]),
            type=str(raw["type"]),
            actor_id=_opt_str(raw["actor_id"]),
            target_id=_opt_str(raw["target_id"]),
            location_id=_opt_str(raw["location_id"]),
            cause_ids=tuple(raw.get("cause_ids") or ()),
            witness_ids=tuple(raw.get("witness_ids") or ()),
            visual_priority=int(raw.get("visual_priority") or 0),
            relationship_delta=_opt_float(raw.get("relationship_delta")),
            emotion_delta=dict(raw.get("emotion_delta") or {}),
            extra={k: v for k, v in raw.items() if k not in known},
        )


def _opt_str(v: Any) -> str | None:
    return None if v is None else str(v)


def _opt_float(v: Any) -> float | None:
    return None if v is None else float(v)
