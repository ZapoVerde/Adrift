# test_function_map_utils.py
# Tests for core utility functions used in generate_function_map.py

import pytest
import os
from scripts.generate_function_map import (
    extract_subsystem_tags,
    infer_path_based_subsystem,
    extract_functions_from_file,
)


# ------------------
# 🧪 extract_subsystem_tags
# ------------------

@pytest.mark.parametrize("docstring,expected", [
    ("""@subsystem:combat""", ["combat"]),
    ("""Some description\n@subsystem:mutation\nOther info""", ["mutation"]),
    ("""@subsystem:vision\n@subsystem:ai""", ["vision", "ai"]),
    ("""No tags here""", []),
    (None, []),
])
def test_extract_subsystem_tags(docstring, expected):
    assert extract_subsystem_tags(docstring) == expected


# ------------------
# 🧪 infer_path_based_subsystem
# ------------------

def test_infer_path_based_subsystem_valid():
    path = os.path.join("Adrift", "combat", "foo.py")
    assert infer_path_based_subsystem(path, "Adrift") == "combat"

def test_infer_path_based_subsystem_invalid():
    path = os.path.join("external", "other.py")
    assert infer_path_based_subsystem(path, "Adrift") is None


# ------------------
# 🧪 extract_functions_from_file (minimal real test)
# ------------------

def test_extract_functions_from_file(tmp_path):
    test_code = '''
    def foo():
        """This is foo.\n@subsystem:test"""
        pass

    def bar():
        pass
    '''
    test_file = tmp_path / "Adrift" / "test_module.py"
    test_file.parent.mkdir(parents=True)
    test_file.write_text(test_code)

    funcs = extract_functions_from_file(str(test_file), str(tmp_path))
    names = [f["function"] for f in funcs]
    subsystems = [f["subsystems"] for f in funcs]

    assert "foo" in names
    assert "bar" in names
    assert any("test" in group for group in subsystems)
