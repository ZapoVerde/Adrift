# tests/test_exporters_edgecases.py

import os
import json
import shutil
from pil_meta.exporters.markdown_vault_exporter import export_markdown_vault

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "export_edgecases")
INPUT_JSON = os.path.join(os.path.dirname(__file__), "sample_input", "sample_graph_edge_cases.json")

def setup_module():
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)

def test_exporter_handles_edge_cases():
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        sample_graph = json.load(f)
    export_markdown_vault(sample_graph, OUTPUT_DIR)
    # This will run the exporter; manual spot-check of output is recommended for edge cases.
    assert os.path.isdir(OUTPUT_DIR)
    # Optional: add more specific checks for files/contents if desired.
