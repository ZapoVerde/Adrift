# definitions/map.py

# LEGACY MODULE
# This file is deprecated under the new world+tactical architecture.
# It is retained only for reference and should not be imported or modified.
raise ImportError("This module is deprecated and should not be used.")
# ─────────────────────────────────────────────────────────────
# 🧠 ROLE: Represents the full dungeon map for a floor/level.
# Contains all Rooms in a dictionary and tracks the current room.
#
# 🚪 Maps control room transitions, travel validation,
# and global traversal logic.
#
# 📦 STRUCTURE:
# - Contains many Room objects
# - Tracks current_room (where player is)
# ─────────────────────────────────────────────────────────────

from Adrift.definitions.room import Room

class Map:
    def __init__(self, rooms: list[Room]):
        self.rooms = {room.internal_name: room for room in rooms}
        self.current_room = None  # Set via set_starting_room()

    def get_room(self, internal_name: str) -> Room:
        """
        Returns a Room object by its internal name.
        """
        return self.rooms.get(internal_name)

    def set_starting_room(self, internal_name: str):
        """
        Sets the initial room when the map is first loaded.
        """
        self.current_room = self.rooms.get(internal_name)

    def move_to_room(self, internal_name: str):
        """
        Moves the current room pointer to a new room.
        Assumes caller has validated that the move is allowed.
        """
        if internal_name in self.rooms:
            self.current_room = self.rooms[internal_name]
