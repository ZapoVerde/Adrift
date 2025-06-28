# generation.py

"""
TileGenerator is responsible for instantiating HexTiles into full terrain and features.

@ignore: stub — placeholder world tile generator with no output logic
"""

class TileGenerator:
    """
    Mock generator for terrain tile features. Currently returns static values.

    @ignore: inactive — not used by any system
    """
    def __init__(self, world_seed):
        self.world_seed = world_seed

    def generate_tile(self, tile, neighbors):
        """
        Populate a tile's biome, elevation, moisture, and features.

        @ignore
        """
        tile.biome_tag = self.sample_biome(tile, neighbors)
        tile.elevation = self.sample_elevation(tile, neighbors)
        tile.moisture = self.sample_moisture(tile, neighbors)
        tile.hinted_features = self.sample_features(tile, neighbors)
        return tile

    def sample_biome(self, tile, neighbors):
        """
        Stub biome sampler.

        @ignore
        """
        return "forest"

    def sample_elevation(self, tile, neighbors):
        """
        Stub elevation sampler.

        @ignore
        """
        return 0.5

    def sample_moisture(self, tile, neighbors):
        """
        Stub moisture sampler.

        @ignore
        """
        return 0.3

    def sample_features(self, tile, neighbors):
        """
        Stub feature generator.

        @ignore
        """
        return []
