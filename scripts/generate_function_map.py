# generate_function_map.py
# Builds a semantic function map (inputs, outputs, relationships) from codebase

import os
import ast
import json
from collections import defaultdict

EXPORT_FOLDER = "exports"

# --- Core Extraction Functions ---

def extract_functions(filepath, root_dir):
    """Parses a file and returns function records with arguments, doc, and called functions."""
    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()

    tree = ast.parse(source, filename=filepath)
    rel_path = os.path.relpath(filepath, root_dir).replace("\\", "/")
    functions = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            calls = set()
            for subnode in ast.walk(node):
                if isinstance(subnode, ast.Call):
                    try:
                        if isinstance(subnode.func, ast.Name):
                            calls.add(subnode.func.id)
                        elif isinstance(subnode.func, ast.Attribute):
                            calls.add(subnode.func.attr)
                    except Exception:
                        continue

            functions.append({
                "module": rel_path,
                "name": node.name,
                "fqname": rel_path.replace("/", ".") + "." + node.name,
                "lineno": node.lineno,
                "args": [rel_path.replace("/", ".") + "." + arg.arg for arg in node.args.args],
                "doc": ast.get_docstring(node) or "",
                "calls": sorted(list(calls))
            })

    return functions

# --- Mapping and Output ---

def build_function_graph(root_dir):
    """Walks the codebase and builds function records and reverse call index."""
    all_funcs = []
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(subdir, file)
                try:
                    all_funcs.extend(extract_functions(full_path, root_dir))
                except Exception as e:
                    print(f"❌ Error parsing {full_path}: {e}")

    fqname_index = {f['name']: f['fqname'] for f in all_funcs}
    reverse_calls = defaultdict(list)

    for f in all_funcs:
        f['call_fqns'] = [fqname_index.get(c, c) for c in f['calls']]
        for called in f['calls']:
            if called in fqname_index:
                reverse_calls[fqname_index[called]].append(f['fqname'])

    for f in all_funcs:
        f['called_by_fqns'] = sorted(list(set(reverse_calls.get(f['fqname'], []))))

    return all_funcs

def export_as_json(records, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)

def export_as_markdown(records, output_path):
    by_module = defaultdict(list)
    for f in records:
        by_module[f['module']].append(f)

    with open(output_path, "w", encoding="utf-8") as f:
        for module in sorted(by_module):
            f.write(f"## 📦 {module}\n\n")
            for func in sorted(by_module[module], key=lambda x: x['lineno']):
                f.write(f"### `{func['name']}()` – line {func['lineno']}\n")
                if func['doc']:
                    f.write(f"_Purpose_: {func['doc'].strip().splitlines()[0]}\n")
                if func['args']:
                    f.write(f"_Inputs_: {', '.join(func['args'])}\n")
                if func['call_fqns']:
                    f.write(f"_Calls_: {', '.join(func['call_fqns'])}\n")
                if func['called_by_fqns']:
                    f.write(f"_Called by_: {', '.join(func['called_by_fqns'])}\n")
                f.write("\n")
            f.write("---\n\n")

# --- Entry Point ---
if __name__ == "__main__":
    PROJECT_ROOT = "./Adrift"
    os.makedirs(EXPORT_FOLDER, exist_ok=True)

    graph = build_function_graph(PROJECT_ROOT)
    export_as_json(graph, os.path.join(EXPORT_FOLDER, "function_map.json"))
    export_as_markdown(graph, os.path.join(EXPORT_FOLDER, "function_map.md"))

    print("\n✅ Exported to exports/function_map.json and exports/function_map.md")
