# YOUTUBE_WORKFLOW (§28, §29)

Publishing is gated: **only a Quality-Gate PASS video may be scheduled**, FAIL is
never uploaded, and nothing goes public without a future `publishAt` (予約投稿) or
an explicit `public` mode (§28, §33).

## Modes (`config/publishing.yaml`)
`local_only` (default) · `private` · `unlisted` · `scheduled`.

- **scheduled (予約投稿)** — the target for hands-off operation. Uploads the video
  **private** with a future `publishAt`; YouTube flips it public at that time. A
  human can still cancel before then. Requires a PASS.
- **private / unlisted** — uploads immediately at that visibility (WARN allowed,
  FAIL not).
- **local_only** — writes a `*.publish.json` manifest next to the video; no upload.

## One-time OAuth setup (free, no monthly fee, §9)

1. Google Cloud Console → new project → enable **YouTube Data API v3**.
2. Create an **OAuth client ID** (type: Desktop app). Download the JSON.
3. Save it as `config/youtube_client_secret.json` (path configurable).
4. `pip install google-api-python-client google-auth-oauthlib`.
5. First run opens a browser consent once; the refresh token is cached at
   `config/youtube_token.json` and reused unattended thereafter. On a headless
   box, swap `run_local_server` for `run_console` (see `publishing/youtube.py`).

Quota note: uploads cost API quota; the free quota allows a few uploads/day —
plenty for the "publish few" strategy (§2). Keep the token file out of git
(already covered by `.gitignore` patterns for `config/*token*`).

## Commands

```bash
# Produce only (no publish):
python -m gcl.cli render  --experiment ... --telemetry ... --frames ...

# Produce + publish per config (unattended):
python -m gcl.cli auto    --experiment ... --telemetry ... --frames ... --mode scheduled

# Publish an already-produced job:
python -m gcl.cli publish --job workspace/renders/<job_id> --mode scheduled
```

`auto --mode scheduled` computes the next slot from `publishing.schedule`
(`time_utc`, `min_lead_hours`) unless `--publish-at <RFC3339>` is given.

## Per-video fields set on upload
Title, description (with chapters + Steam CTA + VOICEVOX credit), tags, privacy /
publishAt, captions (SRT), and — best-effort — thumbnail and playlist. Failures on
thumbnail/playlist/captions are reported but never fail the whole upload.

## Analytics learner (§29)
Import impressions, CTR, 30-s retention, avg view %/duration, subs, end-screen &
Steam-link clicks; break down by series / protagonist / length / title-format /
thumbnail-layout. **May tune** plan/protagonist/length/intro/title/thumbnail/
publish-time/series-mix. **Must never tune** in-game event rates, NPC
personalities, world settings, balance, or story (§29, §33). Phase 5.
