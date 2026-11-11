from __future__ import annotations

from game.levels.level import Level

import game.core.person as person_module
import game.world.map as map_module


class TutorialLevel(Level):
    def __init__(
        self,
        *,
        name: str,
        map: map_module.Map,
        startX: int,
        startY: int,
        introText: str,
        complete: bool,
        hints: list[str],
    ) -> None:
        super().__init__(
            name=name,
            map=map,
            startX=startX,
            startY=startY,
            introText=introText,
            complete=complete,
        )
        self.hints: list[str] = hints

    def handleMove(self, person: person_module.Person, direction: str) -> str:
        """Handles player movement
        Args:
            person (person_module.Person): person to move
            direction (str): direction to move

        :return str: message returned from player movement.
            """
        directions = {
            "up": (0, 1),
            "down": (0, -1),
            "left": (-1, 0),
            "right": (1, 0),
        }
        if direction not in directions:
            return "Invalid direction."

        dx, dy = directions[direction]
        x, y = person.positionX + dx, person.positionY + dy
        if not self.map.inBounds(x, y):
            person.decreaseEnergy(1)
            return "You bumped into a wall."

        destination = self.map.getTile(x, y)
        if not destination.isPassable():
            person.decreaseEnergy(1)
            message = "You bumped into a wall."
            if destination.getDescription():
                message += f" {destination.getDescription()}"
            return message

        person.setPosition(x, y)
        person.decreaseEnergy(1)

        if destination.tileType == "exit":
            self.markComplete()
            return "You reached the exit."

        if destination.getDescription():
            return f"You moved. {destination.getDescription()}"

        return "You moved."


    def getHint(self) -> str:
        """TODO: Implement getHint."""
        raise NotImplementedError("TutorialLevel.getHint is not implemented yet")
