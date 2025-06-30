# pil_meta/exporters/usage_map_exporter.py

from pathlib import Path
import json
from datetime import datetime
from typing import Union, Optional

def export_usage_map(usage_map: dict,
                     output_dir: Union[str, Path],
                     project_name: str = "project",
                     timestamp: Optional[str] = None) -> dict:
    """
    Export the usage map to both a timestamped and stable JSON file.

    Args:
        usage_map (dict): Usage summary dictionary.
        output_dir (Union[str, Path]): Directory to write the JSON file into.
        project_name (str): Optional project name prefix for timestamped file.
        timestamp (Optional[str]): Optional timestamp string in YYYYMMDD_HHMMSS format.

    Returns:
        dict: Paths of both timestamped and stable filenames
    """
    outdir = Path(output_dir)
    outdir.mkdir(parents=True, exist_ok=True)

    ts = timestamp or datetime.now().strftime("%Y%m%d_%H%M%S")

    stable_path = outdir / "usage_map.json"
    ts_filename = f"usage_map_{project_name}_{ts}.json"
    ts_path = outdir / ts_filename

    with open(stable_path, "w", encoding="utf-8") as f:
        json.dump(usage_map, f, indent=2, ensure_ascii=False)

    with open(ts_path, "w", encoding="utf-8") as f:
        json.dump(usage_map, f, indent=2, ensure_ascii=False)

    return {
        "stable": str(stable_path),
        "timestamped": str(ts_path)
    }
