# pil_meta/pipeline.py
"""
Main orchestration pipeline for the PIL meta-engine.
Handles config loading, symbol extraction, entity graph building, linkage injection,
tag/link application, export, and governance reporting.
"""

import sys
import traceback
from pathlib import Path
from datetime import datetime

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
from pil_meta.utils.export_cleanup_utils import clean_exports_dir

def run_pipeline(config_path="pilconfig.json"):
    try:
        config = load_config(config_path)
        project_root = Path(config["project_root"]).resolve()
        project_name = project_root.name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        asset_symbols = load_asset_symbols(config)
        code_symbols = []
        for pyfile in project_root.rglob("*.py"):
            code_symbols.extend(load_code_symbols(str(pyfile), str(project_root)))

        print("\n🔍 Scanning summary:")
        print(f"   ├─ Code symbols: {len(code_symbols)}")
        print(f"   ├─ Asset files: {len(asset_symbols)}")
        print(f"   └─ Project root: {project_root}")

        entities = code_symbols + asset_symbols
        entity_graph = build_entity_graph(entities)
        entity_graph = inject_call_links(entity_graph, str(project_root))

        print("\n🧠 Graph construction:")
        print(f"   ├─ Total nodes: {len(entity_graph)}")
        print("   └─ Linkages injected")

        clean_exports_dir(config["output_dir"])

        graph_paths = export_entity_graph(entity_graph, config["output_dir"], project_name, timestamp)
        usage_paths = export_usage_map(build_usage_map(entity_graph), config["output_dir"], project_name, timestamp)
        vault_files = export_markdown_vault(entity_graph, config["vault_dir"], project_name, timestamp)
        index_path = export_vault_index(entity_graph, config["vault_dir"], project_name, timestamp)
        variable_report_path = export_variable_usage_markdown(
            build_usage_map(entity_graph),
            str(Path(config["output_dir"]) / "variable_usage.md"),
            project_name,
            timestamp
        )

        print("\n📤 Exports written:")
        print(f"   ├─ Entity graph → {graph_paths['stable']} ({Path(graph_paths['timestamped']).name})")
        print(f"   ├─ Usage map → {usage_paths['stable']} ({Path(usage_paths['timestamped']).name})")
        print(f"   ├─ Vault files → {len(vault_files)} Markdown files")
        print(f"   ├─ Vault index → {index_path}")
        print(f"   └─ Variable usage → {variable_report_path}")

        try:
            generate_exception_report(entity_graph, config["output_dir"])
        except Exception as e:
            print(f"❌ Failed to generate exceptions report: {e}")

        print("\n📎 Governance:")
        print(f"   ├─ Exceptions (latest) → {Path(config['output_dir']) / 'function_map_exceptions.json'}")
        print(f"   ├─ Exceptions (timestamped) → {sorted(Path(config['output_dir']).glob('function_map_exceptions_*.json'))[-1]}")
        print(f"   └─ Usage map (timestamped) → {usage_paths['timestamped']}")

        journal_entries = load_markdown_entries(config["journal_path"])
        print(f"\n📓 Journal entries loaded: {len(journal_entries)}")

        missing_docstrings = sum(1 for n in entity_graph.values() if not n.get("docstring_present"))
        orphaned = sum(1 for n in entity_graph.values() if n.get("is_orphaned"))

        print("\n📊 Project health:")
        print(f"   ├─ Missing docstrings: {missing_docstrings}")
        print(f"   └─ Orphaned entities: {orphaned}")

        print("\n✅ Metadata pipeline complete.")

        snapshot_path = take_project_snapshot(
            config,
            entity_graph_path=graph_paths["stable"]
        )
        from zipfile import ZipFile
        with ZipFile(snapshot_path, 'r') as zipf:
            file_count = len(zipf.infolist())
        print(f"📦 Created snapshot with {file_count} files → {snapshot_path}")

    except Exception:
        print("\n❌ Pipeline failed. Full traceback below:")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    run_pipeline()
