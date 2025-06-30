#!/usr/bin/env python3
"""
run_pil_self.py — Self-runner version for PIL_Project
Usage:
    ./run_pil_self.py

This version is designed to live **inside the PIL_Project folder**.
It runs the pipeline using pil_meta as the project root and references pilconfig_self.json.
"""

import subprocess
import sys
from pathlib import Path

# Define pipeline script and config path
pipeline_script = Path("scripts/rebuild_pil.py")
config_path = Path("pilconfig_self.json")

if not pipeline_script.exists():
    print(f"❌ Could not find pipeline script at: {pipeline_script.resolve()}")
    sys.exit(1)

if not config_path.exists():
    print(f"❌ Could not find config file at: {config_path.resolve()}")
    sys.exit(1)

print(f"🚀 Running PIL pipeline from: {pipeline_script.resolve()}")
subprocess.run(
    [sys.executable, str(pipeline_script),
     str(config_path)], check=True)
