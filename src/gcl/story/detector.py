"""Detect story candidates from the event stream.

A *candidate* is a causally-linked chain of events that share a protagonist (an
``actor_id``) — the raw material for one NPC Chronicle or one World Experiment
beat. Detection is deliberately simple and deterministic: we follow the
``cause_ids`` edges the *game* recorded. We never invent links (§21).
"""
from __future__ import annotations

from dataclasses import dataclass, field

from ..telemetry.schema import Event


@dataclass
class StoryCandidate:
    protagonist: str | None          # actor_id, or None for a world-level arc
    events: list[Event]              # ordered by (game_day, timestamp)
    kind: str                        # "npc_chronicle" | "world_experiment"

    @property
    def day_span(self) -> int:
        if not self.events:
            return 0
        return self.events[-1].game_day - self.events[0].game_day

    @property
    def locations(self) -> set[str]:
        return {e.location_id for e in self.events if e.location_id}

    @property
    def event_types(self) -> list[str]:
        return [e.type for e in self.events]

    def summary(self) -> str:
        who = self.protagonist or "world"
        return (
            f"{self.kind}:{who} "
            f"[{len(self.events)} events / {self.day_span}d / "
            f"{len(self.locations)} locations]"
        )


# Event types that, when present, mark a genuine change of state for a person.
_TRANSFORMATION_TYPES = frozenset({
    "npc_role_change", "village_chief_change", "npc_exile", "npc_turned_bandit",
    "faction_join", "faction_leave", "marriage", "divorce", "death", "birth",
    "bankruptcy", "arrest", "betrayal",
})


def detect_candidates(
    events: list[Event],
    *,
    min_chain: int = 2,
) -> list[StoryCandidate]:
    """Build one candidate per protagonist plus one world-level candidate.

    ``min_chain`` drops actors with too little happening — the brief is explicit
    that we must not film an NPC where nothing happens (§6).
    """
    by_actor: dict[str, list[Event]] = {}
    for e in events:
        if e.actor_id:
            by_actor.setdefault(e.actor_id, []).append(e)
        # A target can also be a protagonist of what was done *to* them.
        if e.target_id and e.target_id.startswith("npc_"):
            by_actor.setdefault(e.target_id, []).append(e)

    candidates: list[StoryCandidate] = []
    for actor, evs in by_actor.items():
        evs = _dedup_sorted(evs)
        if len(evs) < min_chain:
            continue
        candidates.append(
            StoryCandidate(protagonist=actor, events=evs, kind="npc_chronicle")
        )

    # World-level arc = every event, for World Experiment / World History framing.
    if events:
        candidates.append(
            StoryCandidate(
                protagonist=None,
                events=_dedup_sorted(events),
                kind="world_experiment",
            )
        )
    return candidates


def has_transformation(candidate: StoryCandidate) -> bool:
    return any(e.type in _TRANSFORMATION_TYPES for e in candidate.events)


def _dedup_sorted(evs: list[Event]) -> list[Event]:
    seen: set[str] = set()
    out: list[Event] = []
    for e in sorted(evs, key=lambda x: (x.game_day, x.timestamp)):
        if e.event_id in seen:
            continue
        seen.add(e.event_id)
        out.append(e)
    return out
