# scripts/load_all_symbols.py

import os
from pil_meta.loaders.code_loader import load_code_symbols
from pil_meta.builders.entity_graph_builder import build_entity_graph
import json

def load_all_symbols(project_root):
    all_symbols = []
    for dirpath, _, filenames in os.walk(project_root):
        for filename in filenames:
            if filename.endswith('.py'):
                fullpath = os.path.join(dirpath, filename)
                try:
                    symbols = load_code_symbols(fullpath)
                    all_symbols.extend(symbols)
                except Exception as e:
                    print(f"⚠️ Skipping {fullpath}: {e}")
    return all_symbols

if __name__ == "__main__":
    project_root = "pil_meta"  # Set your project root here
    symbols = load_all_symbols(project_root)
    print(f"Loaded {len(symbols)} symbols from project.")

    entity_graph = build_entity_graph(symbols)
    with open("entity_graph.json", "w", encoding="utf-8") as f:
        json.dump(entity_graph, f, indent=2)
    print("✅ Wrote entity_graph.json")
