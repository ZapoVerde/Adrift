### 🔁 Turn-Based Flow

**Status:** Locked

* Four stages: `Perception → Initiative → Action → Cleanup`.
* Implemented in `engine.py`, each stage routes to utility modules.
* Messaging is strictly externalized (see Messaging Architecture).
* Rationale: Separates world state changes from player logic. Ensures flexibility for AI, delay effects, and future time manipulation mechanics.

**📐 Architectural Implications**

* `engine.py` acts as orchestrator only — no logic embedded.
* Each phase dispatches to appropriate utility modules (e.g. `perception_utils.observe()`, `initiative_queue.roll()`, `action_handler.resolve_turn()`).
* Hook-ready structure: special states (e.g. stunned, on fire) can inject effects into specific phases.

**🔄 Flow Integration**

* Player actions and AI behavior are resolved in the Action phase, after perception and initiative.
* Initiative phase rolls determine order per round, with optional rerolls or delay effects.
* Cleanup phase handles status expiration, post-turn triggers, and visibility updates.

**🧠 Design Philosophy**

* Inspired by tactical TTRPGs and XCOM structure: clear event separation improves reasoning and debuggability.
* Keeps combat predictable yet allows complex emergent behavior via condition hooks.
* Prevents coupling of perception and action: e.g. no seeing and shooting in one atomic step.

**📝 Unstructured Notes**

* Early flow experiments collapsed perception into action, which reduced tactical nuance.
* The four-phase model allows finer control over turn order, timed buffs, and queued triggers.
* Supports future extensions like overwatch (check during others' Action phase).
* Player UI feedback can be structured phase-by-phase, making it easier to narrate or visualize combat.
* “Action” includes both actor choice and system resolution (e.g. traps, reactions).
* Certain events (e.g. alarms) can trigger mid-phase depending on architecture hooks.