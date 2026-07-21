"""Configuration + path resolution.

All tunables live in ``config/*.yaml`` (§32 "設定ファイルで変更可能",
"絶対パスをハードコードしない"). Paths are resolved relative to the project root
unless absolute, so the same checkout works on Linux and Windows.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = PROJECT_ROOT / "config"


def load_config() -> dict[str, Any]:
    """Merge every ``config/*.yaml`` under a key named after the file stem."""
    cfg: dict[str, Any] = {}
    if CONFIG_DIR.exists():
        for f in sorted(CONFIG_DIR.glob("*.yaml")):
            with f.open("r", encoding="utf-8") as fh:
                cfg[f.stem] = yaml.safe_load(fh) or {}
    return cfg


def resolve_path(value: str | Path) -> Path:
    p = Path(value)
    return p if p.is_absolute() else (PROJECT_ROOT / p)


def get(cfg: dict, dotted: str, default: Any = None) -> Any:
    """`get(cfg, "app.channel_name")` — dotted lookup with a default."""
    cur: Any = cfg
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return default
        cur = cur[part]
    return cur
