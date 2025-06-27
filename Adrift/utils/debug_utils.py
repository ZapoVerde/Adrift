# utils/debug_utils.py
# ─────────────────────────────────────────────────────────────
# 🐞 DEBUG HELPER
# Provides debug() function that respects global DEBUG_MODE.
# Automatically tags debug output with the caller module.
# ─────────────────────────────────────────────────────────────



import sys, os

# Dynamically add project root (one level above /utils/) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Adrift.config import DEBUG_MODE

import inspect

def debug(message: str):
    if DEBUG_MODE:
        caller = inspect.stack()[1].filename.split('/')[-1].replace('.py', '')
        print(f"[{caller.upper()} DEBUG] {message}")
