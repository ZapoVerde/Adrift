# world/discovery.py

"""
Handles LocationStub logic and transformation into LocationInstance.
"""

class LocationStub:
    def __init__(self, type, faction, seed):
        self.type = type
        self.faction = faction
        self.seed = seed
        self.revealed = False
        self.rumor_hooks = []

    def reveal(self):
        self.revealed = True
        return self.instantiate()

    def instantiate(self):
        return LocationInstance(self.type, self.seed)


class LocationInstance:
    def __init__(self, type, seed):
        self.type = type
        self.seed = seed
        self.floorplan = None
        self.actors = []
        self.items = []
        self.environment = []

    def generate_floorplan(self):
        pass

    def teardown(self):
        pass
