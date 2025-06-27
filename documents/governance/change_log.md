# 🪵 Design Change Log

This document captures all meaningful design changes after a system is marked `Locked`.

Each entry must include:
- Timestamp
- Changed system(s)
- Summary of change
- Reason for change
- Impact (e.g., testing, refactoring)
- Follow-up actions if needed

---

### 📅 2025-06-23 – Clarified “Locked” vs “Implemented” Status
**System(s):** Governance  
**Change:** Defined difference between locked design and implemented code  
**Reason:** Prevent confusion about readiness  
**Impact:** None to existing systems  
**Follow-up:** Update Design Journal status tags

---

### 📅 2025-06-23 – Created “Action Queuing & Interrupt Logic”
**System(s):** New system added to Design Journal  
**Change:** Introduced actor-level action queues, flags, and flush policy  
**Reason:** Needed to handle squad tactics and AI chaining  
**Impact:** Requires implementation of queue metadata and flush logic  
**Follow-up:** Implement tag handling; add to test suite

---

### 📅 2025-06-23 – Added Tick Timing Reference Table
**System(s):** Combat Flow, Reference Tables  
**Change:** Imported definitive tick timing table for weapon actions  
**Reason:** Establish unified model for speed/delay resolution  
**Impact:** Will affect speed-based balance and animation logic  
**Follow-up:** Sync with item timing stats and PER modifiers

---

### 📅 2025-06-23 – Equipment Requirements Overhaul
**System(s):** Equipment Stat Requirements  
**Change:** Clarified soft stat gates vs skill bonuses; added capped stat logic  
**Reason:** Improve realism, avoid skill-based gating  
**Impact:** Stat parsing and bonus caps must be coded  
**Follow-up:** Revisit ITEM_DB to specify `stat_bonus_caps`

---

### 📅 2025-06-23 – World Structure Clarification
**System(s):** World, Zone, Room Architecture  
**Change:** Removed “room” concept; clarified that zones are cosmetic labels only  
**Reason:** Clean up spatial hierarchy  
**Impact:** Update all references to deprecated room logic  
**Follow-up:** Audit old worldgen or room functions

---

### 📅 2025-06-23 – Created Section 7: World, Terrain & Lazy Hex System
**System(s):** World Architecture  
**Change:** Defined global map system, floorplan lazy loading, and inert zones  
**Reason:** Enable memory-safe overworld traversal and discovery  
**Impact:** Requires world registry and floorplan loader  
**Follow-up:** Implement `World` object and stub generators

---

### 📅 2025-06-23 – Defined PER Stat Light Capping
**System(s):** Light Tier Visibility Model  
**Change:** Made clear that light allows visibility, PER determines usable range  
**Reason:** Separate environmental visibility from observer clarity  
**Impact:** Implement clamping logic in observe()  
**Follow-up:** Add light/PER cap unit test

---

### 📅 2025-06-23 – Consolidated Tactical Tile & Floorplan Model
**System(s):** Tactical Tile Model  
**Change:** Merged all prior discussion into single unified tactical entry  
**Reason:** Eliminate redundant tile/zone/room logic  
**Impact:** Requires parser + logic updates  
**Follow-up:** Migrate legacy tile usage into new dict model

---

📌 _Continue updating this file for each locked system modified post-lock._
