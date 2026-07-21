"""Select a publisher + resolve the publish request from config (§28)."""
from __future__ import annotations

from .base import Publisher
from .local import LocalPublisher
from .youtube import YouTubePublisher

# Modes that go to YouTube vs. stay local.
_YOUTUBE_MODES = {"private", "unlisted", "scheduled"}


def get_publisher(cfg: dict) -> Publisher:
    pub = (cfg or {}).get("publishing", {}) if isinstance(cfg, dict) else {}
    mode = str(pub.get("mode", "local_only")).lower()
    if mode not in _YOUTUBE_MODES:
        return LocalPublisher()
    yt = pub.get("youtube", {})
    return YouTubePublisher(
        client_secret_path=yt.get("client_secret_path",
                                  "config/youtube_client_secret.json"),
        token_path=yt.get("token_path", "config/youtube_token.json"),
    )


def privacy_for_mode(mode: str) -> str:
    mode = (mode or "local_only").lower()
    if mode == "unlisted":
        return "unlisted"
    # private and scheduled both upload as private (scheduled adds publishAt).
    return "private"
