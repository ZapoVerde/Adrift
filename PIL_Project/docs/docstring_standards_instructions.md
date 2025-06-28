# Docstring and Annotation Standards — Quick Instructions

**MANDATORY:**  
All code symbols (functions, classes, modules, variables/lists/constants) **must** follow these standards:

- Every symbol must have a structured docstring or comment block in the correct format.
- The **first line** is a one-sentence summary (description).
- Docstring/comments can include annotation lines using these keywords:
    - `@tags: ["tag1", "tag2"]`  *(Python list of strings; no spaces in tags)*
    - `@journal: "Journal Entry Title"`  *(quoted string; for documentation cross-linking)*
    - `@deprecated`  *(no argument; marks symbol as deprecated)*
    - `@status: "draft"` *(or "stable", "experimental", etc.; quoted string)*
    - `@visibility: "internal"` *(or "public"; quoted string)*
- **Variable/lists/constants**: Place comments immediately above the assignment.

---

**REQUIRED METADATA FIELDS (for every symbol):**
- `fqname`: Fully qualified name (e.g., `my_mod.foo.bar`)
- `module`: Module or file name (e.g., `my_mod.utils`)
- `function`/`class`/`variable`: Local symbol name
- `type`: One of: function, method, class, module, variable

> **Any missing or empty metadata fields are a standards violation.**

---

**Example (function):**
```python
def foo():
    """Short summary of what foo does.
    @tags: ["core", "math"]
    @status: "stable"
    """
    ...
```

**Example (variable):**
```python
# Number of retries for the connection.
# @tags: ["network", "config"]
# @status: "draft"
MAX_RETRIES = 3
```

---

**No code or documentation will be accepted unless these rules are followed.**
