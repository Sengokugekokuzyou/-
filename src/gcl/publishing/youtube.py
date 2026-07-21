"""YouTube publisher (§28) — YouTube Data API v3, free tier, no monthly fee (§9).

Auth is a one-time OAuth (installed-app flow) the channel owner runs once; a
refresh token is cached locally and reused unattended thereafter — so scheduled
uploads run with no human in the loop, yet nothing goes public without a Quality
Gate PASS and (for 予約) a future publishAt.

The Google client libraries are an OPTIONAL dependency: without them this
publisher reports "not configured" and the pipeline falls back to local export,
so the core install stays dependency-light.
"""
from __future__ import annotations

from pathlib import Path

from .base import Publisher, PublishRequest, PublishError, build_video_body

_SCOPES = ["https://www.googleapis.com/auth/youtube"]


class YouTubePublisher(Publisher):
    name = "youtube"

    def __init__(
        self,
        *,
        client_secret_path: str,
        token_path: str,
    ) -> None:
        self.client_secret_path = client_secret_path
        self.token_path = token_path

    # ── availability ─────────────────────────────────────────────────────────
    @staticmethod
    def _libs_available() -> bool:
        try:
            import google.oauth2.credentials  # noqa: F401
            import google_auth_oauthlib.flow  # noqa: F401
            import googleapiclient.discovery   # noqa: F401
            return True
        except Exception:  # noqa: BLE001
            return False

    def is_configured(self) -> bool:
        return self._libs_available() and Path(self.client_secret_path).exists()

    # ── auth ─────────────────────────────────────────────────────────────────
    def _credentials(self):
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
        from google_auth_oauthlib.flow import InstalledAppFlow

        creds = None
        tp = Path(self.token_path)
        if tp.exists():
            creds = Credentials.from_authorized_user_file(str(tp), _SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not Path(self.client_secret_path).exists():
                    raise PublishError(
                        f"missing OAuth client secret: {self.client_secret_path}"
                    )
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.client_secret_path, _SCOPES)
                # Runs a one-time local consent; headless machines can use
                # run_console() instead — documented in YOUTUBE_WORKFLOW.md.
                creds = flow.run_local_server(port=0)
            tp.parent.mkdir(parents=True, exist_ok=True)
            tp.write_text(creds.to_json(), encoding="utf-8")
        return creds

    def _service(self):
        from googleapiclient.discovery import build
        return build("youtube", "v3", credentials=self._credentials(),
                     cache_discovery=False)

    # ── publish ──────────────────────────────────────────────────────────────
    def publish(self, req: PublishRequest) -> dict:
        if not self._libs_available():
            raise PublishError(
                "google-api-python-client not installed. "
                "`pip install google-api-python-client google-auth-oauthlib`"
            )
        if not Path(req.video_path).exists():
            raise PublishError(f"video not found: {req.video_path}")
        from googleapiclient.http import MediaFileUpload

        yt = self._service()
        body = build_video_body(req)
        media = MediaFileUpload(req.video_path, chunksize=-1, resumable=True)
        try:
            request = yt.videos().insert(
                part="snippet,status", body=body, media_body=media)
            response = _resumable_upload(request)
        except Exception as e:  # noqa: BLE001
            raise PublishError(f"YouTube upload failed: {e}") from e

        video_id = response.get("id")
        result = {
            "target": "youtube",
            "video_id": video_id,
            "url": f"https://youtu.be/{video_id}" if video_id else None,
            "privacy_status": body["status"]["privacyStatus"],
            "publish_at": body["status"].get("publishAt"),
        }
        # Best-effort extras — never fail the whole publish on these.
        if video_id and req.thumbnail_path and Path(req.thumbnail_path).exists():
            try:
                yt.thumbnails().set(
                    videoId=video_id,
                    media_body=MediaFileUpload(req.thumbnail_path)).execute()
            except Exception as e:  # noqa: BLE001
                result.setdefault("warnings", []).append(f"thumbnail: {e}")
        if video_id and req.playlist_id:
            try:
                yt.playlistItems().insert(part="snippet", body={"snippet": {
                    "playlistId": req.playlist_id,
                    "resourceId": {"kind": "youtube#video", "videoId": video_id},
                }}).execute()
            except Exception as e:  # noqa: BLE001
                result.setdefault("warnings", []).append(f"playlist: {e}")
        if video_id and req.captions_path and Path(req.captions_path).exists():
            try:
                yt.captions().insert(
                    part="snippet",
                    body={"snippet": {"videoId": video_id,
                                      "language": req.caption_language,
                                      "name": req.caption_language, "isDraft": False}},
                    media_body=MediaFileUpload(req.captions_path)).execute()
            except Exception as e:  # noqa: BLE001
                result.setdefault("warnings", []).append(f"captions: {e}")
        return result


def _resumable_upload(request):
    """Drive a resumable upload to completion (§32 resumable)."""
    response = None
    while response is None:
        _status, response = request.next_chunk()
    return response
