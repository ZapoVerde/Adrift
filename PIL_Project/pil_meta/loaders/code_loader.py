# code_loader.py
"""
Extract all symbols (function, class, method, variable, module) from a single Python source file.
"""

import ast
import os

def load_code_symbols(pyfile_path):
    """
    Parse a single Python file and return a list of symbols with metadata.

    Args:
        pyfile_path (str): Path to .py file.

    Returns:
        list of dicts: Each with type, name, fqname, module, lineno, doc.
    """
    with open(pyfile_path, "r", encoding="utf-8") as f:
        source = f.read()

    module_name = os.path.splitext(os.path.basename(pyfile_path))[0]
    symbol_list = []

    # Module-level docstring
    tree = ast.parse(source, filename=pyfile_path)
    module_doc = ast.get_docstring(tree)
    symbol_list.append({
        "type": "module",
        "name": module_name,
        "fqname": module_name,
        "module": module_name,
        "lineno": 1,
        "doc": module_doc or ""
    })

    # Collect assignments for variables with comments
    lines = source.splitlines()
    for idx, line in enumerate(lines):
        if "=" in line and "#" in line:
            # very naive: MY_CONSTANT = 42  # comment
            parts = line.split("#", 1)
            left = parts[0].strip()
            right = parts[1].strip()
            if "=" in left:
                var_name = left.split("=")[0].strip()
                symbol_list.append({
                    "type": "variable",
                    "name": var_name,
                    "fqname": f"{module_name}.{var_name}",
                    "module": module_name,
                    "lineno": idx + 1,
                    "doc": right
                })

    # AST walk for classes/functions
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            is_method = False
            parent = getattr(node, 'parent', None)
            if parent and isinstance(parent, ast.ClassDef):
                is_method = True
            symbol_list.append({
                "type": "method" if is_method else "function",
                "name": node.name,
                "fqname": f"{module_name}.{node.name}",
                "module": module_name,
                "lineno": node.lineno,
                "doc": ast.get_docstring(node) or ""
            })
        elif isinstance(node, ast.ClassDef):
            symbol_list.append({
                "type": "class",
                "name": node.name,
                "fqname": f"{module_name}.{node.name}",
                "module": module_name,
                "lineno": node.lineno,
                "doc": ast.get_docstring(node) or ""
            })

    # Fix parent linkage for methods
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child.parent = node

    # Patch types: fix methods so they're not misclassified as top-level functions
    for s in symbol_list:
        if s["type"] == "function":
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == s["name"]:
                    parent = getattr(node, 'parent', None)
                    if parent and isinstance(parent, ast.ClassDef):
                        s["type"] = "method"

    return symbol_list
