# test_tag_validation.py
# Verifies that all tags used in definitions are valid against TAG_DB.

from Adrift.definitions import skill_defs, technique_defs
from Adrift.utils.general_utils import validate_all_tags


def test_all_tags_are_valid():
    """
    Runs tag validation across all tagged definitions.
    Fails if any tag is not found in TAG_DB.
    """
    validate_all_tags(skill_defs.SKILL_DB, technique_defs.TECHNIQUE_DB)
