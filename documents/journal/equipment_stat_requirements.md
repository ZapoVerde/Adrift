### 🛠️ Equipment Stat Requirements

**Status:** Locked

* Items define handling expectations based on STR, DEX, and PER.
* Stats are soft gates only — actors may equip any item regardless of stats.
* Shortfalls apply handling penalties: slower actions, accuracy penalties, or fumble risk.
* Skills never gate item use. They influence reliability, outcome consistency, and failure mitigation.
* Rationale: Supports emergent play, misfit character builds, and non-blocking gear access.

**📐 Architectural Implications**

* Items declare:
  - `base_damage`: numeric
  - `timing_stats`: list of STR/DEX fields that affect speed
  - `control_stats`: list of PER-related fields that affect accuracy
  - `required_skill`: weapon skill used for roll boosts and failure reduction
  - `critical_failure_mode`: flavor keyword for mishandling (e.g. `"misfire"`, `"drop"`)
  - `stat_bonus_caps`: optional `dict` of `stat → cap` value beyond which bonus does not apply

* Runtime checks:
  - Compute stat shortfall deltas
  - Apply timing and roll penalties proportionally
  - Apply bonuses from stats if they exceed thresholds (weapon-specific rules)
  - Cap bonuses as defined — e.g. STR may improve timing up to a point, but not beyond
  - Check skill level for roll bonuses and critical failure suppression
  - Certain weapons allow one stat to influence both timing and control ("double dipping")

**🔄 Flow Integration**

* Integrated into all item-based action flows: equipping, attacking, using, throwing.
* Core combat loop (`resolve_attack`) calculates:
  - Penalties from under-threshold stats
  - Bonuses from over-threshold stats (subject to caps)
  - Skill-based accuracy improvements
  - Critical failure risk scaling by skill
* All narrative output flows through `messaging.py`.

**🧠 Design Philosophy**

* Stats determine what is possible; skills determine how reliable the result is.
* Each weapon defines which stats influence timing and control.
* Some stats may boost one or both performance areas, and may be capped to reflect realism.
* Design encourages narrative and tactical variety without hard gating.

**📝 Unstructured Notes**

* Example: STR 4 actor uses STR 8 shotgun → -2 roll, slow recovery, high fumble chance.
* STR above requirement might reduce timing delay — but capped if unrealistic.
* DEX might improve draw speed, PER might stabilize aim — depends on weapon config.
* Skill fallback model allows partial benefit even if actor lacks exact weapon training.
* Visual indicators may flag suboptimal gear fits (e.g. orange border for mismatch).
* Design encourages experimentation and accommodates absurd loadouts narratively.
