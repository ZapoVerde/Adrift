# tests/test_thing_definitions.py

from Adrift.definitions.thing import THING_DB

def test_things_have_required_fields():
    for key, thing in THING_DB.items():
        assert isinstance(thing, dict), f"{key} is not a dict"

        assert "blocks_sight" in thing, f"{key} missing 'blocks_sight'"
        assert isinstance(thing["blocks_sight"], bool), f"{key} 'blocks_sight' must be bool"

        assert "cover_rating" in thing, f"{key} missing 'cover_rating'"
        assert isinstance(thing["cover_rating"], int), f"{key} 'cover_rating' must be int"

        assert "destructible" in thing, f"{key} missing 'destructible'"
        assert isinstance(thing["destructible"], bool), f"{key} 'destructible' must be bool"

        if thing["destructible"]:
            assert "hp" in thing, f"{key} is destructible but missing 'hp'"
            assert isinstance(thing["hp"], int), f"{key} 'hp' must be int if destructible"
