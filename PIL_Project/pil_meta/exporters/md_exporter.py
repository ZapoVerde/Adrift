# pil_meta/exporters/md_exporter.py
"""
Markdown Exporter (exporters)

Exports a single code entity as a Markdown file with metadata and Obsidian links.
Intended for use in manual or fine-grained exports, not for bulk vault building.
"""

import os
from pathlib import Path

def export_entity_markdown(entity: dict, output_dir: str) -> None:
    """
    Export a single entity as a Markdown file with metadata and Obsidian links.

    Args:
        entity (dict): Entity metadata dictionary, e.g.
            {
                "fqname": "module.func",
                "type": "function",
                "description": "...",
                "tags": ["combat", "stateful"],
                ...
            }
        output_dir (str): Directory to write markdown file.
    """
    outdir = Path(output_dir)
    outdir.mkdir(parents=True, exist_ok=True)

    name = entity.get("name") or entity.get("function") or entity.get("fqname")
    type_ = entity.get("type", "unknown")
    fqname = entity.get("fqname", "")
    tags = entity.get("tags", [])
    docstring = entity.get("docstring_full", "")
    description = entity.get("description", "")
    status = entity.get("status", "n/a")
    visibility = entity.get("visibility", "n/a")
    deprecated = "✅" if entity.get("deprecated") else "❌"
    links_md = ""

    if entity.get("links"):
        for link in entity["links"]:
            links_md += f"- **{link.get('type', 'link')}**: {link.get('target')}\n"
    if entity.get("linked_journal_entry"):
        links_md += f"- **journal**: {entity['linked_journal_entry']}\n"
    tags_md = " ".join(f"#{t.replace(' ', '_')}" for t in tags)

    # Sanitize filename for filesystem
    def _sanitize_filename(s):
        return (
            s.replace("/", "_")
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

    filename = _sanitize_filename(name) + ".md"
    filepath = outdir / filename

    md = f"""# {name}
> **Fully qualified name:** `{fqname}`

**Type:** {type_}
**Status:** {status}
**Visibility:** {visibility}
**Tags:** {tags_md}
**Deprecated:** {deprecated}

---

## Description
{description}

## Full Docstring
```
{docstring}
```

## Links
{links_md if links_md else 'None'}

---
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"✅ Exported entity markdown → {filepath}")
