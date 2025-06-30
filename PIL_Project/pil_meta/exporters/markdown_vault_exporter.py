# pil_meta/exporters/markdown_vault_exporter.py
"""
Markdown Vault Exporter (exporters)

Exports the PIL entity graph as Markdown/Obsidian-compatible files for each symbol,
using human-friendly names for navigation but always showing the real fqname.
"""

import os
from pathlib import Path


def friendly_name(node):
    """Returns a human-friendly display name for vault navigation.
    @tags: ["export", "vault"]
    @status: "stable"
    @visibility: "internal"
    """
    # Helper to pull from top-level or metadata
    def get_field(n, k):
        return n.get(k) or n.get("metadata", {}).get(k) or "unknown"

    module_name = get_field(node, "module")
    module_part = module_name.split(".")[-1] if module_name != "unknown" else "unknown"
    name = get_field(node, "name")
    function = get_field(node, "function")

    if node["type"] == "function":
        return f'{name or function or "?"} (in {module_part})'
    if node["type"] == "method":
        # Try to extract class from fqname: module.class.method
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


def _sanitize_filename(name):
    """Sanitizes a string for use as a safe Markdown filename.
    @tags: ["filesystem", "vault"]
    @status: "stable"
    @visibility: "internal"
    """
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


def export_markdown_vault(graph: dict, output_dir: str):
    """Export the entity graph as a Markdown vault: one file per node, with friendly names, tags, and links.
    @tags: ["export", "markdown", "vault"]
    @status: "stable"
    @visibility: "public"
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    for fqname, node in graph.items():
        friendly = friendly_name(node)
        subdir = node.get("type", "misc") + "s"
        node_dir = output_path / subdir
        node_dir.mkdir(parents=True, exist_ok=True)
        file_path = node_dir / (_sanitize_filename(friendly) + ".md")

        # Obsidian tag line
        tags = " ".join(f"#{t.replace(' ', '_')}" for t in node.get("tags", []))

        # Links section
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

    print(f"✅ Exported Markdown vault with friendly names to {output_path}")
