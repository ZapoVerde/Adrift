import os

def export_entity_markdown(entity, output_dir):
    """
    Export a single entity as a Markdown file with metadata and Obsidian links.

    Args:
        entity (dict): Entity metadata dictionary, e.g. {
            "fqname": "module.func",
            "type": "function",
            "doc": "...",
            "tags": ["combat", "stateful"],
            ...
        }
        output_dir (str): Directory to write markdown file.
    """
    os.makedirs(output_dir, exist_ok=True)
    friendly_name = entity.get("fqname", "unknown_entity")
    filename = os.path.join(output_dir, f"{friendly_name}.md")

    with open(filename, "w", encoding="utf-8") as f:
        # Top metadata block
        f.write(f"# {friendly_name}\n\n")
        f.write(f"**Type:** {entity.get('type', 'unknown')}\n\n")
        f.write(f"**Tags:** {', '.join(entity.get('tags', []))}\n\n")
        f.write("---\n\n")
        f.write(entity.get("doc", "No documentation available.") + "\n\n")
        # Example Obsidian link usage
        f.write(f"See related entities:\n")
        for tag in entity.get("tags", []):
            f.write(f"- [[{tag}]]\n")
