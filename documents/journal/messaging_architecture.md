### 🎯 Messaging Architecture

**Status:** Locked

* All player-facing output must be routed through `messaging.py`.
* No raw strings are permitted in logic modules — even temporary output must use message functions.
* Messaging layer supports message types, formatting, suppression, and deferred output.
* Rationale: Centralizes narrative control, supports modular UI systems, and decouples logic from text.

**📐 Architectural Implications**

* `messaging.py` provides core functions: `notify_player()`, `log_combat()`, `narrate()`.
* All modules (combat, movement, perception) must import from messaging rather than using `print()` or inline strings.
* Messages may carry tags (e.g. `combat`, `alert`, `ambient`) for filtering.
* Log history may be stored for test assertions or event replay.

**🔄 Flow Integration**

* Combat results, perception outcomes, item discovery, and actor dialogue all route through this system.
* Messaging may differ by UI (e.g. text, tooltip, sidebar) but logic always emits a semantic message.
* Suppression rules prevent clutter (e.g. don't log every footstep unless in debug).

**🧠 Design Philosophy**

* Prevents message scatter and duplication.
* Enables test harnesses to assert exact messages under known conditions.
* Future-proof: supports localization, branching narrative modes, or alternate UIs.
* Enforces strict separation of simulation and narration.

**📝 Unstructured Notes**

* May later support message queuing or interruption (e.g. pause on critical discovery).
* Test suites should mock `messaging.py` to capture output.
* Narrative events (e.g. "the wall collapses") should still be routed through the same interface.
* Important for accessibility: allows screen reader or tooltip-friendly extensions.
