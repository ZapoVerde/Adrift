# hex.py

"""
Handles HexTile definitions and lazy generation scaffolding.
"""

class HexTile:
    """
    Represents a single tile in the axial world coordinate system (q, r).
    Intended to serve as a foundational unit in overworld travel and terrain logic.

    Fields:
    - q, r: axial coordinates
    - seed: tile-specific generation seed
    - biome_tag, elevation, moisture: terrain properties
    - terrain_tags: arbitrary feature tags
    - hinted_features: placeholder for future map features
    - location_stub: optional undiscovered structure reference
    - faction_influence_estimates: placeholder for strategic layer
    """
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
        """
        Generate a unique integer seed based on tile coordinates.

        Returns:
            int: reproducible seed based on (q, r)
        """
        return hash((self.q, self.r))

    def coord(self):
        """
        Return the axial coordinates of this tile.

        Returns:
            tuple[int, int]: (q, r)
        """
        return (self.q, self.r)