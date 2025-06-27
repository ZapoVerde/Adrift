## 🥋 Technique System Overview

**Status:** Locked  
**Date:** 2025-06-25  
**Time:** 00:00 UTC

This system is fully specified and under governance. Any changes must be tracked in the Design Changelog and justified in the Audit Journal.

---

### 🔍 Summary

Techniques are tactical actions acquired through practice, not planning. Each skill may unlock **one unique technique**, which is procedurally assembled from a curated component library. The unlock process uses the same probabilistic XP model as skill growth. Once acquired, a technique can evolve through modular component changes, reflecting the actor's growing tactical fluency.

Techniques do **not scale by default** — all default effects are flat. Stat-based scaling is considered a rare modifier only available through specific evolution paths.

---

### 📐 Architectural Implications

- Techniques are actor-unique and non-transferable.
- Each skill has a one-to-one mapping to at most one technique per actor.
- Techniques consist of:
  - One optional **trigger**
  - One or more **effects**
  - Zero or one **modifier** (e.g., `on_crit`, `vs_condition`, `stat_scaling`)
- Components are drawn from a locked library (`technique_component_library.py`)
- Techniques must be thematically appropriate for the originating skill
- Evolution modifies component structure only — not number of uses or cooldown
- Techniques never appear unless skill level ≥ 2 and unlock roll succeeds

---

### 🔄 Flow Integration

- On a successful skill-tagged action:
  - XP is added to the skill (as normal)
  - If skill is visible and level ≥ 2 → technique unlock roll is attempted
  - If roll succeeds → technique is generated procedurally
- Player choices:
  - Accept technique → it becomes bound to the actor
  - Reject technique → discard; next unlock requires fresh success and roll
- On technique use:
  - XP accumulates per use
  - On level-up, player chooses a modular evolution:
    - Replace a component (e.g., `bleed` → `push`)
      - The replacement **must not** duplicate the component being replaced
    - Add a new component (if limit not exceeded)
    - Apply a rare modifier (e.g., `stat_scaling`, `on_crit`)

---

### 🧠 Design Philosophy

- Techniques are **player-facing verbs**, not passive traits
- Procedural variation ensures emergent identity and expressive combat
- One-per-skill limit prevents bloat and maintains readability
- Flat effect model reinforces predictability and mechanical clarity
- Evolution is personal: no two actors will likely refine the same technique the same way
- Rejecting a technique is a valid tactical decision — but comes with opportunity cost

---

### 📝 Unstructured Notes

- Techniques never appear at level 1 — this is intentional to avoid early overload
- Composure and other activation costs are deferred (system disabled for MVP)
- Named techniques may be generated with flavor hooks, but names are cosmetic
- Effects stack only if component rules allow it (e.g., `bleed` yes, `push` no)
- Component limits: 1 trigger, 1–2 effects, 0–1 modifier
- Evolution trees should remain shallow and irreversible
- Future: technique inspiration or copying via observed enemies may be possible
