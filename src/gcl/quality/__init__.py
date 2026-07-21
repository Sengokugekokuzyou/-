"""Quality Gate (§27): PASS / WARN / FAIL before anything is published."""

from .gate import run_gate, GateResult, Check

__all__ = ["run_gate", "GateResult", "Check"]
