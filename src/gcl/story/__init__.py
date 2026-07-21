"""Story intelligence: turn a flat event stream into ranked video candidates."""

from .detector import StoryCandidate, detect_candidates
from .content_score import ScoreBreakdown, score_candidate

__all__ = [
    "StoryCandidate",
    "detect_candidates",
    "ScoreBreakdown",
    "score_candidate",
]
