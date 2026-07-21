"""Publisher interface + request model (§28).

The body builder is a pure function so it can be unit-tested without the Google
client libraries or a network.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


class PublishError(Exception):
    pass


@dataclass
class PublishRequest:
    video_path: str
    title: str
    description: str = ""
    tags: list[str] = field(default_factory=list)
    category_id: str = "20"          # "Gaming"
    privacy_status: str = "private"  # private | unlisted | public
    publish_at: str | None = None    # RFC3339; scheduled ("予約") upload
    thumbnail_path: str | None = None
    captions_path: str | None = None
    caption_language: str = "ja"
    playlist_id: str | None = None
    made_for_kids: bool = False


def build_video_body(req: PublishRequest) -> dict:
    """The `videos.insert` request body (snippet + status).

    Scheduling rule (§28 予約投稿): a scheduled upload MUST be uploaded as
    ``private`` with a future ``publishAt``; YouTube flips it public at that time.
    """
    status: dict = {
        "privacyStatus": req.privacy_status,
        "selfDeclaredMadeForKids": req.made_for_kids,
    }
    if req.publish_at:
        # Scheduled → force private + publishAt, per the API contract.
        status["privacyStatus"] = "private"
        status["publishAt"] = req.publish_at
    return {
        "snippet": {
            "title": req.title[:100],           # YouTube hard limit
            "description": req.description[:5000],
            "tags": req.tags,
            "categoryId": req.category_id,
        },
        "status": status,
    }


class Publisher(ABC):
    name: str = "base"

    @abstractmethod
    def is_configured(self) -> bool:
        ...

    @abstractmethod
    def publish(self, req: PublishRequest) -> dict:
        """Return {'target','video_id'?,'url'?,'path'?}. Raise PublishError on
        failure — a failed publish is never reported as success."""
