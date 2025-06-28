# pipeline.py
"""
Pipeline: Main Entry

Coordinates full metadata graph construction and export from source code.
This module is the top-level orchestrator for the Project Intelligence Layer (PIL),
responsible for running a complete metadata pass using configuration in pilconfig.json.

Steps:
- Load config
- Extract raw function symbols
- Normalize fields for graph compatibility
- Build and enrich entity graph
- Export graph to disk
- Emit governance exception report
"""

import shutil
from pathlib import Path

from pil_meta.loaders.config_loader import load_config
from pil_meta.loaders.code_loader import load_code_symbols
from pil_meta.builders.entity_graph_builder import build_entity_graph
from pil_meta.builders.linkage_builder import inject_call_links
from pil_meta.exporters.json_exporter import export_entity_graph
from pil_meta.utils.exceptions_reporter_utils import generate_exception_report

def run_pipeline() -> None:
    """
    Execute full metadata extraction and export pipeline.

    This is the entry point called by `scripts/rebuild_pil.py`. It uses
    paths from `pilconfig.json`, loads all top-level Python symbols,
    builds the graph, computes call linkages, and writes outputs.
    """
    # 🔧 Load configuration
    config_path = Path(__file__).resolve().parents[1] / "pilconfig.json"
    config = load_config(str(config_path))  # ensure path is passed as string

    # 🧹 Clear previous exports
    export_path = Path(config["output_dir"])
    if export_path.exists():
        shutil.rmtree(export_path)
    export_path.mkdir(parents=True, exist_ok=True)

    # 📥 Load code-level symbols from source tree
    print("\n📥 Loading code symbols...")
    raw_symbols = load_code_symbols(str(config_path))
    print(f"✅ Found {len(raw_symbols)} function symbols.")

    # 🧾 Normalize for graph compatibility
    for symbol in raw_symbols:
        symbol["docstring_present"] = bool(symbol["description"])
        symbol["test_coverage"] = False  # placeholder, to be overwritten later
        symbol["linked_journal_entry"] = None
        symbol["is_orphaned"] = True
        symbol["links"] = []
        symbol["called_by_fqns"] = []  # required by linkage builder
        symbol["calls_fqns"] = []      # required by linkage builder
        symbol["ignore"] = symbol.get("ignore", False)
        symbol["deprecated"] = symbol.get("deprecated", False)

    # 🧠 Build core entity graph
    print("\n🧠 Building entity graph...")
    graph = build_entity_graph(raw_symbols)

    # 🔗 Compute function-to-function call links
    print("\n🔗 Injecting call linkages...")
    graph = inject_call_links(graph, config["project_root"])

    # 📤 Save enriched graph to disk
    print("\n📤 Exporting entity graph...")
    export_entity_graph(graph, config["output_dir"])

    # 📋 Emit governance report to track missing docs/tests/etc.
    report_path = str(Path(config["output_dir"]) / "function_map_exceptions.json")
    summary = generate_exception_report(graph, report_path)

    # 🧾 Print quick governance summary
    print("\n📊 Project health snapshot:")
    print(f"   ├─ {summary['missing_docstrings']} missing docstrings")
    print(f"   ├─ {summary['untested']} untested functions")
    print(f"   └─ {summary['orphaned']} orphaned (unlinked) entities")

    print("\n✅ Metadata pipeline complete.")
