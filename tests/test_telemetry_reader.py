import json

import pytest

from gcl.telemetry import read_events
from gcl.telemetry.reader import ReaderError


def _write(tmp_path, lines):
    p = tmp_path / "t.jsonl"
    p.write_text("\n".join(lines), encoding="utf-8")
    return p


def _valid(**over):
    base = {
        "event_id": "evt_1", "world_seed": 1, "game_day": 2, "timestamp": 1.0,
        "type": "combat", "actor_id": "npc_1", "target_id": "npc_2",
        "location_id": "glen", "cause_ids": [], "witness_ids": [],
        "visual_priority": 50,
    }
    base.update(over)
    return json.dumps(base, ensure_ascii=False)


def test_reads_valid_events_sorted(tmp_path):
    p = _write(tmp_path, [
        _valid(event_id="evt_b", game_day=3, timestamp=1.0),
        _valid(event_id="evt_a", game_day=2, timestamp=9.0),
    ])
    res = read_events(p)
    assert [e.event_id for e in res.events] == ["evt_a", "evt_b"]
    assert res.skipped == []


def test_skips_malformed_line_non_strict(tmp_path):
    p = _write(tmp_path, ["{not json}", _valid()])
    res = read_events(p)
    assert len(res.events) == 1
    assert len(res.skipped) == 1


def test_missing_required_field_reported(tmp_path):
    bad = json.dumps({"event_id": "x", "type": "combat"})
    p = _write(tmp_path, [bad])
    res = read_events(p)
    assert res.events == []
    assert "missing required" in res.skipped[0][1]


def test_strict_raises(tmp_path):
    p = _write(tmp_path, ["{bad}"])
    with pytest.raises(ReaderError):
        read_events(p, strict=True)


def test_missing_file():
    with pytest.raises(ReaderError):
        read_events("/no/such/file.jsonl")
