# test/test_floorplan_parser.py

from pprint import pprint

def parse_layout(layout_str):
    SYMBOL_TABLE = {
        "#": lambda: {
            "terrain": "stone",
            "things": [{"type": "wall", "blocks_movement": True, "blocks_los": True}],
        },
        ".": lambda: {"terrain": "stone", "things": []},
        " ": lambda: {"terrain": "void", "things": []},
        "@": lambda: {
            "terrain": "stone",
            "things": [],
            "actor": {"type": "player", "name": "You"},
        },
        "g": lambda: {
            "terrain": "stone",
            "things": [],
            "actor": {"type": "goblin", "name": "Goblin Grunt"},
        },
        "C": lambda: {
            "terrain": "stone",
            "things": [{"type": "crate", "cover": "partial", "destructible": True}],
        },
        "F": lambda: {
            "terrain": "stone",
            "things": [],
            "env": [{"type": "fire", "duration": 3}],
        },
        "+": lambda: {
            "terrain": "stone",
            "things": [{"type": "door", "state": "closed", "blocks_los": True, "blocks_movement": True}],
        },
    }

    lines = layout_str.strip("\n").splitlines()
    height = len(lines)
    width = max(len(line) for line in lines)

    floorplan = {
        "id": "test_map",
        "width": width,
        "height": height,
        "seed": 12345,
        "metadata": {"label": "Test Layout"},
        "tiles": {},
    }

    for y, line in enumerate(lines):
        for x, char in enumerate(line.ljust(width)):
            base_tile = {
                "terrain": "stone",
                "things": [],
                "items": [],
                "env": [],
                "actor": None,
                "light": 1.0,
                "memory": "unseen",
                "zone": None,
            }
            parser = SYMBOL_TABLE.get(char, SYMBOL_TABLE["."])
            updates = parser()
            tile = {**base_tile, **updates}
            floorplan["tiles"][(x, y)] = tile

    return floorplan


def render_ascii_map(floorplan):
    symbols = {
        "wall": "#",
        "crate": "C",
        "door": "+",
        "brazier": "B",
        "fire": "F",
        "player": "@",
        "goblin": "g",
        "floor": ".",
        "void": " ",
    }

    width = floorplan["width"]
    height = floorplan["height"]
    tiles = floorplan["tiles"]

    for y in range(height):
        row = ""
        for x in range(width):
            tile = tiles.get((x, y), {})
            if not tile:
                row += " "
                continue

            if tile["actor"]:
                row += symbols.get(tile["actor"]["type"], "?")
            elif tile["env"]:
                row += symbols.get(tile["env"][0]["type"], "F")
            elif tile["things"]:
                row += symbols.get(tile["things"][0]["type"], "?")
            elif tile["terrain"] == "void":
                row += " "
            else:
                row += "."
        print(row)


if __name__ == "__main__":
    layout = """
##################
#............... #
#....C..g....... #
#............... #
#....@.......... #
##################
"""
    floorplan = parse_layout(layout)
    render_ascii_map(floorplan)
