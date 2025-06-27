# unused_function_detector.py
# Scans function_map.json and outputs a list of functions that are not called by any others

import json
import os
from collections import defaultdict

INPUT_PATH = "exports/function_map.json"
OUTPUT_PATH = "exports/unused_functions.md"

def load_function_map(path):
    """
    Load the function map from JSON.

    Parameters:
        path (str): Path to the function_map.json file.

    Returns:
        list[dict]: Parsed function records.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def detect_unused_functions(functions):
    """
    Identify functions that are never called by any other function.

    Parameters:
        functions (list[dict]): List of function records.

    Returns:
        list[dict]: Subset of functions where 'called_by_fqns' is empty.
    """
    return [f for f in functions if not f.get("called_by_fqns")]

def group_by_module(functions):
    """
    Group function records by their module.

    Parameters:
        functions (list[dict]): List of function records.

    Returns:
        dict[str, list[dict]]: Mapping from module path to its functions.
    """
    grouped = defaultdict(list)
    for f in functions:
        grouped[f["module"]].append(f)
    return grouped

def export_markdown(unused_funcs, path):
    """
    Write unused function report to Markdown.

    Parameters:
        unused_funcs (list[dict]): List of unused function records.
        path (str): Output file path.
    """
    grouped = group_by_module(unused_funcs)
    with open(path, "w", encoding="utf-8") as f:
        f.write("# 🧹 Unused Function Report\n\n")
        f.write("These functions are not called by any other function.\n\n")
        for module in sorted(grouped):
            f.write(f"## 📦 {module}\n\n")
            for func in sorted(grouped[module], key=lambda x: x["lineno"]):
                fqname = func["fqname"]
                doc = func["doc"].strip().split("\n")[0] if func["doc"] else ""
                f.write(f"- `{fqname}` — {doc}\n")
            f.write("\n")

if __name__ == "__main__":
    """
    Main entry point. Loads function map and writes unused function report.
    """
    if not os.path.exists(INPUT_PATH):
        print(f"❌ No input found at {INPUT_PATH}")
    else:
        functions = load_function_map(INPUT_PATH)
        unused = detect_unused_functions(functions)
        export_markdown(unused, OUTPUT_PATH)
        print(f"✅ Found {len(unused)} unused functions. Report saved to {OUTPUT_PATH}")


# TODO:
# - Add optional ignore list for known entrypoints
# - Detect @cli or @entry annotations
# - Visualize with DOT or interactive HTML
