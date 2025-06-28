# rebuild_pil.py
"""
CLI entry point to trigger full PIL metadata pipeline.

Usage:
    python scripts/rebuild_pil.py

Reads from pilconfig.json and emits entity_graph.json and other metadata exports.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


from pil_meta.pipeline import run_pipeline
if __name__ == "__main__":
    run_pipeline()
