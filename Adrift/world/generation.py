# world/generation.py

"""
TileGenerator is responsible for instantiating HexTiles into full terrain and features.
"""

class TileGenerator:
    def __init__(self, world_seed):
        self.world_seed = world_seed

    def generate_tile(self, tile, neighbors):
        tile.biome_tag = self.sample_biome(tile, neighbors)
        tile.elevation = self.sample_elevation(tile, neighbors)
        tile.moisture = self.sample_moisture(tile, neighbors)
        tile.hinted_features = self.sample_features(tile, neighbors)
        return tile

    def sample_biome(self, tile, neighbors):
        return "forest"

    def sample_elevation(self, tile, neighbors):
        return 0.5

    def sample_moisture(self, tile, neighbors):
        return 0.3

    def sample_features(self, tile, neighbors):
        return []
