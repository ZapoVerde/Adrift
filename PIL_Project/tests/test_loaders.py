# test_loaders.py
import os
import sys
import inspect

# Allow relative import from PIL in project structure
here = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(here, '..'))
sys.path.insert(0, project_root)

from pil_meta.loaders.code_loader import load_code_symbols

def test_loader_finds_all_entities():
    """Ensure all entity types and metadata are found for a sample input file."""
    sample_file = os.path.join(here, "sample_input", "everything.py")
    symbols = load_code_symbols(sample_file)
    assert isinstance(symbols, list), "Loader did not return a list of symbols."

    # Confirm types present
    found_types = set(s["type"] for s in symbols)
    assert "function" in found_types, "Missing function type"
    assert "class" in found_types, "Missing class type"
    assert "method" in found_types, "Missing method type"
    assert "variable" in found_types, "Missing variable type"
    assert "module" in found_types, "Missing module type"

    # Required metadata on every symbol
    for sym in symbols:
        for field in ("fqname", "module", "type", "lineno"):
            assert field in sym, f"Missing {field} on symbol {sym}"

    # Check variable docstrings/comments are attached
    var = next((s for s in symbols if s["type"] == "variable" and s["name"] == "MY_CONSTANT"), None)
    assert var is not None, "MY_CONSTANT variable missing"
    assert "The answer to everything" in var.get("doc", ""), "Variable docstring missing"

    # Ensure private function is found
    assert any(s for s in symbols if s["name"] == "_private_function"), "Private function not detected"

    # Confirm docstring parsing for class/method/function
    assert any("top-level function" in s.get("doc", "") for s in symbols), "Function docstring missing"
    assert any("Class method doc" in s.get("doc", "") for s in symbols), "Method docstring missing"
    assert any("Static method doc" in s.get("doc", "") for s in symbols), "Static method docstring missing"
