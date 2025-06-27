# generate_function_map.py
# Scans a codebase and generates a function integration map with docstrings and basic flow metadata

import os
import ast
import pandas as pd
import json
import subprocess
from collections import defaultdict

PROJECT_ROOT = "./Adrift"
EXPORT_FOLDER = "exports"


def extract_subsystem_tags(doc):
    """
    Extract @subsystem tags from docstring.

    Parameters:
        doc (str): The full docstring to scan.

    Returns:
        list[str]: Subsystem tags (lowercased).
    """
    if not doc:
        return []
    lines = doc.strip().split("\n")
    tags = []
    for line in lines:
        line = line.strip()
        if line.startswith("@subsystem:"):
            tag = line.split(":", 1)[1].strip().lower()
            if tag:
                tags.append(tag)
    return tags


def infer_path_based_subsystem(filepath, root_dir):
    """
    Infer subsystem from Adrift subdirectory name.

    Parameters:
        filepath (str): Full path to the file.
        root_dir (str): Project root.

    Returns:
        str|None: Subsystem string or None if unknown.
    """
    rel = os.path.relpath(filepath, root_dir).replace("\\", "/")
    parts = rel.split("/")
    if len(parts) >= 2 and parts[0] == "Adrift":
        return parts[1].lower()
    return None


def extract_functions_from_file(filepath, root_dir):
    """
    Parse a Python file and extract function definitions.

    Parameters:
        filepath (str): Path to the .py file.
        root_dir (str): Root of the project for relative module paths.

    Returns:
        list[dict]: Metadata for each function.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()

    tree = ast.parse(source, filename=filepath)
    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_name = node.name
            lineno = node.lineno
            doc = ast.get_docstring(node)
            rel_path = os.path.relpath(filepath, root_dir).replace("\\", "/")
            module = rel_path.replace(".py", "")

            # Subsystems = tag-based + fallback from folder
            tag_subsystems = extract_subsystem_tags(doc)
            path_subsystem = infer_path_based_subsystem(filepath, root_dir)
            subsystems = sorted(set(tag_subsystems + ([path_subsystem] if path_subsystem else [])))

            functions.append({
                "module": module,
                "function": func_name,
                "fqname": f"{module}.{func_name}",
                "lineno": lineno,
                "doc": doc or "",
                "calls_fqns": [],
                "called_by_fqns": [],
                "subsystems": subsystems
            })
    return functions


def build_function_index(root_dir):
    """
    Walk the project and build a function index.

    Parameters:
        root_dir (str): Project root to scan.

    Returns:
        pd.DataFrame: Collected function data.
    """
    all_functions = []
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(subdir, file)
                try:
                    all_functions.extend(extract_functions_from_file(full_path, root_dir))
                except Exception as e:
                    print(f"❌ Error parsing {full_path}: {e}")
    df = pd.DataFrame(all_functions)
    df.sort_values(by=["module", "lineno"], inplace=True)
    return df


def ensure_export_dir():
    os.makedirs(EXPORT_FOLDER, exist_ok=True)


def export_index(df):
    """
    Save index as CSV, Markdown, and JSON.

    Parameters:
        df (pd.DataFrame): Data to export.
    """
    df.to_csv(f"{EXPORT_FOLDER}/function_index.csv", index=False)
    df.to_markdown(f"{EXPORT_FOLDER}/function_index.md", index=False)
    df.to_json(f"{EXPORT_FOLDER}/function_map.json", orient="records", indent=2)


def export_subsystem_map(df):
    """
    Group functions by subsystem and export Markdown summary.

    Parameters:
        df (pd.DataFrame): Indexed function data with subsystem info.
    """
    grouped = defaultdict(list)
    for _, row in df.iterrows():
        for group in row.subsystems:
            grouped[group].append((row.fqname, row.doc.strip().split("\n")[0] if row.doc else ""))

    with open(f"{EXPORT_FOLDER}/subsystem_map.md", "w", encoding="utf-8") as f:
        f.write("# 🧠 Subsystem Map\n\n")
        for key in sorted(grouped):
            f.write(f"## 🧩 {key}\n\n")
            for fqname, doc in sorted(grouped[key]):
                f.write(f"- `{fqname}` — {doc}\n")
            f.write("\n")


if __name__ == "__main__":
    """
    Main entry point. Generates base function map and triggers analysis tools.
    """
    ensure_export_dir()
    df = build_function_index(PROJECT_ROOT)
    export_index(df)
    export_subsystem_map(df)
    print("\n✅ Exported base function map and subsystem map")

    # 🔁 Run post-analysis tools (will modify function_map.json in place)
    subprocess.run(["python", "scripts/test_coverage_estimator.py"])
    subprocess.run(["python", "scripts/unused_function_detector.py"])
    print("\n✅ Analysis tools complete")


# TODO:
# - Integrate with refactor risk scoring
# - Add CLI args for per-tool invocation
# - Consider mapping subsystems to domain-level packages
