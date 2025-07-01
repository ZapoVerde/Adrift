# pil_meta/exporters/markdown_vault_exporter.py
"""
Markdown vault exporter for PIL project.

Exports the entire codebase entity graph as a set of Markdown files, suitable for
importing into Obsidian or other knowledge vault tools. Each symbol (function,
class, etc.) is exported as a separate file with PIL metadata, links, and
friendly names.

@tags: ["export", "markdown", "vault"]
@status: "stable"
"""

import os
from pathlib import Path
from typing import Union, Optional

def friendly_name(node: dict) -> str:
    """
    Returns a human-friendly display name for vault navigation.

    Args:
        node (dict): Entity graph node.

    Returns:
        str: User-friendly label for UI or markdown heading.

    Recursive note: This function may call itself via the filename sanitizer for
    fallback purposes, but always resolves due to string fallback.
    """
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
    """
    Sanitizes a string for use as a safe Markdown filename.

    Args:
        name (str): Raw symbol or friendly name.

    Returns:
        str: Sanitized string safe for the filesystem.
    """
    # Recursion note: Called by friendly_name and may call friendly_name for fallback.
    # Always terminates, as string fallback is enforced.
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
    """
    Exports the given entity graph to a Markdown "vault"—one .md file per symbol.

    Args:
        graph (dict): Entity graph as produced by pipeline.
        output_dir (str or Path): Destination directory for vault.
        project_name (str, optional): Project display name (for metadata).
        timestamp (str, optional): Run timestamp for traceability.

    Returns:
        list[str]: List of written Markdown file paths.

    Each file contains:
    - Friendly name as H1 heading
    - FQ name, type, status, visibility, tags, deprecated status
    - Description and full docstring
    - Structured links to other nodes and journal entries

    Folders are organized by symbol type (e.g., functions/, classes/).
    Files are sanitized for filesystem safety and Obsidian compatibility.

    @tags: ["export", "markdown", "vault"]
    @status: "stable"
    """
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
