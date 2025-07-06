# STAGE 2 IMPLEMENTATION PLAN — TICK PHASE ENGINE

**Status:** STRUCTURE LOCKED\
**Version:** 1.0\
**Stage ID:** 2

---

## NAME + GOAL

**Name:** Tick Phase Engine\
**Goal:** Dispatch registered hook groups for each tick using clean modular phases

---

## STRATEGIC NARRATIVE

Tick progression must be structured into discrete system phases. Each tick consists of:

- Perception (sensory input gathering)
- Initiative (AI/system priority)
- Action (actor decisions and updates)
- Cleanup (remove expired effects, handle delays)

This stage introduces a dispatch engine that allows systems to register hooks per phase. The dispatcher will call these hooks every tick in the correct order.

---

## DURATION + PHASES

**Estimate:** 3.5 hours\
**Phases:** 2

---

## PHASE 2.1 — PHASE REGISTRY + DISPATCH CORE

**Goal:** Define tick phases and dispatch loop **Files:**

- `core/tick_phases.py` (PERMANENT)
- `services/hook_dispatcher.py` (PERMANENT)

**Imports:**

- `from debug_core.debug import debug`
- `from config import DEBUG_MODE`
- `from core.tick_clock import get_current_tick`

**Contracts:**

```python
TICK_PHASES = ["perception", "initiative", "action", "cleanup"]
def register_hook(phase: str, callback: Callable): ...
def dispatch_tick(): ...
```

- Each tick calls `dispatch_tick()`
- Hooks are stored per phase and executed in order
- Each hook receives no args and is responsible for side effects

**FBD:**

```
dispatch_tick()
→ for phase in TICK_PHASES:
    → call all registered callbacks in phase
    → debug("phase_executed", context=f"tick/{phase}")
```

**Lock Criteria:**

- `register_hook()` stores callbacks safely
- `dispatch_tick()` processes all phases
- Hooks log via `debug()` when run
- Supports testing hooks via fixture injection

---

## PHASE 2.2 — EMPTY PHASE REGISTRATION

**Goal:** Ensure all four tick phases execute cleanly even when empty **Files:**

- (shared with above)

**Imports:**

- `from core.tick_phases import dispatch_tick`

**Contracts:**

- Test that dispatching runs all four phases
- Empty phases emit `debug()` trace only

**FBD:**

```
Tick → dispatch_tick()
→ perception (no-op)
→ initiative (no-op)
→ action (no-op)
→ cleanup (no-op)
```

**Lock Criteria:**

- All four phases execute in correct order
- Logs appear in trace even when no systems are registered
- Future system registration will not require refactoring

---

## FBD SUMMARY

```
register_hook("action", my_callback)
dispatch_tick()
→ perception → initiative → action → cleanup
→ logs debug("phase_executed") per phase
```

---

## SIGHTLINES

**Upstream:** Tick Clock, Debug, Config\
**Downstream:** Actors, Perception, AI, Action Systems, Cleanup

---

## TAG POSTURE

- [PERMANENT]: `tick_phases.py`, `hook_dispatcher.py`

---

## STATUS

**STRUCTURE LOCKED** — phase registry and dispatch model are frozen

---

## DEPENDENCIES

**Predecessors:** Stage 0 (Instrumentation), Stage 1 (Tick Clock)\
**Successors:** Stage 3 (Actor Lifecycle), Stage 6 (Effects), Stage 11 (AI Dispatch)

---

## LOCK-IN CRITERIA

- All four phases must exist and dispatch in order
- Phase hooks can be safely registered and called
- All debug logs conform to tag schema and appear in trace
- Empty phase execution emits trace but causes no side effects

