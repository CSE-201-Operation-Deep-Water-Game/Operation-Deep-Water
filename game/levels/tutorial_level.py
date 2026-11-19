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
        invalidMoveResponse = self.validateMove(person, direction)
        if direction in self.DIRECTIONS:
            person.decreaseEnergy(1)
        if invalidMoveResponse:
            return invalidMoveResponse

        dx, dy = self.DIRECTIONS[direction]
        x, y = person.positionX + dx, person.positionY + dy
        person.setPosition(x, y)
        destination = self.map.getTile(x, y)

        if destination.tileType == "exit":
            self.markComplete()
            return "You reached the exit."

        if destination.getDescription():
            return f"You moved. {destination.getDescription()}"

        return "You moved."