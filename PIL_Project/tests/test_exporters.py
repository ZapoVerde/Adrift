import os
import shutil
from pil_meta.exporters.md_exporter import export_entity_markdown

TEST_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "export_test_output")

def setup_module():
    # Clean test output folder before test run
    if os.path.exists(TEST_OUTPUT_DIR):
        shutil.rmtree(TEST_OUTPUT_DIR)

def test_export_entity_markdown_creates_file_and_content():
    entity = {
        "fqname": "sample.module.func",
        "type": "function",
        "doc": "This is a sample function for testing.",
        "tags": ["sample", "test", "exporter"]
    }

    export_entity_markdown(entity, TEST_OUTPUT_DIR)
    md_file = os.path.join(TEST_OUTPUT_DIR, "sample.module.func.md")
    assert os.path.isfile(md_file), "Markdown file was not created."

    with open(md_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Check content basics
    assert content.startswith("# sample.module.func")
    assert "**Type:** function" in content
    assert "**Tags:** sample, test, exporter" in content
    assert "This is a sample function for testing." in content

    # Check Obsidian link syntax for tags
    for tag in entity["tags"]:
        assert f"[[{tag}]]" in content
