# pil_meta/utils/exceptions_reporter_utils.py
"""
Project health analysis and governance exception reporting.

Delegates validation and enrichment to dedicated modules. Coordinates:
- Governance rule execution
- Usage graph export
- Summary reporting

Governance logic lives in governance_validator.py
Usage mapping lives in usage_map_builder.py

@tags: ["exceptions", "report", "governance"]
@status: "stable"
@visibility: "public"
"""

import json
from pathlib import Path
from datetime import datetime
from collections import Counter

from pil_meta.validators.governance_validator import validate_governance_rules
from pil_meta.builders.usage_map_builder import build_usage_map


def generate_exception_report(graph: dict, output_dir: str) -> dict:
    """
    Generate governance exception and usage reports with timestamped filenames.

    @tags: ["governance", "report", "exceptions"]
    @status: "stable"
    @visibility: "public"

    Args:
        graph (dict): Entity graph keyed by fqname
        output_dir (str): Where to write JSON files

    Returns:
        dict: Summary stats for key issue types
    """
    exceptions, issue_counts = validate_governance_rules(graph)
    usage_summary = build_usage_map(graph)

    outdir = Path(output_dir)
    outdir.mkdir(parents=True, exist_ok=True)

    # Clean up old reports
    for old in outdir.glob("function_map_exceptions_*.json"):
        old.unlink()
    for old in outdir.glob("usage_map_*.json"):
        old.unlink()

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    exception_path = outdir / f"function_map_exceptions_{ts}.json"
    usage_path = outdir / f"usage_map_{ts}.json"

    with exception_path.open("w", encoding="utf-8") as f:
        json.dump(exceptions, f, indent=2)

    with usage_path.open("w", encoding="utf-8") as f:
        json.dump(usage_summary, f, indent=2)

    print(f"\n🚨 Exceptions report written → {exception_path}")
    print(f"📎 Usage map written → {usage_path}")

    return {
        "missing_docstrings": issue_counts.get("missing_docstring", 0),
        "untested": issue_counts.get("missing_test", 0),
        "orphaned": issue_counts.get("orphaned", 0),
        "missing_tags": issue_counts.get("missing_tags", 0),
        "ignored_functions_used": issue_counts.get("invalid_ignore_usage", 0)
    }
