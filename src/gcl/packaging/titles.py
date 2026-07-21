"""Title candidate generation (§25/§5) — template driven, format-rotated.

Six title formats are rotated so we never publish the same shape twice in a row
(§2-6, §27 "同じタイトル形式を連続使用しない"). Titles are filled only from
recorded facts (day count, location, event label) so they can never over-promise
something the video does not show (§25 "実際に起きた内容と一致").
"""
from __future__ import annotations

from ..story.detector import StoryCandidate

FORMATS = ("question", "result", "time", "person", "conflict", "change")


def _facts(candidate: StoryCandidate) -> dict:
    evs = candidate.events
    peak = max(evs, key=lambda e: e.visual_priority) if evs else None
    loc = next((e.location_id for e in evs if e.location_id), "村")
    return {
        "days": candidate.day_span or (evs[-1].game_day if evs else 0),
        "location": loc,
        "peak_type": peak.type if peak else "",
        "who": candidate.protagonist or loc,
        "n_events": len(evs),
    }


def title_candidates(
    candidate: StoryCandidate,
    *,
    question_ja: str,
    avoid_formats: tuple[str, ...] = (),
    n: int = 10,
) -> list[dict]:
    """Return up to ``n`` JP title candidates, each tagged with its format.

    ``avoid_formats`` is the format(s) used by the previous uploads — those are
    pushed to the end so the rotation constraint is respected.
    """
    f = _facts(candidate)
    days, loc = f["days"], f["location"]

    bank: dict[str, list[str]] = {
        "question": [
            question_ja,
            f"{loc}はこの後どうなるのか？",
        ],
        "result": [
            f"{loc}で起きたことの結末",
            f"記録が示した{loc}の顛末",
        ],
        "time": [
            f"{loc}の{days}日間",
            f"{days}日で変わった{loc}",
        ],
        "person": [
            f"ある{('村人' if candidate.protagonist else '村')}の記録",
            f"{f['who']}に起きたこと",
        ],
        "conflict": [
            f"{loc}を揺るがした対立の記録",
            f"{loc}で何が争いを生んだのか",
        ],
        "change": [
            f"{loc}はどう変わったのか",
            f"{days}日間の変化を追う",
        ],
    }

    return _round_robin(bank, FORMATS, avoid_formats, n)


def english_title_candidates(
    candidate: StoryCandidate,
    *,
    question_en: str = "",
    avoid_formats: tuple[str, ...] = (),
    n: int = 10,
) -> list[dict]:
    """EN title candidates (§25 wants 10 EN titles too). Facts-only fills."""
    f = _facts(candidate)
    days, loc = f["days"], f["location"]
    q = question_en or f"What Happened in {loc}?"
    bank: dict[str, list[str]] = {
        "question": [q, f"What Becomes of {loc}?"],
        "result": [f"How It Ended in {loc}", f"The Fate of {loc}, on Record"],
        "time": [f"{days} Days in {loc}", f"{loc}, in {days} Days"],
        "person": ["One Villager's Record", f"What Happened to {f['who']}"],
        "conflict": [f"The Conflict That Shook {loc}", f"What Sparked the Strife in {loc}"],
        "change": [f"How {loc} Changed", f"Tracing {days} Days of Change"],
    }
    return _round_robin(bank, FORMATS, avoid_formats, n)


def _round_robin(bank, formats, avoid_formats, n):
    ordered = [fmt for fmt in formats if fmt not in avoid_formats] + list(avoid_formats)
    out: list[dict] = []
    # Round-robin across formats so the top candidates are format-diverse.
    idx = 0
    while len(out) < n:
        progressed = False
        for fmt in ordered:
            options = bank.get(fmt, [])
            if idx < len(options):
                out.append({"format": fmt, "text": options[idx]})
                progressed = True
                if len(out) >= n:
                    break
        if not progressed:
            break
        idx += 1
    return out
