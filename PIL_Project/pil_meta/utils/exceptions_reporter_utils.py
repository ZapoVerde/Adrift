# exceptions_reporter_utils.py
"""
Project health analysis and governance exception reporting.

Analyzes the final entity graph to identify undocumented, untested, and orphaned functions.
Also validates docstring structure and tracks usage of deprecated or ignored functions.

This file also exposes docstring validation logic for reuse during graph construction.
"""

import json
from pathlib import Path
from collections import Counter

def check_docstring_signature_match(node: dict) -> bool:
    """
    Checks if the function docstring references the function name and its parameters.

    This is used both during entity graph construction (to enrich metadata)
    and during governance report generation (to flag issues).

    Parameters:
        node (dict): Metadata dictionary for a function or method.

    Returns:
        bool: True if name and all params appear in the first line of the docstring
    """
    doc = node.get("description", "").lower()
    name = node.get("function", "").lower()
    params = node.get("metadata", {}).get("args", [])

    if not doc or not name:
        return False

    return name in doc and all(p.lower() in doc for p in params)

def generate_exception_report(graph: dict, output_path: str) -> dict:
    """
    Extracts and exports metadata violations to a governance-style report.
    Also enriches nodes with `docstring_valid`.

    Parameters:
        graph (dict): Full entity graph keyed by fqname
        output_path (str): Path to write the exceptions report

    Returns:
        dict: Summary counts of major issue types for downstream printing
    """
    exceptions = {}
    issue_counts = Counter()

    for fqn, node in graph.items():
        issues = []

        # Enrich node
        docstring_valid = check_docstring_signature_match(node)
        node["docstring_valid"] = docstring_valid

        # Governance rules
        if not node.get("docstring_present"):
            issues.append("missing_docstring")
        elif not docstring_valid:
            issues.append("invalid_docstring_signature")

        if not node.get("test_coverage"):
            issues.append("missing_test")
        if not node.get("tags"):
            issues.append("missing_tags")
        if node.get("is_orphaned"):
            issues.append("orphaned")
        if node.get("deprecated") and node.get("called_by_fqns"):
            issues.append("deprecated_but_used")
        if node.get("ignore") and node.get("called_by_fqns"):
            issues.append("invalid_ignore_usage")

        if issues:
            for issue in issues:
                issue_counts[issue] += 1

            exceptions[fqn] = {
                "module": node.get("module"),
                "function": node.get("function"),
                "issues": issues,
                "calls": node.get("calls_fqns", []),
                "called_by": node.get("called_by_fqns", [])
            }

    # Write full JSON
    report_path = Path(output_path)
    with report_path.open("w", encoding="utf-8") as f:
        json.dump(exceptions, f, indent=2)

    print(f"\n🚨 Exceptions report written → {report_path}")

    # Print headline summary
    if issue_counts:
        print("\n🔎 Exception Summary:")
        for issue, count in sorted(issue_counts.items()):
            print(f"  {issue.ljust(30, '.')} {count}")
    else:
        print("\n✅ No metadata exceptions found — project is clean.")

    return {
        "missing_docstrings": issue_counts.get("missing_docstring", 0),
        "untested": issue_counts.get("missing_test", 0),
        "orphaned": issue_counts.get("orphaned", 0)
    }
