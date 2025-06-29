# PIL_Project/pil_meta/loaders/config_loader.py

import os
import json

def load_config(config_path="pilconfig.json"):
    """
    Load the PIL project configuration and resolve all paths as absolute.

    Args:
        config_path (str): Path to pilconfig.json file (absolute or relative)

    Returns:
        dict: Configuration fields with all main paths resolved as absolute paths.
    """
    config_abspath = os.path.abspath(config_path)
    config_dir = os.path.dirname(config_abspath)
    with open(config_abspath, "r", encoding="utf-8") as f:
        config = json.load(f)

    for key in [
        "project_root",
        "journal_path",
        "output_dir",
        "docs_dir",
        "vault_dir",
        "snapshot_dir",
    ]:
        if key in config and not os.path.isabs(config[key]):
            config[key] = os.path.abspath(os.path.join(config_dir, config[key]))

    config["config_self_path"] = config_abspath
    return config
