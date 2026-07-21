"""Content Score (§19) — a transparent, deterministic 100-point rubric.

    Causality       20
    Transformation  15
    Uncertainty     15
    Emotion         15
    Visuality       15
    Game Appeal     10
    Originality     10

Every sub-score is an explainable function of *recorded* facts, never an LLM
guess. The score never decides publication on its own (§19); it only ranks
candidates and routes them (>=85 long-form, 70-84 shorts, 55-69 b-roll, <=54
discard). The Quality Gate always has the final say.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field

from ..telemetry.schema import Event
from .detector import StoryCandidate, has_transformation

MAX = {
    "causality": 20,
    "transformation": 15,
    "uncertainty": 15,
    "emotion": 15,
    "visuality": 15,
    "game_appeal": 10,
    "originality": 10,
}

# Types that read well as a "game clip" rather than a stats table (§20, §26).
_VISUAL_GAMEPLAY_TYPES = frozenset({
    "combat", "raid", "village_defense", "npc_theft", "arrest", "hunt",
    "quest_spawn", "quest_success", "quest_fail", "wolf_relationship_change",
    "construction", "faction_join", "betrayal",
})


@dataclass
class ScoreBreakdown:
    parts: dict[str, float] = field(default_factory=dict)

    @property
    def total(self) -> float:
        return round(sum(self.parts.values()), 1)

    @property
    def tier(self) -> str:
        t = self.total
        if t >= 85:
            return "long_form"      # 通常/大型動画候補
        if t >= 70:
            return "shorts"         # Shorts/短編候補
        if t >= 55:
            return "broll"          # Bロール/Devlog/資料
        return "discard"           # 原則破棄

    def as_dict(self) -> dict:
        return {"total": self.total, "tier": self.tier, "parts": self.parts}


def score_candidate(
    candidate: StoryCandidate,
    *,
    type_histogram: Counter | None = None,
) -> ScoreBreakdown:
    """Score one candidate.

    ``type_histogram`` is the distribution of event types across *all* candidates
    in this batch; it powers Originality (rare combinations score higher), which
    is how we avoid publishing the same shape of video repeatedly (§2-6, §27).
    """
    evs = candidate.events
    parts: dict[str, float] = {}

    # Causality: how much of the chain is genuinely linked by recorded causes.
    linked = sum(1 for e in evs if e.cause_ids)
    depth = _max_cause_depth(evs)
    parts["causality"] = _clamp(
        (linked / max(1, len(evs))) * 12 + min(depth, 4) * 2, MAX["causality"]
    )

    # Transformation: did someone's state actually change?
    swing = sum(abs(e.relationship_delta or 0.0) for e in evs)
    parts["transformation"] = _clamp(
        (7 if has_transformation(candidate) else 0) + min(swing / 20.0, 1.0) * 8,
        MAX["transformation"],
    )

    # Uncertainty: variety of outcomes / mix of success & failure.
    types = set(e.type for e in evs)
    has_fail = any("fail" in t or t in {"death", "bankruptcy", "exile"} for t in types)
    has_win = any("success" in t or t in {"village_defense", "quest_success"} for t in types)
    parts["uncertainty"] = _clamp(
        min(len(types), 6) * 1.5 + (6 if (has_fail and has_win) else 0),
        MAX["uncertainty"],
    )

    # Emotion: magnitude of recorded emotional change.
    emo = sum(sum(abs(v) for v in e.emotion_delta.values()) for e in evs)
    parts["emotion"] = _clamp(min(emo / 60.0, 1.0) * MAX["emotion"], MAX["emotion"])

    # Visuality: how filmable the peak moments are.
    if evs:
        vp_avg = sum(e.visual_priority for e in evs) / len(evs)
        vp_peak = max(e.visual_priority for e in evs)
        parts["visuality"] = _clamp(
            (vp_avg / 100.0) * 9 + (vp_peak / 100.0) * 6, MAX["visuality"]
        )
    else:
        parts["visuality"] = 0.0

    # Game Appeal: presence of recognisably-gameplay moments.
    gameplay = sum(1 for e in evs if e.type in _VISUAL_GAMEPLAY_TYPES)
    parts["game_appeal"] = _clamp(min(gameplay, 5) * 2, MAX["game_appeal"])

    # Originality: rarer type-combinations score higher.
    parts["originality"] = _originality(evs, type_histogram)

    return ScoreBreakdown(parts={k: round(v, 1) for k, v in parts.items()})


def _originality(evs: list[Event], hist: Counter | None) -> float:
    if not evs:
        return 0.0
    if not hist:
        # No corpus to compare against yet → neutral-high (benefit of the doubt).
        return round(MAX["originality"] * 0.6, 1)
    total = sum(hist.values()) or 1
    # Average rarity of this candidate's types (1 - frequency).
    rarity = sum(1.0 - hist.get(e.type, 0) / total for e in evs) / len(evs)
    return _clamp(rarity * MAX["originality"], MAX["originality"])


def _max_cause_depth(evs: list[Event]) -> int:
    by_id = {e.event_id: e for e in evs}
    memo: dict[str, int] = {}

    def depth(eid: str, seen: frozenset[str]) -> int:
        if eid in memo:
            return memo[eid]
        e = by_id.get(eid)
        if not e or not e.cause_ids:
            return 0
        best = 0
        for c in e.cause_ids:
            if c in seen or c not in by_id:
                continue
            best = max(best, 1 + depth(c, seen | {eid}))
        memo[eid] = best
        return best

    return max((depth(e.event_id, frozenset()) for e in evs), default=0)


def _clamp(v: float, hi: float) -> float:
    return max(0.0, min(v, hi))
