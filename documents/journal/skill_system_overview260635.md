## 🎓 Skill System Overview

**Status:** Locked  
**Date:** 2025-06-25  
**Time:** 00:00 UTC

This system is fully specified and under governance. Any changes must be tracked in the Design Changelog and justified in the Audit Journal.

---

### 🔍 Summary

Skills represent learned behavior patterns grounded in actor experience. They are organized hierarchically (e.g., `melee → sword → rapier`) and grow through successful use. Actors do not start with all skills — instead, new ones emerge organically through repeated success with associated equipment or actions. Each skill can unlock one unique, procedurally generated technique.

XP is accumulated on successful use only. Unlocks and leveling use the same probabilistic model:

```python
chance = xp / (xp + difficulty(level))
```

This ensures that skill growth is emergent, contextual, and grounded in actual behavior, not player-selected upgrades.

---

### 📐 Architectural Implications

- Skills are tracked as structured hierarchies (tree model: general → specific → specialized)
- XP is logged separately per skill, regardless of shared ancestry
- Skills are not auto-visible: actors gain XP in hidden skills before reaching level 1
- The UI only surfaces skills once they reach a functional threshold (level 1 or higher)
- Parent skills may be used as fallback when no child skill is present, but not the reverse
- Technique generation requires skill level ≥ 2 and successful roll

---

### 🔄 Flow Integration

- On action:
  - All skill tags associated with the action are checked
  - If skill is known: XP is added
  - If skill is unknown: XP is still added, silently
- At the end of action resolution:
  - XP roll is performed per known or hidden skill
  - If roll passes and level threshold is met → skill levels up
  - If skill hits level 1 for the first time → skill becomes visible

- Techniques unlock only via the same XP-based probability model and only after the skill is visible and level ≥ 2
- Actors may only have one technique per skill

---

### 🧠 Design Philosophy

- Skills are earned, not assigned — they are retrospective reflections of actor behavior
- Hierarchical skill structure allows generalists to be viable early, with specialism emerging over time
- Hidden XP in unknown skills allows actors to "discover" aptitudes naturally
- Skill progression should surprise the player occasionally — not always be under their control
- XP is not a currency — it is a signal of actor reliability and success

---

### 📝 Unstructured Notes

- Skill decay is not currently modeled, but may be introduced under fatigue, trauma, or memory systems
- Skill tags should be consistently applied across items, techniques, and world interactions
- No player-assigned skills: all growth is event-driven
- Skills should appear sparse early-game to avoid UI clutter
- Internal growth curves should be visible via debug tooling
- Skill merge/compression rules may be introduced if trees become too deep
