"""Job identity and output layout (§32).

Every run gets a unique ``job_id`` and its own directory under ``workspace/`` so
outputs are never overwritten and any single stage can be re-run in isolation.
The job_id is derived from inputs + a wall clock stamp passed *in* (we never call
time in library code paths that need to stay reproducible under test).
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class Job:
    job_id: str
    root: Path
    manifest: dict[str, Any] = field(default_factory=dict)

    def path(self, *parts: str) -> Path:
        p = self.root.joinpath(*parts)
        p.parent.mkdir(parents=True, exist_ok=True)
        return p

    def write_report(self, name: str, data: dict) -> Path:
        p = self.path(name)
        with p.open("w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
        return p


def make_job_id(prefix: str, seed: str, stamp: str) -> str:
    """Deterministic-ish id: prefix + short hash(seed) + caller-supplied stamp."""
    h = hashlib.sha1(seed.encode("utf-8")).hexdigest()[:8]
    return f"{prefix}_{stamp}_{h}"


def open_job(workspace: Path, job_id: str) -> Job:
    root = workspace / "renders" / job_id
    root.mkdir(parents=True, exist_ok=True)
    return Job(job_id=job_id, root=root)
