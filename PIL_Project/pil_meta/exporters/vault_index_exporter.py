# vault_index_exporter.py
"""
Vault Index Exporter (exporters)

Generates an Obsidian-friendly index.md for your code vault,
grouped by type, with live Dataview sections and usage links.
"""

from collections import defaultdict
from pathlib import Path

def export_vault_index(graph: dict, output_dir: str):
    """
    Writes an index.md in output_dir listing all code entities grouped by type,
    with Obsidian links and Dataview live dashboards.
    """
    index = []
    index.append("# 🧭 Project Code Vault Index\n")
    index.append("This file is auto-generated. Use it as your starting dashboard in Obsidian.\n")
    index.append("---\n")

    by_type = defaultdict(list)
    for node in graph.values():
        by_type[node["type"]].append(node["fqname"])

    for group in ["module", "class", "function", "method", "variable"]:
        items = sorted(set(by_type.get(group, [])))
        if not items:
            continue
        icon = {
            "module": "📦",
            "class": "🏛️",
            "function": "⚙️",
            "method": "🔹",
            "variable": "🧩"
        }.get(group, "")
        index.append(f"## {icon} {group.title()}s")
        for fqn in items:
            index.append(f"- [[{fqn}]]")
        index.append("")

    # Optional: Add a Dataview dashboard for status/tags
    index.append("---\n")
    index.append("## 📊 Live Dataview: All Non-Stable Code")
    index.append("```dataview\n"
                 "table type, status, tags\n"
                 f'from "{output_dir}"\n'
                 "where status != \"stable\"\n"
                 "sort type asc\n"
                 "```")

    # Write the index file
    index_path = Path(output_dir) / "index.md"
    index_path.write_text("\n".join(index), encoding="utf-8")
    print(f"✅ Exported vault index to {index_path}")
