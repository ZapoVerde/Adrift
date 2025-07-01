# pil_meta/exporters/markdown_vault_exporter.py

import os
from pathlib import Path
from typing import Union, Optional

def friendly_name(node):
    """Returns a human-friendly display name for vault navigation."""
    def get_field(n, k):
        return n.get(k) or n.get("metadata", {}).get(k) or "unknown"

    module_name = get_field(node, "module")
    module_part = module_name.split(".")[-1] if module_name != "unknown" else "unknown"
    name = get_field(node, "name")
    function = get_field(node, "function")

    if node["type"] == "function":
        return f'{name or function or "?"} (in {module_part})'
    if node["type"] == "method":
        parts = node["fqname"].split(".")
        class_part = parts[-2] if len(parts) >= 3 else "unknown"
        return f'{name or function or "?"} ({class_part} in {module_part})'
    if node["type"] == "class":
        return f'{name or function or "?"} (in {module_part})'
    if node["type"] == "variable":
        return f'{name or function or "?"} (in {module_part})'
    if node["type"] == "module":
        return module_part or node["fqname"]
    return node["fqname"]

def _sanitize_filename(name: str) -> str:
    """Sanitizes a string for use as a safe Markdown filename."""
    return (
        name.replace("/", "_")
            .replace("\\", "_")
            .replace(":", "-")
            .replace("?", "")
            .replace("*", "")
            .replace("|", "-")
            .replace('"', "")
            .replace("'", "")
            .replace("<", "")
            .replace(">", "")
    )

def export_markdown_vault(
    graph: dict,
    output_dir: Union[str, Path],
    project_name: str = "project",
    timestamp: Optional[str] = None
) -> list[str]:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    written_files = []

    for fqname, node in graph.items():
        friendly = friendly_name(node)
        subdir = node.get("type", "misc") + "s"
        node_dir = output_path / subdir
        node_dir.mkdir(parents=True, exist_ok=True)
        file_path = node_dir / (_sanitize_filename(friendly) + ".md")

        tags = " ".join(f"#{t.replace(' ', '_')}" for t in node.get("tags", []))
        links_md = ""
        if node.get("links"):
            for link in node["links"]:
                links_md += f"- **{link.get('type', 'link')}**: {link.get('target')}\n"
        if node.get("linked_journal_entry"):
            links_md += f"- **journal**: {node['linked_journal_entry']}\n"

        md = f"""# {friendly}
> **Fully qualified name:** `{node['fqname']}`

**Type:** {node.get('type', '')}
**Module:** {node.get('module', '')}
**Status:** {node.get('status', '') or 'n/a'}
**Visibility:** {node.get('visibility', '') or 'n/a'}
**Tags:** {tags}
**Deprecated:** {'✅' if node.get('deprecated') else '❌'}

---

## Description
{node.get('description', '')}

## Full Docstring
```
{node.get('docstring_full', '')}
```

## Links
{links_md if links_md else 'None'}

---
"""
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(md)

        written_files.append(str(file_path))

    return written_files
