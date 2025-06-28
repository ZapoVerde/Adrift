# 🧠 Project Intelligence Layer (PIL) — High-Level Development Plan

## 🔍 Goal
Build a fully modular, testable, config-driven metadata reasoning engine. Reuse existing function analysis logic to extract, graph, and export structured code metadata.

---

## 📍 Current Strengths (Leverage Immediately)

- ✅ AST-based function map extraction (`generate_function_map.py`)
- ✅ Tag + flag parsing (`@ignore`, `@subsystem`, `@deprecated`)
- ✅ Test coverage estimation
- ✅ Unused function detection
- ✅ Working CLI pipeline (`rebuild_function_report.py`)
- ✅ Validated output formats (JSON + Markdown)

---

## 📐 Principles for Efficient Migration

1. **Never start from scratch** — rehome and clean.
2. **Break large scripts into responsibility-aligned modules**:
   - *Loader* = I/O and extraction
   - *Builder* = transforms and graphs
   - *Exporter* = final formats
3. **Structure internal state as a graph or entity list early** — to avoid coupling to DataFrames or hard-coded structure.

---

## 🚀 Development Plan

### 🔧 Phase 1: MVP Migration and Orchestration

| Task | Outcome |
|------|---------|
| 🔁 Migrate `generate_function_map.py` → `PIL/loaders/code_loader.py` | Output = `List[Dict]` with keys: `fqname`, `doc`, `tags`, etc |
| 📊 Move `export_index()` and `export_subsystem_map()` → `PIL/exporters/` | Initial exporter format for `function_map.json` and `subsystem_map.md` |
| 🧠 Create `build_entity_graph()` → `PIL/builders/entity_graph_builder.py` | Construct `nodes`, `edges` with inferred types |
| 🔄 Replace old orchestration with `pipeline.py` | Modular, readable, testable |
| ✅ Add `tests/test_pipeline.py` smoke test | Ensure pipeline works clean |

---

### 🧠 Phase 2: Enrich and Expand the Metadata Graph

| Task | Outcome |
|------|---------|
| 🔌 Rehome test coverage logic from `test_coverage_estimator.py` | Add `coverage: str` to each node |
| 👻 Rehome unused function logic from `unused_function_detector.py` | Add `orphaned: bool` to node metadata |
| 🔗 Implement `linkage_builder.py` for edge inference | `calls`, `modifies`, `related_to`, etc |
| 🏷️ Add `tag_inference.py` to handle `tag_registry.json` compliance | Add validated tags to nodes |

---

### 📤 Phase 3: Reporting and Exporting

| Task | Outcome |
|------|---------|
| 🧾 Implement markdown and JSON exporters | Vault-ready + readable |
| 📊 Add coverage and unused reports | Markdown + JSON mirrors |
| 🧪 Validate roundtrip (load → build → export → reload) | Sanity check integrity |

---

### 📦 Phase 4: Vault and Journal Integration (Optional)

| Task | Outcome |
|------|---------|
| 📖 Add markdown_loader for design docs | Extract `headings`, `tags`, `rules`, etc |
| 🔗 Soft link code → journal using TF-IDF or anchors | `inferred_journal_link` edge in graph |
| 🧠 Enable backlinking, orphan detection, and topic clusters | Bonus value in design governance |

---

## 🛠️ Tooling

- All config and paths via `pilconfig.json`
- CLI script: `python scripts/rebuild_pil.py`
- Zip/export-friendly outputs in `exports/`

---

## ✅ Next Step

Start with **Phase 1**, migrating function map generation into PIL’s structured modules.
