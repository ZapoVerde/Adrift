# world/hex.py

"""
Handles HexTile definitions and lazy generation scaffolding.
"""

class HexTile:
    def __init__(self, q, r, seed=None):
        self.q = q
        self.r = r
        self.seed = seed or self.generate_seed()
        self.biome_tag = None
        self.elevation = None
        self.moisture = None
        self.terrain_tags = []
        self.hinted_features = []
        self.location_stub = None
        self.faction_influence_estimates = {}

    def generate_seed(self):
        return hash((self.q, self.r))

    def coord(self):
        return (self.q, self.r)
