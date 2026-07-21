# Normal video script structure (§21)

The Narrative Builder emits lines in this order. Each asserted line must carry the
`event_id`(s) it came from — the Quality Gate FAILs any asserted line without a
source (anti-fabrication, §21).

| Section | Purpose | Rule |
|---|---|---|
| Hook | The most striking recorded moment (highest `visual_priority`) | Fact only. |
| Question | The experiment's question | From the experiment definition. |
| Setup | Where/who/when | Fact only. |
| Escalation | The recorded chain, in order | Causes stated **only** when `cause_ids` exist. |
| Focus Character | The protagonist's thread | Fact only. |
| Turning Point | The transformation / peak event | Fact only. |
| Result | The last recorded state | No exaggeration. |
| Interpretation | Meaning | **Hedged** ("〜した可能性があります" / "ログ上では〜"). |
| Steam CTA | Link to the game | — |

## Forbidden (§21)
Invented dialogue, asserted emotions/intentions not in the log, changed
head-counts or day-counts, exaggerated results, fabricated causality, ads for
non-existent features.

## Hedged phrasings for interpretation
- 「〜だった可能性があります」
- 「ログ上では〜が直前に発生しています」
- 「〜が影響したと考えられます」

See `packaging/script_builder.py` for the implementation and
`content/experiments/food_shortage_glen_script_sample.md` for generated output.
