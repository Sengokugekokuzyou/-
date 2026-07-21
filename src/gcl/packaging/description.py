"""Packaging assets (§25): description, chapters, thumbnail text, pinned
comment, Steam news, X post — all from recorded facts + config, no fabrication.

Chapters are derived from the narration timing segments produced by the TTS
stage, so timestamps are exact.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from ..story.detector import StoryCandidate
from .titles import title_candidates, english_title_candidates

# Script-section → JP chapter label (§21 sections).
_SECTION_JP = {
    "Hook": "異変", "Question": "問い", "Setup": "舞台", "Escalation": "経過",
    "Focus Character": "注目人物", "Turning Point": "転機", "Result": "結果",
    "Interpretation": "考察", "Steam CTA": "GEKOKUJOについて",
}


def _fmt_ts(seconds: float) -> str:
    s = int(seconds)
    h, s = divmod(s, 3600)
    m, s = divmod(s, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def build_chapters(narration_segments: list[dict]) -> list[dict]:
    """Group consecutive segments by section → YouTube chapters.

    Returns [{"time": "0:00", "label": "..."}]. The first chapter is forced to
    0:00 (a YouTube requirement). Callers should note YouTube also wants >=3
    chapters each >=10s; short demos may not qualify — that's surfaced, not faked.
    """
    chapters: list[dict] = []
    last_section = None
    for seg in narration_segments:
        section = seg.get("section", "")
        if section and section != last_section:
            label = _SECTION_JP.get(section, section)
            chapters.append({"time": _fmt_ts(seg.get("start", 0.0)), "label": label})
            last_section = section
    if chapters:
        chapters[0]["time"] = "0:00"
    return chapters


def thumbnail_texts(candidate: StoryCandidate, *, max_n: int = 5) -> list[str]:
    """Short, on-screen thumbnail phrases (§26). Minimal words, fact-true."""
    f_loc = next((e.location_id for e in candidate.events if e.location_id), "村")
    days = candidate.day_span or (candidate.events[-1].game_day
                                  if candidate.events else 0)
    peak = max(candidate.events, key=lambda e: e.visual_priority) \
        if candidate.events else None
    out = [f"{f_loc}", f"{days}日間"]
    if peak:
        from .script_builder import _TYPE_JP
        out.append(_TYPE_JP.get(peak.type, peak.type))
    out.append("記録")
    out.append("その結末")
    # De-dup, keep order, cap.
    seen, res = set(), []
    for t in out:
        if t and t not in seen:
            seen.add(t); res.append(t)
        if len(res) >= max_n:
            break
    return res


@dataclass
class Package:
    title: dict
    titles_ja: list[dict]
    titles_en: list[dict]
    thumbnail_texts: list[str]
    description: str
    chapters: list[dict]
    pinned_comment: str
    steam_news: str
    x_post: str
    warnings: list[str] = field(default_factory=list)

    def as_dict(self) -> dict:
        return {
            "title": self.title,
            "titles_ja": self.titles_ja,
            "titles_en": self.titles_en,
            "thumbnail_texts": self.thumbnail_texts,
            "description": self.description,
            "chapters": self.chapters,
            "pinned_comment": self.pinned_comment,
            "steam_news": self.steam_news,
            "x_post": self.x_post,
            "warnings": self.warnings,
        }


def build_package(
    candidate: StoryCandidate,
    *,
    chosen_title: dict,
    question_ja: str,
    question_en: str = "",
    narration_segments: list[dict] | None = None,
    game_name: str = "GEKOKUJO: Vagrant Crown",
    steam_url: str = "",
    tts_credit: str = "",
    playlist: str = "",
) -> Package:
    narration_segments = narration_segments or []
    chapters = build_chapters(narration_segments)
    warnings: list[str] = []
    if narration_segments and len(chapters) < 3:
        warnings.append("fewer than 3 chapters — YouTube may not show a chapter list")

    titles_ja = title_candidates(candidate, question_ja=question_ja)
    titles_en = english_title_candidates(candidate, question_en=question_en)

    loc = next((e.location_id for e in candidate.events if e.location_id), "村")
    days = candidate.day_span or (candidate.events[-1].game_day
                                  if candidate.events else 0)

    # Description: fact-true summary, then chapters, Steam CTA, credits (§25).
    desc_lines = [
        f"{game_name} の世界で記録された出来事を、ログに基づいて追ったドキュメンタリーです。",
        "",
        f"舞台：{loc}／記録期間：{days}日間",
        f"問い：{question_ja}",
        "",
        "※このシリーズはゲーム内のイベントログのみを根拠にしています。"
        "ログに無い会話・感情・因果は加えていません。",
    ]
    if chapters:
        desc_lines += ["", "▼チャプター"]
        desc_lines += [f"{c['time']} {c['label']}" for c in chapters]
    if steam_url:
        desc_lines += ["", f"▼GEKOKUJO: Vagrant Crown（Steam）", steam_url]
    if tts_credit:
        desc_lines += ["", f"音声：{tts_credit}"]
    if playlist:
        desc_lines += ["", f"シリーズ：{playlist}"]
    description = "\n".join(desc_lines)

    pinned = (
        f"この動画は {game_name} のゲーム内ログだけを根拠に構成しています。"
        f"事実と異なる点があればコメントで教えてください。"
        + (f"\nSteam: {steam_url}" if steam_url else "")
    )
    steam_news = (
        f"【World Experiment】{chosen_title.get('text', '')}\n\n"
        f"{loc} の{days}日間の記録を動画にまとめました。"
        f"生きた世界で何が起きたのか、ログを追っています。"
    )
    x_post = (
        f"{chosen_title.get('text', '')}\n"
        f"#{game_name.split(':')[0].strip()} #GEKOKUJO"
        + (f"\n{steam_url}" if steam_url else "")
    )

    return Package(
        title=chosen_title, titles_ja=titles_ja, titles_en=titles_en,
        thumbnail_texts=thumbnail_texts(candidate), description=description,
        chapters=chapters, pinned_comment=pinned, steam_news=steam_news,
        x_post=x_post, warnings=warnings,
    )
