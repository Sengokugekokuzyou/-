# BGM_MV_SPEC (§8–§11)

BGM music videos share GCL's Capture / Camera / Editing / Packaging / Quality Gate
with normal videos, but use **separate templates, edit rules, cadence, and quality
bars** (§37). Implementation is Phase 2, gated on the 3D third-person Early Access
build for scenic footage.

## Formats (§9)
- **A. Official Music Video** — one per track; length = song; multi-location;
  cuts follow the song's structure; captions = track + game name only.
- **B. Scenic Journey** — protagonist + wolf traveling (forest, road, village,
  river, bridge, dusk, camp, dawn). Third-person, keeps a real-gameplay feel.
- **C. Ambient / Work Music** — 30/60/90-min compilations of same-mood tracks;
  vary location/weather/time/camera so no blatant short-clip loop (§27).
- **D. Battle Music Video** — combat footage; real gameplay first, no misleading
  over-cinematic editing (§9-D).
- **E. Night / Campfire** — calm night/rain/campfire; optional low-volume ambience
  (fire, wind, rain, river, distant animals, village life) layered under the BGM.

## Metadata (§10)
`content/bgm_tracks/<id>.yaml` — see `northern_forest_theme.yaml`. Fields: id,
titles, file, duration, bpm, **rights** (must be confirmed before publish, §33),
mood, `intensity_curve`, suitable locations/times/weather, preferred subjects,
`video_modes`. BPM/intensity may be auto-analyzed, but **manual values always
win** (§10).

## Director (§11): song structure → shots
| Song section | Footage |
|---|---|
| Intro | wide forest establishing |
| Verse / quiet | protagonist + wolf walking |
| Build | village / bridge / river / travel changes |
| Peak | combat, hill vista, capital in the distance |
| Outro | campfire, dusk, night sky |

Edit sync targets: beat, bar, volume change, instrument entry, song peak, end.
**No excessive fast cutting** — GCL BGM MVs favor calm, immersive editing (§11).

Shot ratio (§20): journey/third-person 50% · scenery/ambient 30% · staged camera
20% (overridable for battle tracks).

## Packaging (§25)
5 JA + 5 EN titles, track-name + game-name captions, description with chapters,
Steam link, OST-playlist link. **No clickbait大煽り文字 on BGM thumbnails** (§26).

## Cadence (§12)
BGM MV: 1–2 / month. Long-form ambient: 0–1 / month. Never let BGM volume bury
normal videos; never schedule two publishes on the same day.

## Quality Gate additions
See `QUALITY_GATE.md` → BGM-specific checks.
