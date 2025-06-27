# lint/check_docstrings.py
"""
Checks all functions and methods in the project for Google-style docstrings.

Reports any functions missing a docstring or using a non-standard format.
Intended to be run manually or via pre-commit/pytest hook.
"""

import os
import ast
import re

PROJECT_ROOT = "Adrift"  # Adjust if needed

# Google-style indicator patterns
VALID_SECTIONS = {"Args", "Returns", "Raises", "Examples", "Note", "Attributes"}
SECTION_PATTERN = re.compile(r"^\s*(Args|Returns|Raises|Examples|Note|Attributes)\s*:", re.MULTILINE)

def is_google_style(docstring: str) -> bool:
    """
    Returns True if the docstring includes one or more Google-style section headers.
    """
    return bool(SECTION_PATTERN.search(docstring))


def check_file_for_docstrings(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()

    tree = ast.parse(source)
    errors = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            name = node.name
            lineno = node.lineno
            docstring = ast.get_docstring(node)

            if not docstring:
                errors.append((lineno, name, "Missing docstring"))
            elif not is_google_style(docstring):
                errors.append((lineno, name, "Non-Google-style docstring"))

    return errors


def scan_project():
    all_violations = []

    for dirpath, _, filenames in os.walk(PROJECT_ROOT):
        for filename in filenames:
            if filename.endswith(".py"):
                path = os.path.join(dirpath, filename)
                violations = check_file_for_docstrings(path)
                if violations:
                    all_violations.append((path, violations))

    return all_violations


if __name__ == "__main__":
    violations = scan_project()
    if not violations:
        print("✅ All functions have Google-style docstrings.")
    else:
        for path, issues in violations:
            print(f"\n❌ {path}")
            for lineno, name, reason in issues:
                print(f"  [L{lineno:>4}] {name} — {reason}")
        exit(1)
