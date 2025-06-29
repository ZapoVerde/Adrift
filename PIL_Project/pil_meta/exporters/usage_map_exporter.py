# pil_meta/exporters/usage_map_exporter.py

from pathlib import Path
import json

def export_usage_map(usage_map: dict, output_dir: str) -> None:
    """
    Export the usage map as usage_map.json.

    Args:
        usage_map (dict): Usage summary dictionary (see build_usage_map).
        output_dir (str): Directory to write the JSON file into.
    """
    outdir = Path(output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    outfile = outdir / "usage_map.json"
    with open(outfile, "w", encoding="utf-8") as f:
        json.dump(usage_map, f, indent=2, ensure_ascii=False)
    print(f"✅ Exported usage map → {outfile}")
