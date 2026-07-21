"""Telemetry ingest: read the event stream the game emits (see EVENT_SCHEMA.md)."""

from .schema import Event, REQUIRED_FIELDS
from .reader import read_events, ReaderError

__all__ = ["Event", "REQUIRED_FIELDS", "read_events", "ReaderError"]
