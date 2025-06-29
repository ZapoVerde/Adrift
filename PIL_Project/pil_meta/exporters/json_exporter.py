# pil_meta/exporters/json_exporter.py
"""
Export the full entity graph to a structured JSON file.

Part of the PIL output pipeline. This module writes the final metadata graph
produced by `entity_graph_builder.py` to disk in a machine-readable format.

Outputs:
  - entity_graph.json → Complete node metadata and semantic linkages

Conforms to the PIL metadata strategy:
  - Includes docstrings, tags, governance flags, and semantic edges
  - Supports downstream validation, journal linkage, and vault export
"""

import os
import json
from pathlib import Path

def export_entity_graph(graph: dict, output_dir: str) -> None:
    """
    Write the in-memory entity graph to `entity_graph.json`.

    Parameters:
        graph (dict): The keyed graph structure, e.g., { fqname: { ... } }
        output_dir (str): Directory to emit the file into (relative or absolute)

    Notes:
        - Output path is `${output_dir}/entity_graph.json`
        - Will create the directory if it does not exist
        - File is formatted with 2-space indentation
    """
    outdir = Path(output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    outfile = outdir / "entity_graph.json"
    with open(outfile, "w", encoding="utf-8") as f:
        json.dump(graph, f, indent=2, ensure_ascii=False)
    print(f"✅ Exported entity graph → {outfile}")
