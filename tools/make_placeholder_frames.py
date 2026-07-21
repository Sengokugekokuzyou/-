"""Generate placeholder capture frames for testing the render spine.

This stands in for the game's ``strategic_capture.tscn`` output until the real
capture path writes frames. It draws simple strategic-map-style frames (day
counter + caption) so the FFmpeg assembler has a real numbered PNG sequence to
work on. Dev tool only — not part of the GCL runtime dependency surface.

    python tools/make_placeholder_frames.py --out workspace/raw_capture/demo_frames \
        --seconds 4 --fps 30 --caption "北方森林 / Glen Village"
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

_FONT_CANDIDATES = (
    "/etc/alternatives/fonts-japanese-gothic.ttf",
    "/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf",
)


def _font(size: int):
    for c in _FONT_CANDIDATES:
        if Path(c).exists():
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--seconds", type=float, default=4.0)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--width", type=int, default=1920)
    ap.add_argument("--height", type=int, default=1080)
    ap.add_argument("--caption", default="GEKOKUJO strategic map")
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    total = max(1, int(args.seconds * args.fps))
    big, small = _font(96), _font(44)

    for i in range(total):
        # Slow day-count sweep to imitate a 7-day strategic sim playing out.
        day = 1 + int((i / total) * 7)
        t = i / total
        bg = (18 + int(24 * t), 26 + int(18 * t), 40 + int(30 * t))
        img = Image.new("RGB", (args.width, args.height), bg)
        d = ImageDraw.Draw(img)
        d.text((120, 120), f"Day {day}", font=big, fill=(240, 235, 220))
        d.text((120, 240), args.caption, font=small, fill=(200, 205, 215))
        d.text((120, args.height - 140),
               "GEKOKUJO Content Lab — placeholder capture",
               font=small, fill=(120, 130, 145))
        img.save(out / f"frame_{i:05d}.png")

    print(f"wrote {total} frames → {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
