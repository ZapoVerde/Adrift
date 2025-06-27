### 🌫️ Environmental Visibility Effects

**Status:** Locked

* Environmental effects reduce visibility by applying penalties during vision path evaluation.
* Each tile contains an `env` list. Each entry is a dict with fields like `type`, `visibility_penalty`, and `duration`.
* Effects accumulate linearly as vision passes through affected tiles.
* Rationale: Supports realistic occlusion (e.g. fog, smoke, steam) and time-based dissipation.

**📐 Architectural Implications**

* `tile['env']` is a list of dicts, each with fields like:
  - `type`: short string identifier (e.g. `"fog"`, `"smoke"`)
  - `visibility_penalty`: integer ≥ 1
  - `duration`: optional integer countdown

* Vision trace calls `accumulate_env_penalties(path)` to sum all encountered penalties.
* Penalties are applied after PER and light tier are resolved, reducing final visibility range.
* Effects may be time-aware: `duration` decrements per turn and expired effects are purged.

**🔄 Flow Integration**

* Integrated into `observe()` vision tracing logic.
* Influences both player and AI visibility.
* Can combine with light and terrain to simulate dense environments or concealed zones.
* Combat behaviors like smoke grenades or fire suppression hook directly into this system.

**🧠 Design Philosophy**

* Emphasizes realism and tactical variability in line-of-sight.
* Avoids binary “see or not” by supporting graduated perception impairment.
* Modular dict-based structure supports easy addition of new effects (e.g. gas, ash, mist).

**📝 Unstructured Notes**

* Can support multi-effect overlap and stacking if needed.
* Penalties could also influence target acquisition or aim penalties, though not yet implemented.
* Future effects might resist cleanup or interact with environment (e.g. fire clears fog).
* Visual effects can be layered over tiles in UI based on `env` contents.
