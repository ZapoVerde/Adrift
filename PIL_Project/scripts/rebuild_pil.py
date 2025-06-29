# scripts/rebuild_pil.py
# to call run: python scripts/rebuild_pil.py
"""
Rebuild PIL Metadata

Script entry point for full rebuild of PIL project intelligence data.
Simply runs the pipeline and exits. Can be called by CI or developer CLI.
"""

from pil_meta.pipeline import run_pipeline

if __name__ == "__main__":
    run_pipeline()
