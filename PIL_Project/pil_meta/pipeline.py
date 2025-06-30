# pil_meta/pipeline.py
"""
Main orchestration pipeline for the PIL meta-engine.
Handles config loading, symbol extraction, entity graph building, linkage injection,
tag/link application, export, and governance reporting.
"""

import sys
import traceback
from pathlib import Path

from pil_meta.loaders.config_loader import load_config
from pil_meta.loaders.asset_loader import load_asset_symbols
from pil_meta.loaders.code_loader import load_code_symbols
from pil_meta.loaders.markdown_loader import load_markdown_entries

from pil_meta.builders.entity_graph_builder import build_entity_graph
from pil_meta.builders.linkage_builder import inject_call_links
from pil_meta.builders.usage_map_builder import build_usage_map

from pil_meta.exporters.json_exporter import export_entity_graph
from pil_meta.exporters.usage_map_exporter import export_usage_map
from pil_meta.exporters.markdown_vault_exporter import export_markdown_vault
from pil_meta.exporters.md_exporter import export_entity_markdown
from pil_meta.exporters.vault_index_exporter import export_vault_index
from pil_meta.exporters.variable_usage_report_exporter import export_variable_usage_markdown
from pil_meta.utils.exceptions_reporter_utils import generate_exception_report
from pil_meta.utils.snapshot_utils import take_project_snapshot


def run_pipeline(config_path="pilconfig.json"):
    """
    Main entry point for running the PIL meta pipeline.
    Loads config, runs all stages, and writes outputs using bulletproof absolute pathing.
    """
    try:
        # 1. Load config and resolve all paths as absolute
        config = load_config(config_path)
        print("[PIL] Loaded config with resolved paths:")
        for key in [
                "project_root", "journal_path", "output_dir", "docs_dir",
                "vault_dir", "snapshot_dir"
        ]:
            print(f"  {key}: {config.get(key)}")

        # 2. Load asset symbols from all tracked asset directories
        asset_symbols = load_asset_symbols(config)
        print(f"✅ Found {len(asset_symbols)} asset files.")

        # 3. Load and parse all Python source files in project_root
        code_symbols = []
        project_root = config["project_root"]
        for pyfile in Path(project_root).rglob("*.py"):
            code_symbols.extend(load_code_symbols(str(pyfile), project_root))
        print(f"✅ Found {len(code_symbols)} code symbols.")

        # 4. Build the base entity graph (merge code and assets)
        entities = code_symbols + asset_symbols
        entity_graph = build_entity_graph(entities)
        print("✅ Built entity graph.")

        # 5. Inject call linkages into the graph
        entity_graph = inject_call_links(entity_graph, project_root)
        print("✅ Injected call linkages.")

        # 7. Export entity graph JSON
        export_entity_graph(entity_graph, config["output_dir"])
        print(f"✅ Exported entity graph to {config['output_dir']}")
        graph_path = str(Path(config["output_dir"]) / "entity_graph.json")

        # 8. Build and export the usage map as JSON
        usage_map = build_usage_map(entity_graph)
        export_usage_map(usage_map, config["output_dir"])
        print(f"✅ Exported usage map to {config['output_dir']}/usage_map.json")

        # 9. Export Markdown vault, index, and variable usage report
        export_markdown_vault(entity_graph, config["vault_dir"])
        export_vault_index(entity_graph, config["vault_dir"])
        export_variable_usage_markdown(
            usage_map, str(Path(config["output_dir"]) / "variable_usage.md"))
        print(
            f"✅ Exported Markdown vault and variable usage report to {config['vault_dir']} and {config['output_dir']}"
        )

        # 10. (Optional) Export individual markdown files for code entities
        # for node in entity_graph.values():
        #     export_entity_markdown(node, config["output_dir"])

        # 11. Governance reporting / exceptions
        exceptions_path = str(
            Path(config["output_dir"]) / "function_map_exceptions.json")
        generate_exception_report(entity_graph, exceptions_path)
        print(f"✅ Exceptions report written → {exceptions_path}")

        # 12. (Optional) Load and index Markdown docs/journals
        journal_entries = load_markdown_entries(config["journal_path"])
        print(f"✅ Loaded {len(journal_entries)} markdown journal entries.")

        print("\n📊 Project health snapshot:")
        missing_docstrings = sum(1 for n in entity_graph.values()
                                 if not n.get("docstring_present"))
        orphaned = sum(1 for n in entity_graph.values()
                       if n.get("is_orphaned"))
        print(f"   ├─ {missing_docstrings} missing docstrings")
        print(f"   └─ {orphaned} orphaned (unlinked) entities")
        print("\n✅ Metadata pipeline complete.")

        # 13. Optional snapshot step (graceful handling)
        try:
            snapshot_path = take_project_snapshot(config,
                                                  entity_graph_path=graph_path)
            print(f"📦 Project snapshot saved to {snapshot_path}")
        except Exception as e:
            print(f"🟡 Snapshot skipped: {e}")

    except Exception:
        print("\n❌ Pipeline failed. Full traceback below:")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    run_pipeline()
