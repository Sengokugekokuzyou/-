"""Packaging: scripts, titles, descriptions — all derived from recorded facts."""

from .script_builder import build_script, ScriptLine
from .titles import title_candidates, english_title_candidates
from .description import build_package, Package, build_chapters, thumbnail_texts

__all__ = [
    "build_script", "ScriptLine",
    "title_candidates", "english_title_candidates",
    "build_package", "Package", "build_chapters", "thumbnail_texts",
]
