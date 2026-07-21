from gcl.telemetry.schema import Event
from gcl.story.detector import StoryCandidate
from gcl.packaging import build_package
from gcl.packaging.description import build_chapters, thumbnail_texts
from gcl.editing.assembler import AssembleSpec, count_frames, input_framerate


def _ev(eid, day, typ, vp=50, loc="glen_village"):
    return Event(eid, 1, day, float(day), typ, "npc_0042", "glen", loc, (), (), vp)


def _candidate():
    return StoryCandidate("npc_0042", [
        _ev("e1", 1, "food_shortage"),
        _ev("e2", 3, "npc_theft", vp=72),
        _ev("e3", 5, "npc_exile", vp=70),
    ], "npc_chronicle")


def test_chapters_from_segments_start_at_zero():
    segs = [
        {"section": "Hook", "start": 4.0, "text": "a"},
        {"section": "Setup", "start": 9.0, "text": "b"},
        {"section": "Setup", "start": 12.0, "text": "c"},
        {"section": "Result", "start": 40.0, "text": "d"},
    ]
    ch = build_chapters(segs)
    assert ch[0]["time"] == "0:00"           # first forced to 0:00
    assert [c["label"] for c in ch] == ["異変", "舞台", "結果"]  # grouped by section


def test_build_package_fields_and_facts():
    cand = _candidate()
    pkg = build_package(
        cand, chosen_title={"format": "time", "text": "glen_villageの4日間"},
        question_ja="食料を失った村は？",
        narration_segments=[{"section": "Hook", "start": 0.0, "text": "x"}],
        steam_url="https://store.steampowered.com/app/4891620/",
        tts_credit="VOICEVOX:冥鳴ひまり", playlist="GEKOKUJO World Experiments",
    )
    assert len(pkg.titles_ja) >= 6
    assert len(pkg.titles_en) >= 6
    assert 1 <= len(pkg.thumbnail_texts) <= 5
    assert "VOICEVOX:冥鳴ひまり" in pkg.description
    assert "store.steampowered.com" in pkg.description


def test_thumbnail_texts_short_and_deduped():
    texts = thumbnail_texts(_candidate())
    assert len(texts) == len(set(texts))
    assert all(len(t) <= 12 for t in texts)


def test_input_framerate_matches_target(tmp_path):
    for i in range(60):
        (tmp_path / f"frame_{i:05d}.png").write_bytes(b"x")
    assert count_frames(tmp_path, "frame_%05d.png") == 60
    spec = AssembleSpec(frames_glob="frame_%05d.png", frames_dir=str(tmp_path),
                        fps=30, target_duration=30.0)
    # 60 frames over 30s → 2 fps input so the sequence lasts exactly the audio.
    assert input_framerate(spec) == 2.0


def test_input_framerate_defaults_to_fps_without_target(tmp_path):
    spec = AssembleSpec(frames_glob="frame_%05d.png", frames_dir=str(tmp_path), fps=24)
    assert input_framerate(spec) == 24.0
