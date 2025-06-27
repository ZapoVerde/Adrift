## 📏 Project Governance Framework

This document defines how decisions, modules, and changes are governed to minimize rework and ensure long-term maintainability of the project.

---

### 1. 🔐 Single Source of Truth (SSoT)

- The **Design Journal** is the exclusive record for finalized decisions.
- If it is not in the journal, it is not considered official.
- Changes to locked designs must:
  - Provide justification
  - Replace or deprecate the old design
  - Document consequences or required migrations

---

### 2. 🧩 Module Ownership

Each module has strictly defined responsibilities:

| Module            | Responsibility                                       |
| ----------------- | ---------------------------------------------------- |
| `engine.py`       | Game loop flow control – no logic or state mutations |
| `combat_utils.py` | All combat calculations and mechanics                |
| `floorplan.py`    | Map layout and zone linkage                          |
| `player_utils.py` | Player-specific actions and vision logic             |
| `messaging.py`    | All user-facing output, no logic                     |
| `config.py`       | Global toggles and shared constants                  |
| `debug_utils.py`  | Debug-only output routing                            |
| `test_*.py`       | Unit and edge case tests for all logic modules       |

---

### 3. 📑 Design Lock Protocol

Designs move through the following stages:

| Stage      | Criteria                                                 | Action Required                                   |
| ---------- | -------------------------------------------------------- | ------------------------------------------------- |
| Draft      | Experimental or under discussion                         | Prototypes allowed, not journal-bound             |
| Locked     | MVP-compliant, tested, accepted by review                | Must be added to Design Journal                   |
| Deprecated | Replaced, superseded, or incompatible with newer systems | Crossed out with replacement rationale in journal |

---

### 4. 📋 Decision Record Template

```md
### 🧠 Decision: [System Name]

**Status:** Locked  
**Summary:**  
- Purpose and scope  
- Rationale for chosen approach  
- Alternatives rejected  

**Architecture Impact:**  
- File/module ownership  
- Consumers and dependencies  

**Testing Requirements:**  
- [ ] Core logic  
- [ ] Edge case  
- [ ] Integration/flow linkage  
```

---

### 5. 📊 Changelog Discipline

All structural, gameplay, or architectural changes must include:

- Date of change
- What was changed or removed
- Why the change occurred
- Any backward compatibility impacts

---

### 6. 🔬 Testing-First Enforcement

Every implemented system must:

- Have a dedicated test file
- Cover both standard and edge cases
- Show integration or flow usage (if applicable)

> Tests must run independently via CLI or test harness.

---

### 7. 🧼 Legacy Detection

Flag and isolate the following as legacy:

- Raw `print()` or embedded strings in logic
- Logic in `engine.py`
- Functions with dual responsibilities
- Outdated methods no longer aligned with journal

Actions:

- Mark with `# LEGACY [date]`
- Quarantine in `_legacy/` folder or refactor immediately

---

### 8. 🔄 MVP Sprint Workflow (Optional)

| Phase     | Objective                                                  |
| --------- | ---------------------------------------------------------- |
| Planning  | Identify 3–5 MVP goals or mechanics to focus on            |
| Execution | Build, refactor, and test targeted systems                 |
| Lock-in   | Integrate finalized designs into the Design Journal        |
| Audit     | Compare implementation vs journal for drift and violations |

---

This framework is mandatory. Any deviation should be explicitly approved and journaled as an exception.

