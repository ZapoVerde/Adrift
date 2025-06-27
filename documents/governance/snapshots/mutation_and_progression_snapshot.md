# ✅ Snapshot: Mutation & Skill Progression Subsystem

**Snapshot ID:** `MUT-SNAPSHOT-001`  
**Date:** 2025-06-26  
**Status:** 🔒 Locked & Stable  
**Tests:** ✅ 64/64 Passing  
**Purpose:** Foundation for XP-based technique evolution and mutation gating

---

## 📦 Code Modules

| File Path | Purpose |
|-----------|---------|
| `Adrift/definitions/actor.py` | Stores actor state: skills, techniques, XP |
| `Adrift/definitions/technique_defs.py` | Canonical technique data (id, rarity, tags) |
| `Adrift/definitions/skill_defs.py` | Canonical skill data (id, tags) |
| `Adrift/utils/skill_xp_utils.py` | XP gain, skill/technique visibility, level-up logic |
| `Adrift/utils/actor_offer_utils.py` | Generates gated evolution offers (based on visibility + boost) |
| `Adrift/utils/technique_mutation_utils.py` | Applies mutation operations (effects, modifiers) |
| `Adrift/flow/action_flow.py` | Calls `track_xp_gain()` from placeholder action runner |

---

## 🧠 Core Behaviors

### 🎓 Skill & Technique XP
- XP is only granted if skill/technique tags match input tags
- XP accumulates on success, rolls level-up probability:
