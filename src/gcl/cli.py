"""GCL command-line entrypoint.

    python -m gcl.cli doctor
    python -m gcl.cli score   --telemetry workspace/telemetry/sample_north_forest.jsonl
    python -m gcl.cli render  --experiment content/experiments/food_shortage_glen.yaml \
                              --telemetry  workspace/telemetry/sample_north_forest.jsonl \
                              --frames     workspace/raw_capture/demo_frames \
                              [--dry-run]

``render`` runs the full Phase-1 spine end to end:
    telemetry → detect → score → pick → script + titles → assemble → probe →
    Quality Gate → job report.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import sys
from collections import Counter
from pathlib import Path

import yaml

from . import config as cfgmod
from .editing import AssembleSpec, assemble_from_frames, find_ffmpeg, probe_media
from .editing.ffmpeg import FFmpegNotFound
from .jobs import make_job_id, open_job
from .packaging import build_script, title_candidates
from .quality import run_gate
from .story import detect_candidates, score_candidate
from .subtitles import write_srt
from .telemetry import read_events
from .tts import get_provider, synthesize_script
from .tts.base import TTSError


def _stamp() -> str:
    return _dt.datetime.now().strftime("%Y%m%d-%H%M%S")


def cmd_doctor(args) -> int:
    print("GCL doctor")
    try:
        ff = find_ffmpeg()
        print(f"  [ok] ffmpeg: {ff}")
    except FFmpegNotFound as e:
        print(f"  [!!] ffmpeg: {e}")
    for font in (
        "/etc/alternatives/fonts-japanese-gothic.ttf",
        "/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf",
    ):
        if Path(font).exists():
            print(f"  [ok] jp font: {font}")
            break
    else:
        print("  [--] jp font: none found (burned-in JP titles will be skipped)")
    cfg = cfgmod.load_config()
    print(f"  [ok] config keys: {', '.join(cfg) or '(none)'}")
    # TTS reachability (§22).
    try:
        prov = get_provider(cfg)
        ok = prov.is_available()
        host = cfgmod.get(cfg, "tts.host", "")
        mark = "ok" if ok else "--"
        print(f"  [{mark}] tts: {prov.name} "
              f"{'reachable' if ok else 'NOT reachable'} {host}".rstrip())
        if not ok and prov.name == "voicevox":
            print("         (start the VOICEVOX app/engine, or set "
                  "tts.provider: mock for offline)")
    except Exception as e:  # noqa: BLE001
        print(f"  [!!] tts: {e}")
    return 0


def _load_events(path: str):
    res = read_events(path)
    if res.skipped:
        print(f"  [warn] skipped {len(res.skipped)} malformed line(s):",
              file=sys.stderr)
        for ln, why in res.skipped[:5]:
            print(f"         line {ln}: {why}", file=sys.stderr)
    return res.events


def _rank(events):
    candidates = detect_candidates(events)
    hist = Counter(e.type for e in events)
    scored = [(c, score_candidate(c, type_histogram=hist)) for c in candidates]
    scored.sort(key=lambda cs: cs[1].total, reverse=True)
    return scored


def cmd_score(args) -> int:
    events = _load_events(args.telemetry)
    if not events:
        print("no events found", file=sys.stderr)
        return 2
    scored = _rank(events)
    print(f"{'TOTAL':>6}  {'TIER':<11}  CANDIDATE")
    print("-" * 60)
    for c, sb in scored:
        print(f"{sb.total:>6.1f}  {sb.tier:<11}  {c.summary()}")
    if args.report:
        Path(args.report).parent.mkdir(parents=True, exist_ok=True)
        with open(args.report, "w", encoding="utf-8") as fh:
            json.dump(
                [{"candidate": c.summary(), **sb.as_dict()} for c, sb in scored],
                fh, ensure_ascii=False, indent=2,
            )
        print(f"\nreport → {args.report}")
    return 0


def cmd_render(args) -> int:
    cfg = cfgmod.load_config()
    exp = {}
    if args.experiment:
        with open(args.experiment, "r", encoding="utf-8") as fh:
            exp = (yaml.safe_load(fh) or {}).get("experiment", {})
    question = exp.get("question_ja") or "この記録は何を示すのか？"
    steam = cfgmod.get(cfg, "publishing.steam_url", "") or cfgmod.get(
        cfg, "app.steam_url", ""
    )

    events = _load_events(args.telemetry)
    if not events:
        print("no events found", file=sys.stderr)
        return 2
    scored = _rank(events)
    candidate, breakdown = scored[0]
    print(f"selected: {candidate.summary()}  →  {breakdown.total} ({breakdown.tier})")

    titles = title_candidates(candidate, question_ja=question)
    chosen = titles[0]
    script = build_script(candidate, question_ja=question, steam_url=steam)

    workspace = cfgmod.resolve_path(cfgmod.get(cfg, "paths.workspace", "workspace"))
    job_id = make_job_id("exp", args.telemetry + chosen["text"], _stamp())
    job = open_job(workspace, job_id)
    print(f"job: {job_id}")

    # ── Narration (§22) + subtitles (§23) ────────────────────────────────────
    narration_path = None
    narration_segments: list[dict] = []
    if args.narrate != "off":
        try:
            if args.tts_provider:
                cfg.setdefault("tts", {})["provider"] = args.tts_provider
            provider = get_provider(cfg)
            if args.narrate == "on" or provider.is_available():
                nres = synthesize_script(
                    provider, script, job.path("narration.wav"),
                    speaker=int(cfgmod.get(cfg, "tts.speaker", 3)),
                    speed=float(cfgmod.get(cfg, "tts.speed", 0.95)),
                    intonation=float(cfgmod.get(cfg, "tts.intonation", 0.9)),
                    gap_seconds=float(cfgmod.get(cfg, "tts.gap_seconds", 0.15)),
                )
                narration_path = str(nres.wav_path)
                narration_segments = [s.as_dict() for s in nres.segments]
                write_srt(nres.segments, job.path("subtitles.ja.srt"))
                print(f"narration → {narration_path} "
                      f"({nres.total_duration:.1f}s, {provider.name})")
            else:
                print(f"  [--] narration skipped: {provider.name} not reachable "
                      "(use --narrate on with tts.provider: mock to force)")
        except TTSError as e:
            print(f"  [!!] narration failed: {e}", file=sys.stderr)

    out_mp4 = job.path("video.mp4")
    media_info = None
    fps = int(cfgmod.get(cfg, "app.fps", 30))
    spec = AssembleSpec(
        frames_glob=cfgmod.get(cfg, "app.frames_glob", "frame_%05d.png"),
        frames_dir=args.frames,
        fps=fps,
        width=int(cfgmod.get(cfg, "app.width", 1920)),
        height=int(cfgmod.get(cfg, "app.height", 1080)),
        title_text=chosen["text"],
        audio_path=narration_path,
    )
    try:
        argv, _ = assemble_from_frames(spec, out_mp4, dry_run=args.dry_run)
        if args.dry_run:
            print("dry-run ffmpeg:\n  " + " ".join(argv))
        else:
            media_info = probe_media(out_mp4)
            print(f"render → {out_mp4}  {media_info}")
    except (FileNotFoundError, RuntimeError, FileExistsError, FFmpegNotFound) as e:
        print(f"  [!!] render failed: {e}", file=sys.stderr)

    gate = run_gate(
        media_info=media_info,
        script_lines=script,
        title=chosen["text"],
        candidate=candidate,
        config=cfg,
        this_title_format=chosen["format"],
        previous_title_format=args.previous_format,
    )

    report = {
        "job_id": job_id,
        "selected_candidate": candidate.summary(),
        "content_score": breakdown.as_dict(),
        "title": chosen,
        "title_candidates": titles,
        "script": [ln.as_dict() for ln in script],
        "narration": {"wav": narration_path, "segments": narration_segments},
        "media_info": media_info,
        "quality_gate": gate.as_dict(),
        "dry_run": args.dry_run,
    }
    job.write_report("report.json", report)
    print(f"\nQuality Gate: {gate.verdict}")
    for c in gate.checks:
        mark = {"PASS": "  ok", "WARN": "warn", "FAIL": "FAIL"}[c.verdict]
        print(f"  [{mark}] {c.name} {('- ' + c.detail) if c.detail else ''}")
    print(f"\nreport → {job.root / 'report.json'}")
    return 0 if gate.verdict != "FAIL" else 1


def cmd_tts(args) -> int:
    """Synthesize a script's narration standalone — the quickest way to test a
    live VOICEVOX engine end to end."""
    cfg = cfgmod.load_config()
    if args.provider:
        cfg.setdefault("tts", {})["provider"] = args.provider
    exp = {}
    if args.experiment:
        with open(args.experiment, "r", encoding="utf-8") as fh:
            exp = (yaml.safe_load(fh) or {}).get("experiment", {})
    question = exp.get("question_ja") or "この記録は何を示すのか？"

    events = _load_events(args.telemetry)
    if not events:
        print("no events found", file=sys.stderr)
        return 2
    candidate, _ = _rank(events)[0]
    script = build_script(candidate, question_ja=question)

    provider = get_provider(cfg)
    if not provider.is_available():
        print(f"  [!!] {provider.name} not reachable "
              f"({cfgmod.get(cfg, 'tts.host', '')}). Start VOICEVOX, or use "
              f"--provider mock.", file=sys.stderr)
        return 3
    out = Path(args.out or "workspace/audio/narration.wav")
    try:
        nres = synthesize_script(
            provider, script, out,
            speaker=int(args.speaker if args.speaker is not None
                        else cfgmod.get(cfg, "tts.speaker", 3)),
            speed=float(cfgmod.get(cfg, "tts.speed", 0.95)),
            intonation=float(cfgmod.get(cfg, "tts.intonation", 0.9)),
            gap_seconds=float(cfgmod.get(cfg, "tts.gap_seconds", 0.15)),
        )
    except TTSError as e:
        print(f"  [!!] {e}", file=sys.stderr)
        return 3
    srt = write_srt(nres.segments, out.with_suffix(".srt"))
    print(f"narration → {nres.wav_path} ({nres.total_duration:.1f}s, "
          f"{len(nres.segments)} lines, {provider.name})")
    print(f"subtitles → {srt}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="gcl", description="GEKOKUJO Content Lab")
    sub = p.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("doctor", help="check environment")
    d.set_defaults(func=cmd_doctor)

    s = sub.add_parser("score", help="rank story candidates from telemetry")
    s.add_argument("--telemetry", required=True)
    s.add_argument("--report", default="")
    s.set_defaults(func=cmd_score)

    r = sub.add_parser("render", help="run the Phase-1 video spine")
    r.add_argument("--telemetry", required=True)
    r.add_argument("--experiment", default="")
    r.add_argument("--frames", default="", help="dir of numbered PNG frames")
    r.add_argument("--previous-format", default="", dest="previous_format")
    r.add_argument("--narrate", choices=["auto", "on", "off"], default="auto",
                   help="auto: narrate if TTS reachable; on: force; off: silent")
    r.add_argument("--tts-provider", default="", dest="tts_provider",
                   help="override config (voicevox | mock)")
    r.add_argument("--dry-run", action="store_true")
    r.set_defaults(func=cmd_render)

    t = sub.add_parser("tts", help="synthesize a script's narration (test VOICEVOX)")
    t.add_argument("--telemetry", required=True)
    t.add_argument("--experiment", default="")
    t.add_argument("--provider", default="", help="voicevox | mock")
    t.add_argument("--speaker", type=int, default=None)
    t.add_argument("--out", default="")
    t.set_defaults(func=cmd_tts)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
