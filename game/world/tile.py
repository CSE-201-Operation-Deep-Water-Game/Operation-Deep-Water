"""Tile scaffolding from the class diagram."""

from __future__ import annotations


import game.core.person as person_module
import game.events.base_event as base_event_module
import game.levels.level as level_module


class Tile:
    """Scaffold for Tile from the class diagram."""

    def __init__(
        self,
        *,
        x: int,
        y: int,
        tileType: str,
        event: base_event_module.BaseEvent | None,
        landmark: str,
    ) -> None:
        self.x: int = x
        self.y: int = y
        self.tileType: str = tileType
        self.event: base_event_module.BaseEvent | None = event
        self.landmark: str = landmark

    def isPassable(self) -> bool:
        """TODO: Implement isPassable."""
        raise NotImplementedError("Tile.isPassable is not implemented yet")

    def setType(self, tileType: str) -> None:
        """TODO: Implement setType."""
        raise NotImplementedError("Tile.setType is not implemented yet")

    def setEvent(self, event: base_event_module.BaseEvent) -> None:
        """TODO: Implement setEvent."""
        raise NotImplementedError("Tile.setEvent is not implemented yet")

    def getDescription(self) -> str:
        """TODO: Implement getDescription."""
        raise NotImplementedError("Tile.getDescription is not implemented yet")

    def trigger(self, person: person_module.Person, level: level_module.Level) -> str:
        """TODO: Implement trigger."""
        raise NotImplementedError("Tile.trigger is not implemented yet")
