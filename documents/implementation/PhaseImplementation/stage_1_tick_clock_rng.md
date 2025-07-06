# STAGE 1 IMPLEMENTATION PLAN — TICK CLOCK & RNG CORE

**Status:** STRUCTURE LOCKED\
**Version:** 1.0\
**Stage ID:** 1

---

## NAME + GOAL

**Name:** Tick Clock & RNG Core\
**Goal:** Provide deterministic tick control and reproducible RNG infrastructure

---

## STRATEGIC NARRATIVE

This stage provides time progression for the simulation and lays the foundation for all random behavior. It ensures:

- World tick counter is incremented correctly
- Tick time is deterministic and reproducible
- All randomness can be labeled and traced
- Seed setting is supported for tests and replays
- Audit trail is compliant with the debug framework

This is the heartbeat of the simulation. All actors, systems, and effects depend on this base layer for temporal progression and entropy.

---

## DURATION + PHASES

**Estimate:** 3.0 hours\
**Phases:** 2 (inline below)

---

## PHASE 1.1 — TICK CLOCK ENGINE

**Goal:** Implement and expose global tick counter\
**Files:**

- `core/tick_clock.py` (PERMANENT)
- `core/world_state.py` (PERMANENT)

**Imports:**

- `from config import DEBUG_MODE`
- `from debug_core.debug import debug`

**Contracts:**

```python
def advance_tick(): ...
def get_current_tick(): ...
```

- Global tick is advanced by `advance_tick()`
- Tick is retrieved by `get_current_tick()`
- Tick advancement triggers `debug()` call with `context="tick/advance"`

**FBD:**

```
advance_tick()
→ increment global tick
→ debug("tick_advanced", context="tick/advance", ai_tags=[...])
```

**Lock Criteria:**

- Tick is stored centrally in `world_state`
- `advance_tick()` modifies it safely
- `debug()` emits structured trace for each tick
- `get_current_tick()` returns correct value

---

## PHASE 1.2 — RNG SYSTEM CORE

**Goal:** Centralize and label all random usage\
**Files:**

- `services/random_source.py` (PERMANENT)

**Imports:**

- `import random`
- `from debug_core.debug import debug`
- `from config import DEBUG_MODE`

**Contracts:**

```python
def get_rng(label: str = "default") -> random.Random: ...
def set_seed(seed: int, stream: str = "default"): ...
```

- Random generators are retrieved via `get_rng(label)`
- Seeds are set deterministically using `set_seed()`
- Labels include `combat`, `worldgen`, etc.
- `debug()` logs every seed set and labeled generator use

**FBD:**

```
get_rng("combat")
→ rng_registry["combat"] → random.Random(seed)
set_seed(1234, stream="combat")
→ rng_registry["combat"].seed(1234)
→ debug("seed_set", label="combat")
```

**Lock Criteria:**

- `get_rng()` returns unique RNG per label
- `set_seed()` initializes RNG for deterministic testing
- All uses of RNG route through this service
- Trace logging shows label and action context

---

## FBD SUMMARY

```
advance_tick() → tick += 1 → debug("tick_advanced")
get_rng(label) → returns named random.Random instance
set_seed(seed, label) → debug("seed_set")
```

---

## SIGHTLINES

**Upstream:** Event bus, debug, config (from Stage 0)\
**Downstream:** Tick phase engine, actors, perception, combat, effects

---

## TAG POSTURE

- [PERMANENT]: `tick_clock.py`, `random_source.py`, `world_state.py`

---

## STATUS

**STRUCTURE LOCKED** — all module boundaries and contracts frozen

---

## DEPENDENCIES

**Predecessors:** Stage 0 (Instrumentation Foundations)\
**Successors:** Stage 2 (Tick Phase Dispatch), Stage 5 (Combat Execution), Stage 20 (WorldGen)

---

## LOCK-IN CRITERIA

- Global tick works and can be incremented
- Ticks are trace-logged using `debug()`
- RNG system returns named deterministic generators
- `set_seed()` sets seed per stream and logs event
- No direct use of `random` outside of `random_source`
- All debug calls meet tagging and trace rules

