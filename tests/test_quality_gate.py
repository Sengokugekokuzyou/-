from gcl.telemetry.schema import Event
from gcl.story.detector import StoryCandidate
from gcl.packaging import build_script
from gcl.packaging.script_builder import ScriptLine
from gcl.quality import run_gate

CFG = {"quality_gate": {"min_width": 1920, "min_height": 1080,
                        "min_duration_seconds": 3}}


def _ev(eid, day, typ, vp=50):
    return Event(eid, 1, day, float(day), typ, "npc_0042", "glen", "glen",
                 (), (), vp)


def _candidate():
    return StoryCandidate("npc_0042", [
        _ev("e1", 1, "food_shortage"),
        _ev("e2", 3, "npc_theft", vp=72),
        _ev("e3", 5, "npc_exile", vp=70),
    ], "npc_chronicle")


def test_clean_render_passes():
    cand = _candidate()
    script = build_script(cand, question_ja="食料を失った村は？")
    res = run_gate(
        media_info={"width": 1920, "height": 1080, "duration": 12.0,
                    "has_audio": True},
        script_lines=script, title="glen の記録", candidate=cand, config=CFG,
    )
    verdicts = {c.name: c.verdict for c in res.checks}
    assert verdicts["technical.resolution"] == "PASS"
    assert verdicts["technical.audio_present"] == "PASS"
    assert verdicts["content.no_fabrication"] == "PASS"
    assert verdicts["content.has_result"] == "PASS"


def test_fabricated_line_fails():
    cand = _candidate()
    # An asserted line with no source event = fabrication.
    bad = [ScriptLine("Escalation", "村人は皆泣いていた", (), hedged=False)]
    res = run_gate(media_info={"width": 1920, "height": 1080, "duration": 5,
                              "has_audio": True},
                   script_lines=bad, title="glen", candidate=cand, config=CFG)
    assert res.verdict == "FAIL"
    assert any(c.name == "content.no_fabrication" and c.verdict == "FAIL"
               for c in res.checks)


def test_no_audio_fails():
    cand = _candidate()
    script = build_script(cand, question_ja="?")
    res = run_gate(media_info={"width": 1920, "height": 1080, "duration": 5,
                              "has_audio": False},
                   script_lines=script, title="glen", candidate=cand, config=CFG)
    assert res.verdict == "FAIL"


def test_title_day_mismatch_fails():
    cand = _candidate()  # spans day 1..5 → day_span 4
    script = build_script(cand, question_ja="?")
    res = run_gate(media_info={"width": 1920, "height": 1080, "duration": 5,
                              "has_audio": True},
                   script_lines=script, title="村の100日間", candidate=cand,
                   config=CFG)
    assert any(c.name == "content.title_consistency" and c.verdict == "FAIL"
               for c in res.checks)


def test_format_repeat_warns():
    cand = _candidate()
    script = build_script(cand, question_ja="?")
    res = run_gate(media_info={"width": 1920, "height": 1080, "duration": 5,
                              "has_audio": True},
                   script_lines=script, title="glen", candidate=cand, config=CFG,
                   previous_title_format="time", this_title_format="time")
    assert any(c.name == "content.title_format_rotation" and c.verdict == "WARN"
               for c in res.checks)
