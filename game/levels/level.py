from __future__ import annotations

from abc import ABC, abstractmethod

import game.core.person as person_module
import game.world.map as map_module


class Level(ABC):
    DIRECTIONS: dict[str, tuple[int, int]] = {
        "up": (0, 1), "down": (0, -1),
        "left": (-1, 0), "right": (1, 0),
    }

    def __init__(
        self,
        *,
        name: str,
        map: map_module.Map,
        startX: int,
        startY: int,
        introText: str,
        complete: bool,
    ) -> None:
        self.name: str = name
        self.map: map_module.Map = map
        self.startX: int = startX
        self.startY: int = startY
        self.introText: str = introText
        self.complete: bool = complete

    def start(self, person: person_module.Person) -> str:
        person.setPosition(self.startX, self.startY)
        self.complete = False
        return self.introText

    @abstractmethod
    def handleMove(self, person: person_module.Person, direction: str) -> str:
        """TODO: Implement handleMove."""
        raise NotImplementedError("Level.handleMove is not implemented yet")

    def isComplete(self) -> bool:
        return self.complete

    def onSonar(self, person: person_module.Person) -> str:
        """React to a sonar pulse from the player's current position."""
        return ""

    def validateMove(self, person: person_module.Person, direction: str) -> str:
        """Return an error, or an empty string, without changing player state."""
        if direction not in self.DIRECTIONS:
            return "Invalid direction."

        dx, dy = self.DIRECTIONS[direction]
        x, y = person.positionX + dx, person.positionY + dy

        if not self.map.inBounds(x, y):
            return "You bumped into a wall."

        tile = self.map.getTile(x, y)
        if not tile.isPassable():
            message = "You bumped into a wall."
            if tile.getDescription():
                message += f" {tile.getDescription()}"
            return message

        return ""

    def markComplete(self) -> None:
        self.complete = True
