# pil_meta/loaders/markdown_loader.py
"""
Markdown Loader

Loads and parses all Markdown (.md) files from a documentation or journal directory.
Extracts frontmatter, tags, and optional code crosslinks for later graph integration.
"""

import os
from pathlib import Path
from typing import Any, Dict, List
import re

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)

def parse_frontmatter(md_content: str) -> Dict[str, Any]:
    """
    Extract YAML frontmatter as a dict, if present.

    Args:
        md_content (str): Raw contents of a markdown file.

    Returns:
        dict: Parsed frontmatter, or empty dict if none present.
    """
    match = FRONTMATTER_RE.match(md_content)
    if not match:
        return {}
    try:
        import yaml
        return yaml.safe_load(match.group(1))
    except ImportError:
        # Fallback: return raw as single value
        return {"frontmatter": match.group(1)}
    except Exception:
        return {}

def load_markdown_entries(journal_dir: str) -> List[Dict[str, Any]]:
    """
    Load all .md files from a directory and extract metadata for each.

    Args:
        journal_dir (str): Path to the journal or docs directory (absolute or relative)

    Returns:
        List[dict]: Each with filename, frontmatter, content, tags
    """
    # Bulletproof: always resolve journal_dir as absolute
    base_path = Path(journal_dir).resolve()
    entries = []
    for dirpath, _, filenames in os.walk(base_path):
        for filename in filenames:
            if filename.endswith('.md'):
                path = Path(dirpath) / filename
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                meta = parse_frontmatter(content)
                # Extract tags as #tag in body or from frontmatter
                tags = set(meta.get("tags", []))
                tags.update(
                    m[1:] for m in re.findall(r"#([\w_-]+)", content)
                )
                entries.append({
                    "filename": str(path),
                    "frontmatter": meta,
                    "tags": list(tags),
                    "content": content,
                })
    return entries
