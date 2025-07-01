# pil_meta/utils/messaging_utils.py
"""
Centralized messaging utility for PIL with structured reporting format.
Supports clean, grouped output with headers, emojis, and indentation.

@tags: ["utility", "messaging", "reporting"]
@status: "stable"
@visibility: "public"
"""

import sys

DEBUG_ENABLED = False

def set_debug(enabled: bool) -> None:
    """Enable or disable debug messages globally."""
    global DEBUG_ENABLED
    DEBUG_ENABLED = enabled

def debug(msg: str, indent: int = 0) -> None:
    """Print debug messages if debug enabled."""
    if DEBUG_ENABLED:
        prefix = "    " * indent
        print(f"{prefix}[DEBUG] {msg}", file=sys.stdout)

def _print_section_header(title: str, icon: str = "──────────────────────────────") -> None:
    print(f"\n{icon}\n{title}\n{icon}")

def info(msg: str, indent: int = 0) -> None:
    """Print informational message with optional indentation."""
    prefix = "    " * indent
    print(f"{prefix}[INFO] {msg}", file=sys.stdout)

def warning(msg: str, indent: int = 0) -> None:
    """Print warning message with optional indentation."""
    prefix = "    " * indent
    print(f"{prefix}[WARNING] {msg}", file=sys.stderr)

def error(msg: str, indent: int = 0) -> None:
    """Print error message with optional indentation."""
    prefix = "    " * indent
    print(f"{prefix}[ERROR] {msg}", file=sys.stderr)

def print_run_context(script: str, config: str, date: str) -> None:
    _print_section_header("🧠 PIL Pipeline: RUN & SCAN", "───────────── PIL Pipeline: RUN & SCAN ─────────────")
    info(f"Script: {script}", indent=1)
    info(f"Config: {config}", indent=1)
    info(f"Date: {date}", indent=1)

def print_folder_tree_summary(tree_lines: list[str]) -> None:
    _print_section_header("📁 Folder Structure (Python Source)", "──────────────────────────────")
    for line in tree_lines:
        print(line)

def print_asset_scan_summary(supported: list[str], found_count: int) -> None:
    _print_section_header("🗂️ Asset Scan", "──────────────────────────────")
    info(f"Supported types: {', '.join(supported)}", indent=1)
    info(f"Asset files found: {found_count}", indent=1)

def print_symbol_extraction(code_symbols: int, asset_files: int, root: str) -> None:
    _print_section_header("🔬 Symbol Extraction", "──────────────────────────────")
    info(f"Code symbols: {code_symbols}", indent=1)
    info(f"Asset files: {asset_files}", indent=1)
    info(f"Project root: {root}", indent=1)

def print_entity_graph(nodes: int, linkages_injected: bool) -> None:
    _print_section_header("📊 Entity Graph", "──────────────────────────────")
    info(f"Total nodes: {nodes}", indent=1)
    info(f"Linkages injected: {'Yes' if linkages_injected else 'No'}", indent=1)

def print_exports(export_paths: dict, vault_files_count: int, index_path: str) -> None:
    _print_section_header("📤 Exports Written", "──────────────────────────────")
    info(f"Entity graph:        {export_paths.get('timestamped', 'N/A')}", indent=1)
    usage_map_path = export_paths.get('timestamped')
    info(f"Usage map:           {usage_map_path if usage_map_path else 'N/A'}", indent=1)
    info(f"Vault files:         {vault_files_count} Markdown files", indent=1)
    info(f"Vault index:         {index_path}", indent=1)

def print_governance_summary(missing_docstrings: int, orphaned: int) -> None:
    if missing_docstrings > 0 or orphaned > 0:
        warning("Governance issues detected:")
        if missing_docstrings > 0:
            warning(f" - Missing docstrings: {missing_docstrings}")
        if orphaned > 0:
            warning(f" - Orphaned entities: {orphaned}")
        warning("Please ask the assistant to review governance exceptions if needed.")
    else:
        info("✅ No governance exceptions detected. Metadata quality is good.")

def print_journal_entries_loaded(count: int) -> None:
    _print_section_header("📓 Journal/Design Documentation", "──────────────────────────────")
    info(f"Journal entries loaded: {count}", indent=1)

def print_pipeline_complete(snapshot_count: int, snapshot_path: str) -> None:
    _print_section_header("✅ Pipeline complete", "──────────────────────────────")
    info(f"Snapshot: {snapshot_count} files → {snapshot_path}", indent=1)
