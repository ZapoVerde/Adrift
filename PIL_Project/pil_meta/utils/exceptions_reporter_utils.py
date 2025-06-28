# exceptions_reporter_utils.py
"""
Project health analysis and governance exception reporting.

Delegates validation and enrichment to dedicated modules. Coordinates:
- Governance rule execution
- Usage graph export
- Summary reporting

Governance logic lives in governance_validator.py
Usage mapping lives in usage_map_builder.py
"""

import json
from pathlib import Path
from collections import Counter

from pil_meta.validators.governance_validator import validate_governance_rules
from pil_meta.builders.usage_map_builder import build_usage_map

def generate_exception_report(graph: dict, output_path: str) -> dict:
    """
    Extracts and exports metadata violations and usage mappings to a governance-style report.

    Parameters:
        graph (dict): Full entity graph keyed by fqname
        output_path (str): Path to write the exceptions report

    Returns:
        dict: Summary counts of major issue types for downstream printing
    """
    exceptions, issue_counts = validate_governance_rules(graph)
    usage_summary = build_usage_map(graph)

    # Write full JSON
    report_path = Path(output_path)
    with report_path.open("w", encoding="utf-8") as f:
        json.dump(exceptions, f, indent=2)

    # Also export usage map separately for per-type analysis
    usage_path = report_path.with_name("usage_map.json")
    with usage_path.open("w", encoding="utf-8") as f:
        json.dump(usage_summary, f, indent=2)

    print(f"\n🚨 Exceptions report written → {report_path}")
    print(f"📎 Usage map written → {usage_path}")

    # Print headline summary
    if issue_counts:
        print("\n🔎 Exception Summary:")
        for issue, count in sorted(issue_counts.items()):
            print(f"  {issue.ljust(30, '.')} {count}")
    else:
        print("\n✅ No metadata exceptions found — project is clean.")

    return {
        "missing_docstrings": issue_counts.get("missing_docstring", 0),
        "invalid_docstring_signature": issue_counts.get("invalid_docstring_signature", 0),
        "untested": issue_counts.get("missing_test", 0),
        "orphaned": issue_counts.get("orphaned", 0),
        "missing_tags": issue_counts.get("missing_tags", 0),
        "ignored_functions_used": issue_counts.get("invalid_ignore_usage", 0)
    }
