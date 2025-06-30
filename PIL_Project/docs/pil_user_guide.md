# 🧠 PIL User Guide — Project Intelligence Layer

This guide explains what the **Project Intelligence Layer (PIL)** is, why it exists, and how to use it effectively as a developer, team member, or AI assistant.

---

## 📖 Introduction to PIL

### What Is PIL?

PIL is a code intelligence framework that builds and maintains a live metadata graph of all meaningful elements in your codebase: functions, classes, modules, variables, and assets. It supports governance, clarity, and assistant reasoning by extracting, validating, and exporting standardized metadata for every tracked symbol.

PIL is designed to:

* Eliminate redundant or abandoned code.
* Prevent misunderstandings about function roles or signatures.
* Maintain architectural clarity through metadata.
* Provide a persistent, factual map for AI to use during code reasoning.

### What Is the Entity Graph?

The **entity graph** is the central output of PIL — a JSON-based structure representing every tracked symbol and its metadata. It includes relationships (like function calls), annotations (e.g., `@tags`, `@status`), and linkage between code elements.

The graph is not a complete mirror of the code but rather a **structural intelligence layer**. It enables reliable decision-making, cross-referencing, and documentation generation.

> 📌 An **entity** is anything PIL tracks: a function, class, module, or asset. Each entity has a unique `fqname` and metadata such as description, tags, and links.

---

## 🚀 How to Use PIL (Developer Checklist)

### 🗅 First-Time Setup

Before starting:

* Place the entire PIL folder (e.g. `PIL_Project/`) as a **sibling to your project root**.

  * For example, if your project is `Adrift/`, then structure it as:

    ```
    AdriftProject/
    ├── Adrift/               ← your actual codebase
    ├── PIL_Project/          ← this contains pil_meta and scripts
    ├── run_pil.py            ← placed in project root
    └── pilconfig.json        ← placed in project root
    ```

1. Copy `run_pil.py` and `pilconfig.json` to your project root.
2. Edit `pilconfig.json` to set:

   * `project_root`, `output_dir`, `snapshot_dir`, etc.
3. Feed the AI assistant a copy of the **Docstring and Annotation Standards — Quick Instructions** and the **Assistant Behavior Profile: Structured Metadata Architect** documents.

   * These documents are included in the `PIL_Project/documents/` folder.

### 🔁 Normal Workflow

Once PIL is set up:

* Run `run_pil.py` for the first time and feed the resulting `entity_graph.json` back to the AI assistant.
* Run `run_pil.py` after each meaningful code change or refactor.
* Upload the latest `entity_graph.json` to the AI assistant at the start of each working session.
* If `scripts/snapshot_project.py` is present, a snapshot of the full project as well as a copy of the latest entity graph will be created automatically after each pipeline run.

### 🧠 Feeding the Entity Graph to the AI Assistant

The AI assistant uses the entity graph to maintain reasoning integrity, detect duplication, and preserve architectural intent.

* After each run of `run_pil.py`, provide the resulting `exports/entity_graph.json` to the assistant.
* If the graph is outdated or missing, the assistant may:

  * Propose redundant helpers
  * Misinterpret function purpose or parameters
  * Violate naming or logic conventions

> 📌 **Best practice**: Always upload the latest graph at the beginning of each working session, and after any major change.

### ⚠️ Common Mistakes

* Missing or malformed `pilconfig.json`
* Symbols without docstrings (causes metadata gaps)
* Not re-running after refactors (results get stale)

---

## 🧠 AI Assistant Behavior Under PIL

When PIL is active, the AI assistant is no longer a generic assistant — it becomes a **code generation and reasoning agent**, constrained and informed by the project’s entity graph and governance standards. This means:

* **The user provides directives**: architectural goals, features to implement, documentation standards, project intent.
* **The AI assistant performs the implementation**: respecting all existing code, symbol names, structure, and documented logic.
* **The AI assistant does not invent helpers or symbols** unless it has:

  1. Exhausted all known graph options,
  2. Flagged the issue to the user explicitly, and
  3. Documented the new code fully per the provided standards.
* **The AI assistant must surface violations**: missing docstrings, naming mismatches, duplicated logic, or anything that breaks the rules.

### 📌 Clarifying the Burden of Compliance

The user is not the coder — the user is the project owner, architect, and design authority. PIL is the framework that delegates execution responsibility to the AI assistant.

That includes:

* Enforcing docstrings, metadata, and tagging.
* Using existing helpers before introducing new ones.
* Refusing to work outside the entity graph without calling it out.

### 🔧 Workflow Relationship

* The user defines goals, architecture, and system intent.
* The AI assistant carries out the implementation using the verified entity graph.
* Documentation, metadata, and standard enforcement are the responsibility of the AI assistant.
* The user is responsible for transferring the AI assistant's output into the actual coding environment.

### 📌 Operational Rules

(See Appendix: Verification Behavior for full detail.). All logic must be verified using the entity graph.

* ✅ The graph is the **source of truth** for symbol names, parameters, return types, and intent.
* ✅ The assistant must **enforce the docstring standards** in all code it generates or edits.
* ✅ All new symbols must include meaningful `@tags` and an appropriate `@status`.
* ✅ The assistant must proactively warn the user if:

  * A function is orphaned (no inbound or outbound links)
  * A helper duplicates an existing symbol
  * A symbol lacks mandatory metadata or has malformed annotations
* ✅ All generated code must favor reuse. New helpers or APIs must only be introduced after checking the graph.

> 🔐 **Important**: The AI assistant's behavior assumes the presence of docstring standards and a current `entity_graph.json`. If these are missing, reasoning may be impaired.

---

## 📦 Snapshotting (Optional)

PIL can create ZIP snapshots of the entire project — including the entity graph — to preserve development state for future comparison or rollback.

* Snapshots (which include the entity graph) are saved to the folder defined in `snapshot_dir` in `pilconfig.json`.
* Snapshotting is triggered automatically at the end of the pipeline run, if `scripts/snapshot_project.py` is present.
* If the script is missing or errors, PIL continues without failure.
* Snapshots are named using timestamps for traceability.

> Snapshots are useful for recovering from faulty merges, tracing metadata drift, or debugging historical issues.

---

## 🗖 Integration Outputs

* `entity_graph.json`: Full list of symbols with docstrings, tags, links
* `exports/vault/`: Markdown pages per symbol, structured for Obsidian
* `usage_map.json`: Reference map of symbol usage
* `function_map_exceptions.json`: Missing metadata, violations, orphans
* `variable_usage.md`: Symbol-level variable introspection report
* `snapshots/`: Timestamped ZIP archives of the full project directory (if snapshotting is enabled)

---

## 📚 Appendix: Sample `pilconfig.json`

Here is a basic working example of `pilconfig.json`, assuming your project is named `Adrift` and your PIL folder is `PIL_Project`:

```json
{
  "project_root": "./Adrift",
  "output_dir": "./exports",
  "docs_dir": "./documents",
  "snapshot_dir": "./snapshots",
  "vault_dir": "./exports/vault",
  "config_self_path": "./pilconfig.json",
  "pil_module_path": "./PIL_Project",
  "asset_extensions": [".png", ".json", ".tmx", ".glb", ".shader", ".svg", ".csv"]
}
```

You can customize paths as needed, but make sure:

* All paths are relative to the project root or absolute.
* `asset_extensions` lists the file types PIL should track.
* `config_self_path` always points to the location of this config file.

---

## 🔍 Appendix: Verification Behavior

The AI assistant’s reasoning is grounded in the current `entity_graph.json`, which acts as a navigational and structural guide.

### When the graph is available:

* The assistant cross-checks all symbol names, parameter lists, and module structure.
* The assistant warns the user if it detects missing docstrings, malformed metadata, or duplicate logic.
* No assumptions are made — only verified facts are used.

### When the graph is missing or outdated:

* The assistant may fall back on generic knowledge, which increases the risk of error.
* PIL behavior is no longer guaranteed.

> 📌 This is why regular feeding of the graph is essential for accurate implementation.

---

## 📌 Final Notes

PIL is a system of memory, traceability, and code clarity. Its outputs are designed to:

* Let AI assistants write more accurate, non-redundant code.
* Help human developers understand project architecture faster.
* Keep project intelligence self-validating and discoverable.

When used correctly, PIL prevents the slow buildup of tech debt caused by forgotten helpers, repeated patterns, and confused assistant suggestions.

It is not optional. It is the backbone of project reasoning.
