# QUALITY_GATE (§27)

The final authority before any publish. A high Content Score **cannot** bypass it
(§19). Implemented in `gcl/quality/gate.py`; thresholds in
`config/quality_gate.yaml`.

## Verdicts
- **PASS** — eligible for scheduled/private upload (§28).
- **WARN** — export privately + write a report; a human must review.
- **FAIL** — regenerate or discard; never published.

The overall verdict is the most severe check (FAIL > WARN > PASS). Checks that
can't be decided from available data report **WARN**, never a silent PASS.

## Checks implemented in v0.1

Technical (from `ffprobe`/`ffmpeg` on the render):
| Check | FAIL when |
|---|---|
| `technical.resolution` | below `min_width`×`min_height` |
| `technical.duration` | below `min_duration_seconds` |
| `technical.audio_present` | no audio stream |
| `technical.probe` | WARN if media info unavailable (dry-run/probe failed) |

Content:
| Check | Rule |
|---|---|
| `content.no_fabrication` | FAIL if any asserted (non-hedged, non-CTA/Question) script line has no `source_event_ids` (§21). |
| `content.has_result` | FAIL if no `Result` section (§21 "結末が存在する"). |
| `content.title_consistency` | FAIL if a day-count in the title contradicts the record; PASS if title references a real location/day; WARN if unverifiable (§25). |
| `content.title_format_rotation` | WARN if same title format as the previous upload (§2-6). |

## Checks specced, added as inputs become available

Technical: frame drops, black frames, silence, clipping, loudness, subtitle
overflow/overlap, UI/debug overlays, mouse cursor, load screens, corrupt files,
TTS mispronunciation (§27). Most require frame/audio analysis (ffmpeg
`blackdetect`/`silencedetect` + a subtitle timing pass) — wired in Phase 1/3.

Content: thumbnail-person-appears-in-video, numeric accuracy vs. log,
over-similarity to previous uploads, "does not flatter the game unfairly" (§27,
§29).

BGM-specific (§27): no BGM file noise, video length matches track, no unnatural
mid-song cut, loop seam quality, ambience doesn't drown the BGM, rights confirmed,
no obvious short-clip looping. Added in Phase 2 with the BGM pipeline.

## Extending
Add a check by appending a `Check(name, verdict, detail)` in `run_gate`. Keep each
check a pure function of inputs so it stays unit-testable (see
`tests/test_quality_gate.py`).
