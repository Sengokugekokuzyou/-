"""Narrative Builder (§21) — fact-anchored, never fabricated.

Every line the narrator says carries the ``event_id`` (or ids) it was derived
from. That provenance is what the Quality Gate checks: a line with no source is
a fabrication and fails the gate. Where we interpret rather than state, we use
the hedged phrasings the brief mandates ("〜した可能性があります" / "ログ上では〜").

The structure follows §21: Hook, Question, Setup, Escalation, Focus, Turning
Point, Result, Interpretation, Steam CTA.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from ..telemetry.schema import Event
from ..story.detector import StoryCandidate

# Human-readable, localisation-key-style labels for event types. In the real
# pipeline these resolve through the game's LocalizationManager catalogue; here
# we keep a small JP map so the sample output is legible.
_TYPE_JP = {
    "npc_theft": "盗みを働いた",
    "arrest": "捕らえられた",
    "npc_exile": "村を追放された",
    "npc_turned_bandit": "盗賊になった",
    "combat": "戦闘になった",
    "village_defense": "村を守る戦いが起きた",
    "raid": "襲撃を受けた",
    "food_shortage": "食料不足に陥った",
    "price_rise": "食料価格が上がった",
    "rumor_spread": "噂が広まった",
    "betrayal": "裏切りが起きた",
    "quest_fail": "依頼に失敗した",
    "quest_success": "依頼を果たした",
    "wolf_relationship_change": "狼との関係が変わった",
    "death": "命を落とした",
    "faction_join": "徒党に加わった",
}


@dataclass
class ScriptLine:
    section: str          # Hook / Question / ... (§21)
    text: str             # narration text (ja)
    source_event_ids: tuple[str, ...] = ()   # provenance — empty = fabrication
    hedged: bool = False  # True when this is interpretation, not assertion

    def as_dict(self) -> dict:
        return {
            "section": self.section,
            "text": self.text,
            "source_event_ids": list(self.source_event_ids),
            "hedged": self.hedged,
        }


def _label(e: Event) -> str:
    return _TYPE_JP.get(e.type, e.type)


def build_script(
    candidate: StoryCandidate,
    *,
    question_ja: str,
    steam_url: str = "",
) -> list[ScriptLine]:
    evs = candidate.events
    if not evs:
        return []

    first, last = evs[0], evs[-1]
    who = candidate.protagonist or "この村"
    lines: list[ScriptLine] = []

    # Hook — the most visually-striking / highest-priority moment, stated plainly.
    peak = max(evs, key=lambda e: e.visual_priority)
    lines.append(ScriptLine(
        "Hook",
        f"{peak.game_day}日目、{_label(peak)}。",
        (peak.event_id,),
    ))

    # Question — comes from the experiment definition, not invented.
    lines.append(ScriptLine("Question", question_ja))

    # Setup — where and who, factual.
    loc = first.location_id or "ある村"
    lines.append(ScriptLine(
        "Setup",
        f"舞台は{loc}。記録は{first.game_day}日目から始まります。",
        (first.event_id,),
    ))

    # Escalation — the recorded chain, in order. Causes are only stated when the
    # game recorded them (§21: no fabricated causality).
    for e in evs[1:-1]:
        if e.cause_ids:
            lines.append(ScriptLine(
                "Escalation",
                f"{e.game_day}日目、{_label(e)}。"
                f"ログ上では直前に別の出来事が影響したと記録されています。",
                tuple([e.event_id, *e.cause_ids]),
                hedged=True,
            ))
        else:
            lines.append(ScriptLine(
                "Escalation",
                f"{e.game_day}日目、{_label(e)}。",
                (e.event_id,),
            ))

    # Turning Point — the transformation event if there is one, else the peak.
    lines.append(ScriptLine(
        "Turning Point",
        f"{peak.game_day}日目、{_label(peak)}。ここが転機でした。",
        (peak.event_id,),
    ))

    # Result — the last recorded state. No exaggeration (§21).
    lines.append(ScriptLine(
        "Result",
        f"{last.game_day}日目時点の記録では、{_label(last)}。",
        (last.event_id,),
    ))

    # Interpretation — hedged, never asserted.
    lines.append(ScriptLine(
        "Interpretation",
        f"{who}に何が起きたのか。断定はできませんが、"
        f"一連の記録からはひとつの因果が読み取れます。",
        tuple(e.event_id for e in evs),
        hedged=True,
    ))

    # Steam CTA.
    if steam_url:
        lines.append(ScriptLine(
            "Steam CTA",
            f"GEKOKUJO: Vagrant Crown の世界はSteamで。{steam_url}",
        ))
    return lines
