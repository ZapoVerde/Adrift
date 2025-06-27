# Adrift/test/conftest.py

import pytest
from lint.check_docstrings import scan_project

def test_docstring_format():
    violations = scan_project()
    assert not violations, "Some functions are missing or misformatted docstrings"
