# YOUTUBE_WORKFLOW (§28, §29)

Publishing is **not** fully automatic by default (§28, §33). Phase 1 exports
locally; YouTube modes arrive in Phase 5.

## Modes (`config/publishing.yaml`)
`local_only` (default) · `private` · `unlisted` · `scheduled`. Only a Quality-Gate
**PASS** video may be scheduled (§28).

## Auth (no monthly fee, §9)
Uploads use the **YouTube Data API v3** with a one-time OAuth client the channel
owner creates in Google Cloud (free tier). GCL stores a refresh token locally and
uploads as the channel — no human "logs in" per upload, and no paid service is
involved. The token lives outside the repo; never commit it.

Daily quota note: uploads cost API quota; the default free quota allows a handful
of uploads/day — fine for the "publish few" strategy (§2).

## Per-video, on publish
Set: title, description, tags, playlist (per series, §12), thumbnail, captions
(SRT JA/EN), visibility/schedule time. Enforce cadence + no-same-day rules from
`config/publishing.yaml` (§12).

## Playlists (§12)
World Experiments · NPC Stories · World History · Original Soundtrack · Relaxing
Fantasy Music · Development Updates.

## Analytics learner (§29)
Import impressions, CTR, 30-s retention, avg view duration/%, new vs returning,
like rate, comments, subs, end-screen & Steam-link clicks; break down by series /
protagonist / length / title-format / thumbnail-layout.

**May tune:** plan selection, protagonist choice, length, intro structure, title
format, thumbnail layout, publish day/time, series mix.

**Must never tune (§29, §33):** in-game event rates, NPC personalities, world
settings, game balance, story. GCL never distorts the game for YouTube.
