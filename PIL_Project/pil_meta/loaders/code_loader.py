# code_loader.py
"""
Loader: Code Symbols

Extracts top-level function symbols from Python files within the configured project root.
Each symbol includes its fully qualified name, module, line number, docstring summary, and flags.
"""

import os
import ast
import json
from pathlib import Path

def load_config(config_path="pilconfig.json"):
    """
    Load the global PIL configuration file.

    Returns:
        dict: Parsed configuration values.
    """
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def extract_docstring_flags(doc):
    """
    Parse flags and tags from a docstring.

    Recognized tags:
    - @subsystem:<tag>
    - @ignore
    - @deprecated

    Returns:
        dict: Extracted flags and tags.
    """
    flags = {
        "subsystems": [],
        "ignore": False,
        "deprecated": False,
    }
    if not doc:
        return flags

    for line in doc.strip().split("\n"):
        line = line.strip()
        if line.startswith("@subsystem:"):
            tag = line.split(":", 1)[1].strip().lower()
            if tag:
                flags["subsystems"].append(tag)
        elif line.startswith("@ignore"):
            flags["ignore"] = True
        elif line.startswith("@deprecated"):
            flags["deprecated"] = True

    return flags

def extract_functions_from_file(filepath, root_path):
    """
    Extract all function definitions from a single Python file.

    Args:
        filepath (Path): Full path to a Python source file.
        root_path (Path): Root project path for relative module resolution.

    Returns:
        list[dict]: List of extracted symbol records.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()

    try:
        tree = ast.parse(source, filename=str(filepath))
    except SyntaxError as e:
        print(f"⚠️ Skipping {filepath}: {e}")
        return []

    functions = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            doc = ast.get_docstring(node)
            flags = extract_docstring_flags(doc)
            rel_path = filepath.relative_to(root_path).as_posix()
            module = rel_path.replace(".py", "").replace("/", ".")
            fqname = f"{module}.{node.name}"

            functions.append({
                "fqname": fqname,
                "module": module,
                "function": node.name,
                "lineno": node.lineno,
                "description": doc.strip().split("\n")[0] if doc else "",
                "tags": flags["subsystems"],
                "ignore": flags["ignore"],
                "deprecated": flags["deprecated"],
                "source_file": rel_path
            })
    return functions

def load_code_symbols(config_path="pilconfig.json"):
    """
    Entry point for symbol extraction.

    Loads configuration and extracts all function symbols from the project root.

    Returns:
        list[dict]: All discovered function symbols.
    """
    config = load_config(config_path)
    root_path = Path(config["project_root"]).resolve()
    all_symbols = []

    for path in root_path.rglob("*.py"):
        if path.name.startswith("_"):
            continue  # Skip __init__.py or hidden files
        try:
            all_symbols.extend(extract_functions_from_file(path, root_path))
        except Exception as e:
            print(f"❌ Error in {path}: {e}")

    return all_symbols

if __name__ == "__main__":
    from pprint import pprint
    pprint(load_code_symbols())
