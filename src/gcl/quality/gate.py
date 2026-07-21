"""Quality Gate — the check every video must pass before publish (§27, §28).

Verdicts:
  PASS  → eligible for scheduled/private upload
  WARN  → export privately + write a report; human review required
  FAIL  → regenerate or discard; never publish

The gate is the final authority — a high Content Score cannot bypass it (§19).
We only implement checks that are *decidable from data we actually have*; each
skipped check is reported, not silently assumed to pass (§ "報告は忠実に").
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

PASS, WARN, FAIL = "PASS", "WARN", "FAIL"
_SEVERITY = {PASS: 0, WARN: 1, FAIL: 2}


@dataclass
class Check:
    name: str
    verdict: str
    detail: str = ""

    def as_dict(self) -> dict:
        return {"name": self.name, "verdict": self.verdict, "detail": self.detail}


@dataclass
class GateResult:
    checks: list[Check] = field(default_factory=list)

    @property
    def verdict(self) -> str:
        if not self.checks:
            return WARN
        return max((c.verdict for c in self.checks), key=lambda v: _SEVERITY[v])

    def add(self, name: str, verdict: str, detail: str = "") -> None:
        self.checks.append(Check(name, verdict, detail))

    def as_dict(self) -> dict:
        return {
            "verdict": self.verdict,
            "checks": [c.as_dict() for c in self.checks],
        }


def run_gate(
    *,
    media_info: dict | None,
    script_lines: list[Any],
    title: str,
    candidate,
    config: dict,
    previous_title_format: str | None = None,
    this_title_format: str | None = None,
) -> GateResult:
    r = GateResult()
    q = config.get("quality_gate", {})

    # ── Technical ────────────────────────────────────────────────────────────
    if media_info is None:
        r.add("technical.probe", WARN, "no media info (dry-run or probe failed)")
    else:
        w, h = media_info.get("width"), media_info.get("height")
        want_w = q.get("min_width", 1920)
        want_h = q.get("min_height", 1080)
        if w and h:
            if w >= want_w and h >= want_h:
                r.add("technical.resolution", PASS, f"{w}x{h}")
            else:
                r.add("technical.resolution", FAIL, f"{w}x{h} < {want_w}x{want_h}")
        else:
            r.add("technical.resolution", WARN, "resolution unknown")

        dur = media_info.get("duration")
        min_dur = q.get("min_duration_seconds", 3)
        if dur is None:
            r.add("technical.duration", WARN, "duration unknown")
        elif dur >= min_dur:
            r.add("technical.duration", PASS, f"{dur:.1f}s")
        else:
            r.add("technical.duration", FAIL, f"{dur:.1f}s < {min_dur}s")

        if media_info.get("has_audio"):
            r.add("technical.audio_present", PASS)
        else:
            r.add("technical.audio_present", FAIL, "no audio stream")

    # ── Content ──────────────────────────────────────────────────────────────
    # No fabrication: every asserted (non-hedged, non-CTA/Question) line must
    # cite at least one source event (§21).
    exempt = {"Question", "Steam CTA"}
    unsourced = [
        ln for ln in script_lines
        if getattr(ln, "section", "") not in exempt
        and not getattr(ln, "hedged", False)
        and not getattr(ln, "source_event_ids", ())
    ]
    if unsourced:
        r.add(
            "content.no_fabrication", FAIL,
            f"{len(unsourced)} asserted line(s) with no source event",
        )
    else:
        r.add("content.no_fabrication", PASS)

    # A result must exist (§21 "結末が存在する").
    if any(getattr(ln, "section", "") == "Result" for ln in script_lines):
        r.add("content.has_result", PASS)
    else:
        r.add("content.has_result", FAIL, "no Result section")

    # Title-result consistency: the day span / location referenced by the title
    # must actually appear in the candidate's events (§25/§27).
    r.add(*_title_consistency(title, candidate))

    # Format rotation: don't reuse the previous upload's title format (§27).
    if (
        previous_title_format
        and this_title_format
        and previous_title_format == this_title_format
    ):
        r.add(
            "content.title_format_rotation", WARN,
            f"same title format as previous upload ({this_title_format})",
        )
    else:
        r.add("content.title_format_rotation", PASS)

    return r


def _title_consistency(title: str, candidate) -> tuple[str, str, str]:
    locs = candidate.locations
    if any(loc and loc in title for loc in locs):
        return ("content.title_consistency", PASS, "title references a real location")
    # A day-count in the title must match the recorded span.
    import re

    m = re.search(r"(\d+)\s*日", title)
    if m:
        if int(m.group(1)) == candidate.day_span or int(m.group(1)) == (
            candidate.events[-1].game_day if candidate.events else -1
        ):
            return ("content.title_consistency", PASS, "day count matches record")
        return (
            "content.title_consistency", FAIL,
            f"title says {m.group(1)}日 but record spans {candidate.day_span}日",
        )
    return (
        "content.title_consistency", WARN,
        "could not verify title against events (no location/day match)",
    )
