# ✅ Testing Protocol Standards – Adrift

## 🧾 Status: **Locked**

All modules in the Adrift project must follow **best practice testing**. MVP-level coverage is insufficient for core systems or utilities. All logic files must be paired with test suites that fulfill both behavioral validation and architectural guarantees.

---

## 🧪 Best Practice Coverage Requirements

### 1. Functional Behavior

* Standard input/output
* Edge conditions (e.g., zero XP, max level, empty zone)
* Conditional branches and flag modifiers (e.g., `stop_at_block`)
* Stateful outcomes over repeated calls (e.g., XP leveling)

### 2. Malformed Inputs

* Wrong types (e.g., `str` passed instead of `list`)
* Missing fields or keys (e.g., `tile["env"]` absent)
* Invalid internal data structures (e.g., mutation list is `None`)
* Null or empty edge cases (empty tags, zero actor stats)

### 3. Contract Enforcement

* All input validation paths must raise clear errors:

  * `TypeError` for type mismatches
  * `ValueError` for invalid values or missing preconditions
* Prefer failure to silent degradation

### 4. Architecture Alignment

* Tests should **mirror the declared purpose** of the function
* Modular utilities should show deterministic outputs
* Flow handlers (e.g., `run_action_phase`) should be tested via **actor state changes**, not deep mocks

---

## 🔁 Test Structure & Hygiene

### 🔹 Layered Test Design

* **Unit tests**: Test each logic function in isolation
* **Integration tests**: Validate entire flow execution (e.g., mutation triggers, XP thresholds)
* **Regression tests**: Cover edge bugs and assertion failures previously encountered

### 🔹 Imports & Module Safety

* Import functions **directly** under test (e.g., `from Adrift.utils.cover_utils import get_cover_bonus`)
* Mock only outer modules — avoid mocking internal logic
* Avoid circular imports by separating logic layers cleanly (e.g., helpers/utilities vs flow drivers)

### 🔹 Fixtures & Setup

* Use `pytest.fixture` to create standardized `Actor`, `Floorplan`, or `Tile` instances
* Prefer factory-style helpers for actors with preloaded skills or techniques
* Clean up state between tests — no cross-test bleed allowed

---

## 📎 Scope of Enforcement

This policy applies to:

* All files in `utils/`, `flow/`, `helpers/`, and reusable logic modules
* All top-level flow handlers (`run_action_phase`, `process_initiative`, etc.)
* All skill, mutation, combat, visibility, and perception systems
* Any logic invoked from `engine.py`, `action_flow.py`, or `messaging.py`

---

## ⚠️ Maintenance Practice

* All **new logic requires matching test coverage**
* Tests should be **updated** any time a function's signature or behavior changes
* Functions without tests are considered **unstable** and may not be deployed

---

## 🧠 Philosophy

* Utility functions are **pure contracts** — they must be safe, deterministic, and testable in isolation.
* Test files are not clutter — they are documentation of how the game thinks.
* We aim for **redundant validation**, not minimal scaffolding.
* **No new system is complete without exhaustive test coverage.**

---

## 🔒 Enforcement

This document is locked. All new logic must satisfy the coverage, structure, and separation requirements above. Legacy test suites will be upgraded incrementally, but new systems will **not pass review without test compliance**.
