## 📚 Technique Component Library – Journal Summary

**Status:** Locked
**Date:** 2025-06-25
**Time:** 00:00 UTC

This document provides governance and integration notes for the procedural technique component registry (`technique_component_library.py`).

It defines the permitted structure, constraints, and mutation rules for all components used in procedural technique generation. All entries are subject to governance and must conform to locked architectural and gameplay models.

---

### 🔍 Summary

Technique components are the atomic parts of procedural combat techniques. Each component fits into one of three mutually exclusive roles:

* **Triggers**: Conditions for activating a technique (e.g., "on first strike", "if flanked")
* **Effects**: The mechanical payload (e.g., "apply bleed", "push target")
* **Modifiers**: Conditionals or amplifiers (e.g., "on crit", "vs burning target", `stat_scaling`)

Each technique is composed of:

* 0–1 Triggers
* 1–2 Effects
* 0–1 Modifiers

Component entries are stored as dicts with locked fields such as:

```python
{
  "id": "bleed",
  "type": "effect",
  "description": "Applies a bleed effect on hit",
  "rare": False,
  "locked": True
}
```

---

### 📐 Architectural Implications

* Components are stored in a central Python module: `technique_component_library.py`
* Components are grouped by type and registered under `ALL_COMPONENTS`
* Component fields are static — any field schema change requires audit
* `rare` flag controls component accessibility during procedural generation
* `locked` flag ensures governance: all components must be reviewed before use
* `stat_scaling` and similar mechanics are only allowed via explicitly flagged `rare=True` modifiers
* A helper function (e.g., `validate_component(component)`) must exist to enforce schema compliance

---

### 🔄 Flow Integration

* During technique unlock:

  * Components are selected based on type, rarity, and compatibility with the actor’s skill
  * Illegal or disallowed combinations are excluded
  * Modifiers are only attached if compatible with effect logic

* During technique evolution:

  * Player may choose to swap a component with another of the same type
  * Some evolution branches may allow adding a second effect (if none exists)
  * Rare components may become available as choices, but only post-unlock

---

### 🧠 Design Philosophy

* Flat structure maximizes clarity, testability, and balance auditing
* Component count is intentionally small during MVP to ensure tight control
* Modifiers should change tactical value, not raw damage
* Effects should remain interpretable and expressive in UI
* Rarity controls narrative flavor and tactical complexity

---

### 📝 Unstructured Notes

* `stat_scaling` is disabled by default and must never appear unless chosen through evolution
* No component may alter cooldown, cost, or composure — those systems are deferred
* Future tags (`tags`, `combo_with`, etc.) may allow more contextual logic but must not affect current systems
* Allowing components to stack (`bleed+push`) must be carefully curated — some will be mutually exclusive
* All additions must pass a validation script and have tests in `test_technique_components.py`
