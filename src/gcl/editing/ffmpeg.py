"""Locate and invoke FFmpeg without hardcoding an absolute path (§32).

Resolution order:
  1. explicit path from config (``paths.yaml: ffmpeg``)
  2. ``ffmpeg`` on PATH (a normal Windows/Linux install)
  3. the binary bundled by the ``imageio-ffmpeg`` pip package (no system install,
     works offline and cross-platform — how this sandbox runs it)
"""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


class FFmpegNotFound(Exception):
    pass


def find_ffmpeg(configured: str | None = None) -> str:
    if configured:
        p = Path(configured)
        if p.exists():
            return str(p)
    on_path = shutil.which("ffmpeg")
    if on_path:
        return on_path
    try:
        import imageio_ffmpeg  # type: ignore

        exe = imageio_ffmpeg.get_ffmpeg_exe()
        if exe and Path(exe).exists():
            return exe
    except Exception:  # noqa: BLE001 - optional dependency
        pass
    raise FFmpegNotFound(
        "ffmpeg not found. Install it, put it on PATH, set paths.yaml:ffmpeg, "
        "or `pip install imageio-ffmpeg`."
    )


def find_ffprobe(configured: str | None = None) -> str | None:
    if configured:
        p = Path(configured)
        if p.exists():
            return str(p)
    return shutil.which("ffprobe")


_FILTER_CACHE: dict[str, bool] = {}


def filter_available(name: str, *, ffmpeg: str | None = None) -> bool:
    """Return True if this ffmpeg build has the named filter.

    Minimal/static builds (e.g. the imageio-ffmpeg binary) omit ``drawtext``
    because they lack libfreetype; a full Windows/Linux install has it. We detect
    rather than assume, so burned-in titles degrade gracefully instead of
    aborting the render."""
    if name in _FILTER_CACHE:
        return _FILTER_CACHE[name]
    exe = ffmpeg or find_ffmpeg()
    proc = subprocess.run([exe, "-hide_banner", "-filters"],
                          capture_output=True, text=True)
    available = any(
        f" {name} " in line for line in proc.stdout.splitlines()
    )
    _FILTER_CACHE[name] = available
    return available


def run_ffmpeg(
    args: list[str],
    *,
    ffmpeg: str | None = None,
    dry_run: bool = False,
) -> tuple[list[str], str]:
    """Build and (unless dry_run) execute an ffmpeg command.

    Returns (argv, stderr_tail). Raises on non-zero exit so a failed render is
    never mistaken for a success (§ "報告は忠実に").
    """
    exe = ffmpeg or find_ffmpeg()
    argv = [exe, "-hide_banner", "-y", *args]
    if dry_run:
        return argv, ""
    proc = subprocess.run(argv, capture_output=True, text=True)
    if proc.returncode != 0:
        tail = "\n".join(proc.stderr.strip().splitlines()[-15:])
        raise RuntimeError(f"ffmpeg failed (exit {proc.returncode}):\n{tail}")
    return argv, "\n".join(proc.stderr.strip().splitlines()[-5:])


def probe_media(path: str | Path, *, ffprobe: str | None = None) -> dict:
    """Return {width,height,duration,fps,has_audio} for a rendered file.

    Falls back to ffmpeg -i parsing when ffprobe is absent (imageio-ffmpeg ships
    ffmpeg only). Best-effort; the Quality Gate treats missing fields as unknown.
    """
    exe = find_ffprobe(ffprobe)
    if exe:
        argv = [
            exe, "-v", "quiet", "-print_format", "json",
            "-show_format", "-show_streams", str(path),
        ]
        proc = subprocess.run(argv, capture_output=True, text=True)
        if proc.returncode == 0:
            return _parse_ffprobe(json.loads(proc.stdout))
    return _probe_via_ffmpeg(path)


def _parse_ffprobe(data: dict) -> dict:
    out = {"width": None, "height": None, "duration": None, "fps": None,
           "has_audio": False}
    for s in data.get("streams", []):
        if s.get("codec_type") == "video":
            out["width"] = s.get("width")
            out["height"] = s.get("height")
            fr = s.get("avg_frame_rate", "0/1")
            try:
                num, den = fr.split("/")
                out["fps"] = round(int(num) / int(den), 3) if int(den) else None
            except Exception:  # noqa: BLE001
                pass
        elif s.get("codec_type") == "audio":
            out["has_audio"] = True
    dur = data.get("format", {}).get("duration")
    if dur:
        out["duration"] = float(dur)
    return out


def _probe_via_ffmpeg(path: str | Path) -> dict:
    exe = find_ffmpeg()
    proc = subprocess.run([exe, "-i", str(path)], capture_output=True, text=True)
    text = proc.stderr
    out = {"width": None, "height": None, "duration": None, "fps": None,
           "has_audio": "Audio:" in text}
    import re

    m = re.search(r"(\d{2,5})x(\d{2,5})", text)
    if m:
        out["width"], out["height"] = int(m.group(1)), int(m.group(2))
    m = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", text)
    if m:
        h, mi, s = int(m.group(1)), int(m.group(2)), float(m.group(3))
        out["duration"] = h * 3600 + mi * 60 + s
    m = re.search(r"(\d+(?:\.\d+)?) fps", text)
    if m:
        out["fps"] = float(m.group(1))
    return out
