from gcl.publishing import build_video_body, PublishRequest, privacy_for_mode
from gcl.publishing.local import LocalPublisher
from gcl.publishing.factory import get_publisher


def test_scheduled_forces_private_with_publish_at():
    req = PublishRequest(video_path="v.mp4", title="t", privacy_status="public",
                         publish_at="2030-01-01T10:00:00Z")
    body = build_video_body(req)
    # A scheduled upload MUST be private + publishAt, regardless of requested privacy.
    assert body["status"]["privacyStatus"] == "private"
    assert body["status"]["publishAt"] == "2030-01-01T10:00:00Z"


def test_title_and_description_truncated():
    req = PublishRequest(video_path="v.mp4", title="x" * 200,
                         description="y" * 6000)
    body = build_video_body(req)
    assert len(body["snippet"]["title"]) == 100
    assert len(body["snippet"]["description"]) == 5000


def test_privacy_for_mode():
    assert privacy_for_mode("unlisted") == "unlisted"
    assert privacy_for_mode("scheduled") == "private"
    assert privacy_for_mode("private") == "private"


def test_factory_local_for_local_only():
    assert get_publisher({"publishing": {"mode": "local_only"}}).name == "local"
    assert get_publisher({"publishing": {"mode": "scheduled"}}).name == "youtube"


def test_local_publisher_writes_manifest(tmp_path):
    video = tmp_path / "video.mp4"
    video.write_bytes(b"\x00")
    req = PublishRequest(video_path=str(video), title="タイトル",
                         description="説明", privacy_status="private")
    res = LocalPublisher().publish(req)
    assert res["target"] == "local_only"
    manifest = tmp_path / "video.publish.json"
    assert manifest.exists()
    import json
    assert json.loads(manifest.read_text(encoding="utf-8"))["title"] == "タイトル"
