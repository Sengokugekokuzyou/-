"""Assemble a video from a captured frame sequence (§24).

Input is a directory of numbered PNGs (what the game's capture scene writes) plus
an optional BGM/voice track and an optional burned-in lower-third title. Output
is an H.264 MP4 with an audio stream (silent if none supplied, so downstream
"no audio track" checks are meaningful).

This is deliberately the *strategic-map* path: the demo (体験版) renders the
軍略マップ, and the existing ``strategic_capture.tscn`` already emits stills — so
this is the shortest route to a first finished video, before the 3D third-person
build lands in Early Access.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .ffmpeg import filter_available, run_ffmpeg

# IPA Gothic ships on this sandbox; on Windows the config points at a bundled
# font. drawtext needs a real font file for Japanese glyphs.
_DEFAULT_FONT_CANDIDATES = (
    "/etc/alternatives/fonts-japanese-gothic.ttf",
    "/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf",
)


@dataclass
class AssembleSpec:
    frames_glob: str          # e.g. "frame_%05d.png" (ffmpeg pattern)
    frames_dir: str
    fps: int = 30
    width: int = 1920
    height: int = 1080
    audio_path: str | None = None     # BGM or narration wav/mp3
    title_text: str | None = None     # burned lower-third (optional)
    font_path: str | None = None
    crf: int = 20                     # quality; lower = better
    # When set, stretch the frame sequence to exactly this many seconds by
    # deriving the input frame rate (frame_count / target). Used to match the
    # video length to the narration length so nothing is cut short (§24).
    target_duration: float | None = None


def _resolve_font(spec: AssembleSpec) -> str | None:
    if spec.font_path and Path(spec.font_path).exists():
        return spec.font_path
    for c in _DEFAULT_FONT_CANDIDATES:
        if Path(c).exists():
            return c
    return None


def count_frames(frames_dir: str | Path, frames_glob: str) -> int:
    """Count frame files matching an ffmpeg numeric pattern (frame_%05d.png)."""
    import re

    # Turn "frame_%05d.png" into a shell glob "frame_*.png".
    glob = re.sub(r"%\d*d", "*", frames_glob)
    return len(list(Path(frames_dir).glob(glob)))


def input_framerate(spec: AssembleSpec) -> float:
    """The input frame rate to feed ffmpeg: the configured fps, or — when a
    target duration is set — one that spreads all frames across that duration."""
    if spec.target_duration and spec.target_duration > 0:
        n = count_frames(spec.frames_dir, spec.frames_glob)
        if n > 0:
            return round(n / spec.target_duration, 6)
    return float(spec.fps)


def assemble_from_frames(
    spec: AssembleSpec,
    out_path: str | Path,
    *,
    ffmpeg: str | None = None,
    dry_run: bool = False,
) -> tuple[list[str], str]:
    """Render frames → MP4. Never overwrites silently: caller supplies a unique
    job path (§32 "出力ファイルを上書きしない")."""
    out_path = Path(out_path)
    if out_path.exists() and not dry_run:
        raise FileExistsError(f"refusing to overwrite existing render: {out_path}")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    pattern = str(Path(spec.frames_dir) / spec.frames_glob)
    args: list[str] = ["-framerate", str(input_framerate(spec)), "-i", pattern]

    # Audio: real track, or a generated silent one so the file always has audio.
    if spec.audio_path and Path(spec.audio_path).exists():
        args += ["-i", spec.audio_path]
    else:
        args += ["-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo"]

    # Video filter chain: scale/pad to target, optional burned title.
    vf = (
        f"scale={spec.width}:{spec.height}:force_original_aspect_ratio=decrease,"
        f"pad={spec.width}:{spec.height}:(ow-iw)/2:(oh-ih)/2,"
        f"format=yuv420p"
    )
    font = _resolve_font(spec)
    if spec.title_text and font and filter_available("drawtext", ffmpeg=ffmpeg):
        safe = spec.title_text.replace(":", r"\:").replace("'", r"\'")
        vf += (
            f",drawtext=fontfile='{font}':text='{safe}':"
            f"fontcolor=white:fontsize=48:box=1:boxcolor=black@0.5:boxborderw=16:"
            f"x=(w-text_w)/2:y=h-text_h-80"
        )
    # If drawtext is unavailable (minimal ffmpeg build), the title is skipped in
    # the burn-in but still lives in the job report / packaging. On a full ffmpeg
    # install the burn-in is applied automatically.

    args += [
        "-vf", vf,
        "-c:v", "libx264", "-crf", str(spec.crf), "-preset", "medium",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        "-movflags", "+faststart",
        str(out_path),
    ]
    return run_ffmpeg(args, ffmpeg=ffmpeg, dry_run=dry_run)
