# run_debugger.py
"""
Satellite relay for launching a ParetoDebugger test entrypoint.

Tests all four debug primitives: debug(), get_debugger(), generate_trace_id(), and debug_trace().
Auto-patches sys.path to ensure sibling access to ParetoDebug is stable.

@tags: ["entrypoint", "debug", "orchestration", "mvp"]
@status: "stable"
"""

import sys
from pathlib import Path

# ========== AUTO-CONFIGURE IMPORT PATH ==========
PROJECT_ROOT = Path(__file__).parent.resolve()
PARETO_PATH = PROJECT_ROOT / "ParetoDebug"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if not PARETO_PATH.exists():
    raise FileNotFoundError(f"Missing ParetoDebug/ directory at {PARETO_PATH}")

# ========== ADAPTER INTERFACE ==========
from ParetoDebug.adapters.debug_adapter import (
    debug,
    get_debugger,
    generate_trace_id,
    debug_trace
)

# ========== DECORATED FUNCTION TEST ==========
@debug_trace(context="satellite/decorated_test")
def traced_example(x, y, trace_id=None):
    """Adds two numbers with debug_trace logging."""
    return x + y

# ========== MAIN RELAY ==========
def main():
    trace_id = generate_trace_id()
    dbg = get_debugger("satellite/launch")

    # 1. Context-bound debug log
    dbg(
        action="test_contextual_log",
        data={"tick": 0, "status": "satellite test"},
        ai_tags=["UI", "actor_data", "prototype", "runtime_behavior"],
        trace_id=trace_id,
        print_console=True
    )

    # 2. Global fallback debug log
    debug(
        action="test_fallback_log",
        data={"tick": 0, "source": "relay"},
        ai_tags=["UI", "actor_data", "mvp", "runtime_behavior"],
        print_console=True
    )

    # 3. Decorator-wrapped function call
    result = traced_example(7, 3, trace_id=trace_id)
    print(f"✅ Decorated function returned: {result}")


if __name__ == "__main__":
    main()
