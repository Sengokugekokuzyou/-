"""Video editing via FFmpeg (§24). No paid tools, no cloud (§9)."""

from .ffmpeg import find_ffmpeg, run_ffmpeg, FFmpegNotFound, probe_media
from .assembler import assemble_from_frames, AssembleSpec

__all__ = [
    "find_ffmpeg",
    "run_ffmpeg",
    "FFmpegNotFound",
    "probe_media",
    "assemble_from_frames",
    "AssembleSpec",
]
