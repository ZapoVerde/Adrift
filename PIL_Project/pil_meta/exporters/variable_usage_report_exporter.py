# pil_meta/exporters/variable_usage_reporter.py

from pathlib import Path
from typing import Union, Optional

def export_variable_usage_markdown(usage_map: dict,
                                   output_path: Union[str, Path],
                                   project_name: str = "project",
                                   timestamp: Optional[str] = None) -> str:
    """
    Export the variable usage summary to a Markdown file.

    Args:
        usage_map (dict): Usage summary from build_usage_map().
        output_path (Union[str, Path]): Path to write the Markdown output to.
        project_name (str): Optional project name prefix (unused).
        timestamp (Optional[str]): Optional timestamp (unused).

    Returns:
        str: Full path to the written Markdown file.
    """
    output_path = Path(output_path)

    lines = ["# Variable Usage Report\n"]
    for varname, usage in sorted(usage_map.get("variable_usage", {}).items()):
        lines.append(f"\n## `{varname}`")
        for user in usage:
            lines.append(f"- `{user}`")

    output_path.write_text("\n".join(lines), encoding="utf-8")
    return str(output_path)
