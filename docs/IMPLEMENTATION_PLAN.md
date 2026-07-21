# IMPLEMENTATION_PLAN

Small, working increments; each phase leaves a runnable artifact (§34). Order is
adjusted to the game's actual roadmap: **strategic-map content first, 3D
third-person / BGM MV once Early Access lands** (see `ARCHITECTURE.md`).

## Phase 0 — Survey ✅ (done)
- Read the game repo; mapped existing systems to GCL modules → `ARCHITECTURE.md`.
- Finding: pseudo-player, EventBus, NpcLifeNarrator, event catalogue, capture, and
  soak harness already exist. GCL is mostly a connection + post-production layer.

## Phase 1 — Minimum video ✅ (spine working) / 🔜 (TTS, subtitles)
Done:
- Telemetry schema + reader (`gcl.telemetry`)
- Candidate detection + Content Score (`gcl.story`)
- Fact-anchored script + title candidates (`gcl.packaging`)
- FFmpeg frame assembler + discovery (`gcl.editing`)
- Quality Gate (`gcl.quality`)
- Godot `TelemetryExporter.gd` drop-in
- CLI `doctor` / `score` / `render`; unit tests; a real MP4 renders end-to-end.

Remaining for a fully finished normal video:
- [x] VOICEVOX TTS adapter (`TTSProvider` → `VoicevoxProvider`, + `MockProvider`)
      — calm voice, 冥鳴ひまり (§22). Pluggable; narration muxed into the render.
- [x] Subtitle generation (SRT) from narration timing, JA (§23). ASS / burn-in /
      EN next.
- [x] Drive video length from narration length (input framerate stretch, §24).
- [x] Real strategic-map frame capture scene (game repo: `strategic_video_capture`)
      — pending in-engine run on the game machine.
- [x] Packaging: titles JA/EN, description, chapters, thumbnail text, pinned
      comment, Steam news, X post (§25).

## Phase 5 (started early per full-automation request) — Publish
- [x] Publisher: local manifest + YouTube private/unlisted/scheduled (§28).
- [x] Orchestrator: `gcl auto` = produce → gate → publish; `gcl publish` for a
      finished job. Scheduled (予約投稿) computes the next slot; PASS-gated.
- [ ] OAuth first-run on the game machine (docs/YOUTUBE_WORKFLOW.md).
- [ ] Analytics import + learner (§29) — tunes packaging only, never the game.

## Phase 2 — BGM MV (EA-gated for 3D footage)
- BGM metadata loader (`content/bgm_tracks/*.yaml` — sample present).
- Optional BPM/intensity auto-analysis, always overridable (§10).
- BGM MV Director: map song structure → shot list (§11).
- Official MV + Ambient outputs; BGM-specific Quality Gate checks (§27).
- First deliverable: one Official MV for `northern_forest_theme`.

## Phase 3 — Replay & re-shoot
- Periodic save → pre-event autosave → scenario re-run (`REPLAY_DESIGN.md`).
- Multi-angle capture; vertical (Shorts) re-shoot (§24).

## Phase 4 — Story intelligence
- Causal chain analysis across seeds; NPC life tracking; multi-seed comparison;
  long-form World History assembly (§7).

## Phase 5 — Publish & learn
- YouTube private → scheduled upload (never auto-public by default, §28).
- Analytics import + report; feed back into planning (§29), **without** touching
  game balance.

## Non-negotiables carried through every phase
Resumable, per-stage re-runnable, dry-run, config-driven, UTF-8, unique job_id,
no overwrite, no paid/monthly services, no fabrication, no auto-publish of
low-quality video (§32, §33).
