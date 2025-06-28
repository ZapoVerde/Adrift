# test_pipeline.py
"""
Smoke test for the Project Intelligence Layer (PIL) pipeline.

Validates that:
- The pipeline executes without error
- `entity_graph.json` is created
- At least one function node is present
- Required metadata fields exist on a sample node

This test does not validate semantic links or coverage logic — those are handled in their own modules.
"""

import sys
from pathlib import Path
import json
import pytest

# Ensure the pil_meta package is importable (local dev support)
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pil_meta.pipeline import run_pipeline


@pytest.mark.smoke
def test_pipeline_generates_valid_entity_graph():
    """
    End-to-end test of the PIL pipeline on real source code.
    """
    output_path = Path("exports/entity_graph.json")

    # Clean up prior run
    if output_path.exists():
        output_path.unlink()

    run_pipeline()

    assert output_path.exists(), "entity_graph.json was not created"

    with output_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    assert isinstance(data, dict), "Output must be a dict"
    assert len(data) > 0, "Graph must contain at least one entity"

    # Validate required fields on a sample node
    sample = next(iter(data.values()))
    required_fields = [
        "fqname", "type", "description", "tags", "source_file",
        "test_coverage", "docstring_present", "linked_journal_entry",
        "is_orphaned", "metadata", "links"
    ]

    for field in required_fields:
        assert field in sample, f"Missing field: {field}"
