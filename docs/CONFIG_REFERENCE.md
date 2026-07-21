# CONFIG_REFERENCE

All tunables live in `config/*.yaml` and are merged under a key named after the
file stem (e.g. `app.yaml` → `cfg["app"]`). Relative paths resolve from the
project root; absolute paths are used as-is (§32). Nothing here is hardcoded in
code.

## config/app.yaml
| Key | Default | Meaning |
|---|---|---|
| `channel_name` | Shirokuro Games | Channel label. |
| `game_name` | GEKOKUJO: Vagrant Crown | Used in packaging/CTAs. |
| `steam_url` | Steam store URL | Steam CTA link. |
| `width` / `height` | 1920 / 1080 | Render target; Quality Gate compares to this. |
| `fps` | 30 | Assembly frame rate. |
| `frames_glob` | `frame_%05d.png` | FFmpeg input pattern for captured frames. |
| `narration_style` | calm_documentary | TTS tone (§22). |

## config/paths.yaml
| Key | Default | Meaning |
|---|---|---|
| `workspace` … `renders` | `workspace/...` | Working directories. |
| `ffmpeg` / `ffprobe` | "" (auto) | Blank → PATH, then bundled imageio-ffmpeg. Set to the Windows install path on the production box. |
| `font` | "" (auto) | JP-capable font for burned-in titles. |

## config/quality_gate.yaml
| Key | Default | Meaning |
|---|---|---|
| `min_width` / `min_height` | 1920 / 1080 | Resolution floor. |
| `min_duration_seconds` | 3 | Duration floor (raise to ~480 for long-form). |
| `require_audio` | true | Audio stream required. |
| `max_title_format_repeat` | 1 | Anti-repetition (§2-6). |
| `max_similarity_to_previous` | 0.7 | Max allowed similarity to recent uploads. |

## config/publishing.yaml
| Key | Default | Meaning |
|---|---|---|
| `mode` | local_only | Publish mode; never auto-public by default (§28). |
| `allowed_modes` | list | local_only/private/unlisted/scheduled. |
| `steam_url` | Steam URL | CTA link. |
| `cadence.*` | see file | Recommended per-format frequency (§12). |
| `prevent_same_day_publish` | true | No two publishes same day (§12). |
| `playlists.*` | see file | Series → playlist names. |

## Overriding on the Windows production machine
Typical changes: set `paths.ffmpeg` to the real ffmpeg.exe, `paths.font` to a
bundled JP font, and raise `quality_gate.min_duration_seconds` for real long-form.
Leave everything else at defaults.
