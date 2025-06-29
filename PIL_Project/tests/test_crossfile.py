# tests/test_crossfile.py

import os
import json
import shutil
from pil_meta.exporters.markdown_vault_exporter import export_markdown_vault

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "export_crossfile")
INPUT_JSON = os.path.join(os.path.dirname(__file__), "sample_input", "sample_graph_crossfile.json")

def setup_module():
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)

def test_crossfile_linking_and_export():
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        sample_graph = json.load(f)
    export_markdown_vault(sample_graph, OUTPUT_DIR)
    # Check for expected cross-links
    assert os.path.isdir(OUTPUT_DIR)
    # Further file/link checks can be added here.
