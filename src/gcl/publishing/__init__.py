"""Publisher (§28). Phase 1 exports locally only; YouTube modes land in Phase 5.

Publish modes (config/publishing.yaml): local_only | private | unlisted | scheduled.
Only Quality-Gate PASS videos may ever be scheduled (§28). This module is a
placeholder in v0.1 — the local export is handled by the render job itself.
"""
