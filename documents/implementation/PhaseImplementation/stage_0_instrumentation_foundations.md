# STAGE 0 IMPLEMENTATION PLAN — INSTRUMENTATION FOUNDATIONS

**Status:** STRUCTURE LOCKED\
**Version:** 1.0\
**Stage ID:** 0

---

## NAME + GOAL

**Name:** Instrumentation Foundations\
**Goal:** Establish debug, trace, tagging, and config scaffolding

---

## STRATEGIC NARRATIVE

Minimum developer instrumentation backbone. Provides:

- Debug output with AI-aligned tagging
- Tag vocabulary scaffolding for MECE enforcement
- Configuration toggle support
- Event bus skeleton (non-functional, for compatibility)
- Compliant with MVP modularity core: flat references, tags, JSON-first

Supports runtime trace visibility and simulation replay.

---

## DURATION + PHASES

**Estimate:** 2.0 hours\
**Phases:** 2 (inline below)

---

## PHASE 0.1 — DEBUG CORE + TAG VOCAB

**Goal:** Provide structured debug logging with MECE tag validation\
**Files:**

- `debug_core/debug.py` (PERMANENT)
- `tags_vocab.json` (PERMANENT)

**Imports:**

- `os`, `json`, `datetime`
- `from config import DEBUG_MODE`
- `from debug_core.tags_vocab import validate_tags`
- `from uuid import uuid4` (optional)

**Contracts:**

```python
def debug(message, context, ai_tags, action, data=None, state=None, trace_id=None):
```

- Tags validated against loaded vocab
- Output is JSONL structured line with `timestamp`, `action`, `context`, `tags`
- `ai_tags` must match MECE rule: 1 tag per group

**FBD:**

```
Caller → debug(msg, ctx, tags, action, ...)
      → validate_ai_tags(tags) → tags_vocab.json
      → emit JSONL (disk or stdout)
```

**Correct debug implementation must:**

- Call `validate_tags(ai_tags)` before emit
- Raise `ValueError` on tag failure
- Write to `debug_logs/{context}.jsonl`
- Never call `print()`
- Include: `context`, `action`, `ai_tags`, `timestamp`
- Support trace\_id, data, state (optional)
- Adhere to contract in `AI and Human User Guide.txt`

**Lock Criteria:**

- `debug()` implemented and emits structured trace
- `tags_vocab.json` schema loaded and applied
- `print()` never used
- All tag groups validated per MECE rules
- Fails loudly on bad/missing tags or action syntax

---

## PHASE 0.2 — EVENT BUS SHELL + CONFIG LOADER\$1**Files:**

- `services/event_bus.py` (DEAD-END)
- `config/config.py` (PERMANENT)
- `/config/config.py` must define `get_config()` and `DEBUG_MODE`, importable as `from config import get_config, DEBUG_MODE`

**Imports:**

- `from debug_core.debug import debug`
- `from config import get_config, DEBUG_MODE`
- `from config import DEBUG_MODE`

**Contracts:**

```python
def publish(event_dict): ...
def get_config(key): ...
```

- `publish()` logs trace via `debug()`
- `get_config()` returns from static config dict
- Events must include `ai_tags`, validated

**FBD:**

```
publish(event_dict) → debug("publish_event", context="event_bus/publish")
get_config(key) → config_dict[key]
```

**Lock Criteria:**

- `publish()` emits via debug()
- `get_config()` returns test-safe values
- Config file includes `DEBUG_MODE`
- No routing logic in event bus
- Config compliance supports test overrides

---

## FBD SUMMARY

```
User/System → debug() → validate_tags() → emit JSONL trace
publish() → debug()
get_config() → static dict
```

---

## SIGHTLINES

**Upstream:** Planning, Tick Dispatch\
**Downstream:** All system debug, event bus, AI trace

---

## TAG POSTURE

- [PERMANENT]: `debug.py`, `config.py`, `tags_vocab.json`
-

---

## STATUS

**STRUCTURE LOCKED** — pseudocode and module boundaries frozen

---

## DEPENDENCIES

**Predecessors:** None (foundational)\
**Successors:** Stage 1 (Tick Clock & RNG), Stage 2 (Tick Phase Dispatch)

---

## LOCK-IN CRITERIA

- `debug()` accepts all standard args, emits JSONL trace
- `ai_tags` validated against `tags_vocab.json`
- `get_config()` reads from static config dict
- `publish()` emits via `debug()`
- No use of `print()` in any debug logic
- Config file must exist and be test-overridable
- All debug calls meet Pareto Debugging Framework spec

