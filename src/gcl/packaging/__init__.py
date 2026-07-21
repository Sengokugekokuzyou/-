"""Packaging: scripts, titles, descriptions — all derived from recorded facts."""

from .script_builder import build_script, ScriptLine
from .titles import title_candidates

__all__ = ["build_script", "ScriptLine", "title_candidates"]
