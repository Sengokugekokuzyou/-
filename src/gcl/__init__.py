"""GEKOKUJO Content Lab (GCL).

Simulate many worlds, detect the few events worth publishing, and turn them into
fact-based third-person RPG videos and BGM music videos for the Shirokuro Games
channel.

This package is intentionally decoupled from the GEKOKUJO game itself. The only
contract between them is the telemetry JSONL emitted by the game (see
``godot_bridge/telemetry_export``) and the captured frames/audio on disk.
"""

__version__ = "0.1.0"
