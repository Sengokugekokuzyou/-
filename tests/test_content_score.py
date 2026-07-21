from collections import Counter

from gcl.telemetry.schema import Event
from gcl.story import detect_candidates, score_candidate
from gcl.story.detector import StoryCandidate


def _ev(eid, day, typ, actor="npc_0042", causes=(), vp=50, rel=None, emo=None):
    return Event(
        event_id=eid, world_seed=1, game_day=day, timestamp=float(day),
        type=typ, actor_id=actor, target_id=None, location_id="glen",
        cause_ids=tuple(causes), witness_ids=(), visual_priority=vp,
        relationship_delta=rel, emotion_delta=emo or {},
    )


def test_transformation_chain_scores_higher_than_flat():
    rich = StoryCandidate("npc_0042", [
        _ev("e1", 1, "food_shortage", vp=40),
        _ev("e2", 2, "npc_theft", causes=["e1"], vp=72, rel=-18, emo={"guilt": 31}),
        _ev("e3", 3, "npc_exile", causes=["e2"], vp=70, rel=-25, emo={"despair": 28}),
        _ev("e4", 4, "npc_turned_bandit", causes=["e3"], vp=78, rel=-12),
    ], "npc_chronicle")
    flat = StoryCandidate("npc_0009", [
        _ev("f1", 1, "rest", actor="npc_0009", vp=10),
        _ev("f2", 2, "rest", actor="npc_0009", vp=10),
    ], "npc_chronicle")

    hist = Counter()
    s_rich = score_candidate(rich, type_histogram=hist)
    s_flat = score_candidate(flat, type_histogram=hist)
    assert s_rich.total > s_flat.total
    assert s_rich.parts["transformation"] > s_flat.parts["transformation"]
    assert s_rich.parts["causality"] > s_flat.parts["causality"]


def test_score_within_bounds():
    c = StoryCandidate("npc_1", [
        _ev("e1", 1, "combat", vp=100, rel=999, emo={"x": 999}),
        _ev("e2", 2, "combat", causes=["e1"], vp=100),
    ], "npc_chronicle")
    sb = score_candidate(c)
    assert 0 <= sb.total <= 100
    for k, v in sb.parts.items():
        assert v >= 0


def test_tiers():
    from gcl.story.content_score import ScoreBreakdown
    assert ScoreBreakdown({"a": 90}).tier == "long_form"
    assert ScoreBreakdown({"a": 75}).tier == "shorts"
    assert ScoreBreakdown({"a": 60}).tier == "broll"
    assert ScoreBreakdown({"a": 40}).tier == "discard"


def test_detector_drops_too_short_actor():
    events = [
        _ev("e1", 1, "combat", actor="npc_active"),
        _ev("e2", 2, "combat", actor="npc_active", causes=["e1"]),
        _ev("s1", 1, "rest", actor="npc_lazy"),
    ]
    cands = detect_candidates(events, min_chain=2)
    actors = {c.protagonist for c in cands}
    assert "npc_active" in actors
    assert "npc_lazy" not in actors  # only 1 event → dropped
    assert None in actors            # world-level candidate present
