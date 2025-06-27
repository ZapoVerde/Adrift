# 🚀 MVP Progress Tracker

This document tracks the implementation progress of all systems required for the **Minimal Viable Prototype (MVP)**.

---

## ✅ MVP Definition

The MVP is defined as:

> A fully functional, testable tactical combat loop featuring:
> - Tile-based floorplan with actor navigation
> - Visibility, stealth, and perception logic
> - Damage resolution and body targeting
> - Inventory and equipment handling
> - Action queueing and interruption
> - Core messaging and feedback through `messaging.py`

It excludes:
- Narrative systems
- Full character progression
- Faction simulation or overworld movement

---

## 🧩 MVP System Checklist

| #  | System                            | Locked | Implemented | Notes |
|----|-----------------------------------|--------|-------------|-------|
| 1  | Damage Multiplier Model           | ✅     | ❌          | Formula defined; needs utility & test coverage |
| 2  | Body Targeting System             | ✅     | ❌          | Weighted random logic needs implementation     |
| 3  | Vision & Perception System        | ✅     | ✅          | Fully implemented with env/light/path tracing  |
| 4  | Inventory Size Model              | ✅     | ❌          | Item sizing & cap structure defined            |
| 5  | Turn-Based Flow                   | ✅     | ✅          | Engine flow split into phases; hooks live      |
| 6  | Tactical Tile Model               | ✅     | ✅          | Tile dicts, parsing, and mutation in place     |
| 7  | World & Lazy Hex Structure        | ✅     | ❌          | World registry and lazy loading model defined  |
| 8  | Light Tier Visibility Model       | ✅     | ✅          | Light limits tied to PER & trace visibility    |
| 9  | Environmental Visibility Effects  | ✅     | ✅          | Env penalties integrated in observe()          |
| 10 | Messaging Architecture            | ✅     | ✅          | `messaging.py` routing enforced                |
| 11 | Equipment Stat Requirements       | ✅     | ❌          | Modifier calculation scaffold needed           |
| 12 | Overkill Weapons                  | ✅     | ❌          | ITEM_DB entries and fail modes pending         |
| 13 | Stealth & Detection Mechanics     | ✅     | ✅          | search(), stealth, PER vs size all live        |
| 14 | Action Queuing & Interrupt Logic  | ✅     | ❌          | Tags & flush logic designed, not implemented   |

---

## 🏁 MVP Completion Estimate

| Phase          | Status       |
|----------------|--------------|
| Architecture   | ✅ Complete  |
| Tactical Logic | 🔄 Partial   |
| Combat Core    | 🔄 Incomplete |
| Input/Output   | ✅ Complete  |
| AI Systems     | ❌ Not scoped |
| Test Coverage  | 🔄 Needed    |

---

## ⏭️ Next Priorities

1. Implement core combat resolution:
   - roll + multiplier + targeting
2. Build equipment + stat integration
3. Add inventory size limits and handling
4. Wire action queues to input + interrupt hooks
5. Finalize tests for perception + vision + stealth

---

📝 All fields must be updated manually after changes. Auto-tracking TBD.
