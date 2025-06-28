# Project Docstring and Annotation Standards — User Guide

## Purpose

These standards define **how every symbol in the codebase**—functions, classes, modules, and top-level variables/lists—**should be documented**.  
They are enforced for:  
- Search and navigation  
- Vault/Obsidian export  
- Governance and quality checks  
- Automated analysis (PIL Project Intelligence Layer)

---

## Standard Format

### 1. **Docstring/Comment Structure**

- **First line:**  
  A one-sentence summary of purpose (like a Sphinx or Google-style summary).

- **Optional annotation lines:**  
  - `@tags: ["tag1", "tag2"]` — A Python list of string tags, with no spaces.
  - `@journal: "Some Journal Entry"` — For linking code to project/journal docs.
  - `@deprecated` — Flags the symbol as deprecated.
  - `@status: "draft"|"stable"|"experimental"` — Current maturity/state.
  - `@visibility: "internal"|"public"` — For vault export or documentation policy.

### 2. **Variables/Lists/Constants**

- Place the annotation comments immediately above the assignment:
    ```python
    # A list of enabled modules for startup.
    # @tags: ["config", "startup"]
    # @status: "stable"
    ENABLED_MODULES = ["core", "api"]
    ```

### 3. **Classes, Functions, Methods, Modules**

- Use Python triple-quoted docstrings inside the definition.

---

## **REQUIRED Metadata Fields**

Every code symbol exported to the vault **must** include these fields in its metadata:

| Field      | Required? | Description                                       |
|------------|-----------|---------------------------------------------------|
| fqname     | Yes       | Fully qualified name, e.g. `my_mod.foo.bar`       |
| module     | Yes       | Module or file where defined (e.g., `my_mod.utils`)|
| function/class/variable | Yes  | Local name of the symbol                    |
| type       | Yes       | One of: function, method, class, module, variable |
| ...        |           | ...                                               |

> **All exporters, validators, and vault generators must assume these keys are always present. Missing or empty fields are considered a standards violation.**

---

## Examples

**Function:**
```python
def compute_total(x, y):
    """Computes the total from x and y.
    @tags: ["math", "core"]
    @status: "stable"
    @journal: "Math Routines"
    """
    return x + y
```

**Class:**
```python
class ConnectionManager:
    """Handles connections for the service.
    @tags: ["network"]
    @status: "draft"
    @deprecated
    """
```

**Module (file):**
At the top of the file:
```python
"""
Main utility module for the API.
@tags: ["api", "utility"]
@status: "stable"
"""
```

**Variable/Constant:**
```python
# Maximum allowed items in the cart.
# @tags: ["config", "limit"]
# @journal: "E-commerce Limits"
MAX_ITEMS = 100
```

---

## Enforcement & Philosophy

- These standards are **non-negotiable**.  
- Every symbol must have a docstring or comment matching these conventions.
- **Every symbol must also provide required metadata fields** (`fqname`, `module`, local name, and `type`).  
- Pull requests, GPT output, or automated tools must check for compliance.
- When in doubt, check the latest standards file (`documents/docstring_standards_guide.md`).

## Rationale

- **Enables advanced search, filtering, and navigation** in the vault and IDE.
- **Links code to design docs/journals** for live project governance.
- **Keeps all contributors aligned**—AI, human, or automation.

---

*When in doubt, ask: Would this be discoverable, navigable, and explainable to a new team member or future GPT? If not, add tags, status, or a better summary.*
