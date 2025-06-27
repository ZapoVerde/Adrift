# test_coverage_estimator.py
# Scans test files and estimates static coverage for each function in function_map.json

import os
import json
import re

INPUT_PATH = "exports/function_map.json"
TEST_DIR = "tests"
OUTPUT_JSON = "exports/test_coverage_report.json"
OUTPUT_MD = "exports/test_coverage_report.md"


def load_function_map(path):
    """
    Load the function map from disk.

    Parameters:
        path (str): Path to JSON file.

    Returns:
        list[dict]: List of function records.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def scan_test_code(test_dir):
    """
    Scan test files for mentioned function names.

    Parameters:
        test_dir (str): Directory containing test files.

    Returns:
        set[str]: Function names mentioned in test files.
    """
    mentioned = set()
    pattern = re.compile(r"\b([a-zA-Z_][a-zA-Z0-9_]*)\b")

    for root, _, files in os.walk(test_dir):
        for file in files:
            if file.startswith("test_") and file.endswith(".py"):
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    for line in f:
                        for match in pattern.findall(line):
                            mentioned.add(match)
    return mentioned


def classify_coverage(functions, mentioned):
    """
    Tag functions as tested, maybe tested, or untested.

    Parameters:
        functions (list[dict]): Function records.
        mentioned (set[str]): Function names found in test code.

    Returns:
        list[dict]: Functions with added 'coverage' tag.
    """
    tested = set()
    for f in functions:
        if f["name"] in mentioned:
            f["coverage"] = "✅ tested"
            tested.add(f["fqname"])

    for f in functions:
        if "coverage" not in f:
            if any(caller in tested for caller in f.get("called_by_fqns", [])):
                f["coverage"] = "⚠️ maybe"
            else:
                f["coverage"] = "❌ untested"
    return functions


def export_json(functions, path):
    """
    Save function coverage info as JSON.

    Parameters:
        functions (list[dict]): Functions with coverage info.
        path (str): Output file path.
    """
    with open(path, "w", encoding="utf-8") as f:
        json.dump(functions, f, indent=2)


def export_markdown(functions, path):
    """
    Save function coverage info as Markdown summary.

    Parameters:
        functions (list[dict]): Functions with coverage info.
        path (str): Output file path.
    """
    categories = {"✅ tested": [], "⚠️ maybe": [], "❌ untested": []}
    for f in functions:
        categories[f["coverage"]].append(f)

    with open(path, "w", encoding="utf-8") as f:
        f.write("# 🧪 Test Coverage Report (Static)\n\n")
        for tag, funcs in categories.items():
            f.write(f"## {tag} ({len(funcs)} functions)\n\n")
            for func in sorted(funcs, key=lambda x: x["fqname"]):
                doc = func["doc"].strip().split("\n")[0] if func["doc"] else ""
                f.write(f"- `{func['fqname']}` — {doc}\n")
            f.write("\n")


if __name__ == "__main__":
    """
    Main entry point. Loads function map and scans tests for static coverage tags.
    """
    if not os.path.exists(INPUT_PATH):
        print(f"❌ Missing {INPUT_PATH}. Run generate_function_map.py first.")
    else:
        funcs = load_function_map(INPUT_PATH)
        mentions = scan_test_code(TEST_DIR)
        tagged = classify_coverage(funcs, mentions)
        export_json(tagged, OUTPUT_JSON)
        export_markdown(tagged, OUTPUT_MD)
        print(f"✅ Exported static test coverage to {OUTPUT_JSON} and {OUTPUT_MD}")


# TODO:
# - Support filtering by subsystem or module
# - Colorize Markdown output
# - Build a heatmap view by file
