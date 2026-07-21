"""Local-only publisher (§28 default mode). Writes a publish manifest next to
the video instead of uploading — the safe default before YouTube is wired."""
from __future__ import annotations

import json
from pathlib import Path

from .base import Publisher, PublishRequest


class LocalPublisher(Publisher):
    name = "local"

    def is_configured(self) -> bool:
        return True

    def publish(self, req: PublishRequest) -> dict:
        video = Path(req.video_path)
        manifest = video.with_suffix(".publish.json")
        data = {
            "target": "local_only",
            "video": str(video),
            "title": req.title,
            "description": req.description,
            "privacy_status": req.privacy_status,
            "publish_at": req.publish_at,
            "playlist_id": req.playlist_id,
            "thumbnail": req.thumbnail_path,
            "captions": req.captions_path,
        }
        manifest.write_text(json.dumps(data, ensure_ascii=False, indent=2),
                            encoding="utf-8")
        return {"target": "local_only", "path": str(video),
                "manifest": str(manifest)}
