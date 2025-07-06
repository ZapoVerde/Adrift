▓▓▓ ADRIFT PROJECT — REORDERED IMPLEMENTATION PLAN ▓▓▓ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 🧩 Purpose: Ensure all dependencies are installed before any referencing system in every stage. 📍 Scope: First 5 stages only, with detailed phase plans added for each. 📡 Debug Compliance: All debug calls must emit structured logs with ai\_tags, follow verb\_noun format, and avoid print(). Use `debug_adapter.get_debugger()` for all instrumentation.

──────────────────────────────────────────────────── STAGE 0 — Instrumentation Foundations ──────────────────────────────────────────────────── ✅ Goal: Establish debug, trace, tagging, and config scaffolding. ⌛️ Estimate: 2 hours 📄 Phases: 2

PHASE 0.1 — Debug Core + Config ──────────────────────────────── Goal: Provide runtime debug() with ai\_tags, and basic config toggles. Estimate: 2 hours Tasks:

- Define debug() function with tag and trace support  ✅ STRUCTURE
- Implement `config.py` with DEBUG\_MODE toggle        ✅ IMPLEMENTATION
- Generate `tags_vocab.json` with MECE structure     ✅ IMPLEMENTATION
- Add trace\_id and ai\_tags support to debug()        ✅ IMPLEMENTATION
- Add placeholder test for debug trace emitter       ✅ IMPLEMENTATION
- Use `get_debugger()` from `debug_adapter`          ✅ IMPLEMENTATION Lock-In Trigger: debug() emits trace\_id and ai\_tags; config toggles work.

Pseudocode:

```python
# config.py
debug_mode = True

# debug_core/debug_utils.py
def get_debugger(context):
    return lambda action, data=None, state=None, trace_id=None, ai_tags=None, print_console=False: ...

# adapters/debug_adapter.py
def get_debugger(context):
    from debug_core.debug_utils import get_debugger
    return get_debugger(context)
```

PHASE 0.2 — Event Bus Stub [DEAD-END] ──────────────────────────────────── Goal: Create placeholder event publishing system. Estimate: 1 hour Tasks:

- Define `publish()` stub in `event_bus.py`          ✅ STRUCTURE
- Route all calls through debug() using context      ✅ IMPLEMENTATION
- Log every call with `event_type` + payload         ✅ IMPLEMENTATION
- Add @status: "deadend" to file header              ✅ IMPLEMENTATION
- Validate adapter interface placeholder             ✅ STRUCTURE Lock-In Trigger: publish() accepts event dict and logs with ai\_tags

Pseudocode:

```python
# services/event_bus.py
# @status: "deadend"
def publish(event_type: str, payload: dict, trace_id=None):
    dbg = get_debugger("services/event")
    dbg(action="publish_event", data={"event_type": event_type, "payload": payload}, trace_id=trace_id,
        ai_tags=["event", "actor_data", "mvp", "runtime_behavior"])
```

──────────────────────────────────────────────────── STAGE 1 — Tick Clock & RNG Core ──────────────────────────────────────────────────── ✅ Goal: Provide deterministic tick control and RNG backbone. ⌛️ Estimate: 3 hours 📄 Phases: 2

PHASE 1.1 — Tick Advancement ──────────────────────────── Goal: Advance tick counter and publish TickEvent Estimate: 2 hours Dependencies: event\_bus, config, debug Tasks:

- Define `advance_tick(world_state)` in `tick_clock.py` ✅ STRUCTURE
- Add debug() emit with current tick                     ✅ IMPLEMENTATION
- Publish TickEvent with tags                            ✅ IMPLEMENTATION
- Include test for tick advancement                      ✅ IMPLEMENTATION
- Ensure event logs with ai\_tags                         ✅ IMPLEMENTATION Lock-In Trigger: world\_state["tick"] increments; TickEvent publishes.

Pseudocode:

```python
# core/tick_clock.py
def advance_tick(world_state: dict, trace_id=None):
    world_state["tick"] += 1
    dbg = get_debugger("core/tick")
    dbg(action="advance_tick", state={"tick": world_state["tick"]}, trace_id=trace_id,
        ai_tags=["time", "actor_data", "mvp", "runtime_behavior"])
    publish("TickEvent", {"tick": world_state["tick"]}, trace_id=trace_id)
```

PHASE 1.2 — RNG with Traceable Labels ──────────────────────────────────── Goal: Add traceable, label-based random() function Estimate: 1 hour Dependencies: debug core Tasks:

- Define `get_rng(label)` using Python random           ✅ STRUCTURE
- Add trace\_id to all outputs using debug()            ✅ IMPLEMENTATION
- Ensure deterministic seeding (optional now)          ✅ IMPLEMENTATION
- Emit debug logs per roll with ai\_tags                ✅ IMPLEMENTATION
- Add stub tests                                        ✅ IMPLEMENTATION Lock-In Trigger: All RNG emits label and trace id to debug.

Pseudocode:

```python
# core/random_source.py
import random

def get_rng(label: str, trace_id=None):
    roll = random.randint(1, 6)
    dbg = get_debugger("core/rng")
    dbg(action="roll_rng", data={"label": label, "value": roll}, trace_id=trace_id,
        ai_tags=["time", "actor_data", "mvp", "runtime_behavior"])
    return roll
```

──────────────────────────────────────────────────── STAGE 2 — Tick Phase Engine ──────────────────────────────────────────────────── ✅ Goal: Dispatch registered hook groups each tick ⌛️ Estimate: 3.5 hours 📄 Phases: 3

PHASE 2.1 — Hook Dispatcher Setup ───────────────────────────────── Goal: Provide central dispatch\_hooks() utility for phase execution. Estimate: 1.5 hours Dependencies: event\_bus, debug Tasks:

- Define `dispatch_hooks(phase, world_state)`         ✅ STRUCTURE
- Accept string key + WORLD\_STATE                     ✅ IMPLEMENTATION
- Log dispatch start/end with ai\_tags                 ✅ IMPLEMENTATION
- Return aggregated hook results                      ✅ IMPLEMENTATION
- Unit test with dummy hooks                          ✅ IMPLEMENTATION Lock-In Trigger: Dispatcher accepts hooks and logs properly.

Pseudocode:

```python
# services/hook_dispatcher.py
def dispatch_hooks(phase: str, world_state: dict, trace_id=None):
    dbg = get_debugger("hooks/dispatcher")
    dbg(action="start_phase", data={"phase": phase}, trace_id=trace_id,
        ai_tags=["time", "actor_data", "mvp", "runtime_behavior"])
    results = []
    for hook_fn in REGISTERED_HOOKS.get(phase, []):
        result = hook_fn(world_state, trace_id)
        results.append(result)
    dbg(action="end_phase", data={"phase": phase, "results": results}, trace_id=trace_id,
        ai_tags=["time", "actor_data", "mvp", "runtime_behavior"])
    return results
```

PHASE 2.2 — Tick Phase Loop Definition ───────────────────────────────────── Goal: Create core tick phase loop with correct ordering Estimate: 1 hour Dependencies: dispatcher, tick\_clock Tasks:

- Define ordered list: perception → action → cleanup → messaging ✅ STRUCTURE
- Call dispatcher for each                                        ✅ IMPLEMENTATION
- Log phase transitions with ai\_tags                              ✅ IMPLEMENTATION
- Hook phase outputs into debug()                                 ✅ IMPLEMENTATION
- Validate modularity contract                                    ✅ STRUCTURE Lock-In Trigger: All 4 tick phases dispatched in correct order.

Pseudocode:

```python
# core/tick_phases.py
def run_tick(world_state: dict, trace_id=None):
    for phase in ["perception", "action", "cleanup", "messaging"]:
        dispatch_hooks(phase, world_state, trace_id)
```

PHASE 2.3 — Empty Hook Registration ─────────────────────────────────── Goal: Register and validate placeholder hooks Estimate: 1 hour Tasks:

- Add dummy function hooks (e.g. log phase marker)     ✅ IMPLEMENTATION
- Validate that hooks fire during correct phase        ✅ IMPLEMENTATION
- Log execution via debug()                            ✅ IMPLEMENTATION
- Mark hooks with ai\_tags                              ✅ IMPLEMENTATION
- Validate dispatcher extensibility                    ✅ STRUCTURE Lock-In Trigger: All empty phases log and can be extended.

Pseudocode:

```python
# systems/example_hooks.py
def dummy_hook(world_state, trace_id=None):
    dbg = get_debugger("hooks/dummy")
    dbg(action="hook_called", state={"tick": world_state.get("tick")}, trace_id=trace_id,
        ai_tags=["time", "actor_data", "mvp", "runtime_behavior"])

REGISTERED_HOOKS = {
    "perception": [dummy_hook],
    "action": [],
    "cleanup": [],
    "messaging": []
}
```

──────────────────────────────────────────────────── STAGE 3 — Actor Lifecycle + Tags ──────────────────────────────────────────────────── ✅ Goal: Define actor tickability, condition states, and control flags ⌛️ Estimate: 3 hours 📄 Phases: 2

PHASE 3.1 — Actor Tag Scaffolding ───────────────────────────────── Goal: Provide tag-based control over actor activity Estimate: 1.5 hours Dependencies: world\_state, dispatch\_hooks Tasks:

- Define is\_tickable(actor\_dict) function              ✅ STRUCTURE
- Accept tags: asleep, stunned, frozen, etc           ✅ IMPLEMENTATION
- Log tag evaluation results with ai\_tags             ✅ IMPLEMENTATION
- Add test fixtures for sample actor dicts            ✅ IMPLEMENTATION
- Tag all outputs                                      ✅ IMPLEMENTATION Lock-In Trigger: Tickability works based on tags

Pseudocode:

```python
# systems/actor_state.py
def is_tickable(actor: dict, trace_id=None):
    tags = actor.get("tags", [])
    tickable = not any(tag in tags for tag in ["asleep", "stunned", "frozen"])
    dbg = get_debugger("actor/tickable")
    dbg(action="check_tickable", data={"tags": tags, "tickable": tickable}, trace_id=trace_id,
        ai_tags=["combat", "actor_data", "mvp", "runtime_behavior"])
    return tickable
```

PHASE 3.2 — Condition Timers and Transitions ──────────────────────────────────────────── Goal: Add turn-based conditions (e.g. sleep counter) Estimate: 1.5 hours Tasks:

- Define condition\_timer field in actor\_dicts          ✅ STRUCTURE
- Auto-decrement each tick during cleanup phase        ✅ IMPLEMENTATION
- Clear tags upon expiry                               ✅ IMPLEMENTATION
- Log each transition via debug()                      ✅ IMPLEMENTATION
- Add tests for sleep recovery                         ✅ IMPLEMENTATION Lock-In Trigger: Conditions expire and modify actor tickability

Pseudocode:

```python
# systems/actor_state.py
def apply_conditions(actor: dict, trace_id=None):
    changed = False
    if "condition_timer" in actor:
        actor["condition_timer"] -= 1
        if actor["condition_timer"] <= 0:
            actor["tags"] = [tag for tag in actor["tags"] if tag != "asleep"]
            actor.pop("condition_timer")
            changed = True
    dbg = get_debugger("actor/conditions")
    dbg(action="update_conditions", state=actor, trace_id=trace_id,
        ai_tags=["combat", "actor_data", "mvp", "runtime_behavior"])
    return changed
```

──────────────────────────────────────────────────── STAGE 4 — Wait / Move Actions ──────────────────────────────────────────────────── ✅ Goal: First actions that modify world\_state and consume ticks ⌛️ Estimate: 4 hours 📄 Phases: 3

PHASE 4.1 — Action Interface Contract ──────────────────────────────────── Goal: Define action format with validate(), execute(), duration\_ticks Estimate: 1.5 hours Dependencies: world\_state, tick\_clock Tasks:

- Define base action dict format                       ✅ STRUCTURE
- Write ActionResult template                         ✅ IMPLEMENTATION
- Log action lifecycle using ai\_tags                   ✅ IMPLEMENTATION
- Unit test sample wait action                         ✅ IMPLEMENTATION
- Validate soft data contract                          ✅ STRUCTURE Lock-In Trigger: wait action returns valid ActionResult

Pseudocode:

```python
# systems/actions/base.py
def make_action_result(success: bool, message: str, events=None):
    return {
        "success": success,
        "message": message,
        "events": events or []
    }

# Example action structure:
# {
#     "name": "wait",
#     "duration_ticks": 1,
#     "validate": validate_fn,
#     "execute": execute_fn
# }
```

PHASE 4.2 — Wait Action Implementation ───────────────────────────────────── Goal: Execute a do-nothing action that consumes time Estimate: 1 hour Tasks:

- Implement validate() as always true                  ✅ IMPLEMENTATION
- Implement execute() to log and consume ticks        ✅ IMPLEMENTATION
- Add tick delay via duration\_ticks                   ✅ IMPLEMENTATION
- Register as action hook                             ✅ IMPLEMENTATION
- Test across multiple ticks                          ✅ IMPLEMENTATION Lock-In Trigger: Wait executes and delays actor

Pseudocode:

```python
# systems/actions/wait.py
def validate(actor, world_state):
    return True

def execute(actor, world_state, trace_id=None):
    dbg = get_debugger("actions/wait")
    dbg(action="execute_wait", data={"actor": actor.get("id")}, trace_id=trace_id,
        ai_tags=["combat", "actor_data", "mvp", "runtime_behavior"])
    return make_action_result(True, "Actor waits.")

WAIT_ACTION = {
    "name": "wait",
    "duration_ticks": 1,
    "validate": validate,
    "execute": execute
}
```

PHASE 4.3 — Move Action with Validation ────────────────────────────────────── Goal: Execute directional movement action Estimate: 1.5 hours Dependencies: actor\_dict, world\_state Tasks:

- validate\_move() uses tile boundaries                ✅ STRUCTURE
- execute() updates actor position                    ✅ IMPLEMENTATION
- ActionResult returns old → new coords               ✅ IMPLEMENTATION
- Add test with impassable terrain                    ✅ IMPLEMENTATION
- Add movement log with ai\_tags                       ✅ IMPLEMENTATION Lock-In Trigger: Actor moves only on legal tiles with correct log

Pseudocode:

```python
# systems/actions/move.py
def validate(actor, world_state):
    return validate_move(actor, dx=0, dy=1)  # example: move south

def execute(actor, world_state, trace_id=None):
    old = actor["pos"]
    new = (old[0], old[1] + 1)
    actor["pos"] = new
    dbg = get_debugger("actions/move")
    dbg(action="execute_move", data={"from": old, "to": new, "id": actor.get("id")}, trace_id=trace_id,
        ai_tags=["movement", "actor_data", "mvp", "runtime_behavior"])
    return make_action_result(True, f"Actor moved to {new}.")

MOVE_ACTION = {
    "name": "move",
    "duration_ticks": 1,
    "validate": validate,
    "execute": execute
}
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ✓ All phases now obey dependency-first ordering ✓ Debug logging complies with Pareto framework ✓ Each phase includes MECE ai\_tags and avoids print() ✓ Next stage: Implement FBD overlays or proceed to Stage 5 breakdown

