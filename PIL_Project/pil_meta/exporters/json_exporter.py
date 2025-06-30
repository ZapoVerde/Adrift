# pil_meta/exporters/json_exporter.py

import json
from datetime import datetime
from pathlib import Path
from typing import Union, Optional

def export_entity_graph(graph: dict,
                        output_dir: Union[str, Path],
                        project_name: str = "project",
                        timestamp: Optional[str] = None) -> dict:
    """
    Exports the entity graph as both a stable file and timestamped variant.

    Args:
        graph (dict): Entity graph.
        output_dir (Union[str, Path]): Where to write output files.
        project_name (str): Optional project name to prefix timestamped file.
        timestamp (Optional[str]): Optional timestamp override (format: YYYYMMDD_HHMMSS).

    Returns:
        dict: {
            "stable": path to entity_graph.json,
            "timestamped": path to entity_graph_<project>_<timestamp>.json
        }
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    ts = timestamp or datetime.now().strftime("%Y%m%d_%H%M%S")

    stable_path = output_dir / "entity_graph.json"
    ts_filename = f"entity_graph_{project_name}_{ts}.json"
    ts_path = output_dir / ts_filename

    with open(stable_path, "w", encoding="utf-8") as f:
        json.dump(graph, f, indent=2)

    with open(ts_path, "w", encoding="utf-8") as f:
        json.dump(graph, f, indent=2)

    return {
        "stable": str(stable_path),
        "timestamped": str(ts_path)
    }
