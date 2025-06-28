# variable_usage_report_exporter.py
"""
Variable Usage Markdown Exporter (exporters)

Exports a summary report of variables/lists/constants used in more than one module,
for vault, governance, or architectural review.
"""

from pathlib import Path

def export_variable_usage_markdown(usage_map: dict, output_path: str):
    """
    Writes a Markdown summary listing each variable used in multiple modules.

    Parameters:
        usage_map (dict): fqname -> list of modules where variable is used
        output_path (str): Path to output .md file
    """
    out = []
    out.append("# 🧩 Cross-File Variable Usage Report\n")
    out.append("Lists all variables (top-level assignments) referenced in more than one module.\n")

    if not usage_map:
        out.append("_No cross-file variable usage detected._")
    else:
        for fqname, modules in sorted(usage_map.items()):
            out.append(f"## `{fqname}`")
            out.append(f"**Used in {len(modules)} files:**")
            for mod in modules:
                out.append(f"- `{mod}`")
            out.append("")  # blank line

    Path(output_path).write_text("\n".join(out), encoding="utf-8")
    print(f"✅ Exported variable usage report → {output_path}")
