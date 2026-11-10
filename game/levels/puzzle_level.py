from __future__ import annotations

from game.levels.level import Level

import game.core.person as person_module
import game.world.map as map_module
from game.world.tile import Tile


class PuzzleLevel(Level):
    """Four landmarks form an X; sonar at its intersection unlocks an entrance."""

    def __init__(
        self,
        *,
        name: str,
        map: map_module.Map,
        startX: int,
        startY: int,
        introText: str,
        complete: bool,
        intersectionX: int,
        intersectionY: int,
    ) -> None:
        super().__init__(
            name=name,
            map=map,
            startX=startX,
            startY=startY,
            introText=introText,
            complete=complete,
        )
        self.intersectionX: int = intersectionX
        self.intersectionY: int = intersectionY
        self.solved: bool = False

    def start(self, person: person_module.Person) -> str:
        """TODO: Reset puzzle state and start the level."""
        raise NotImplementedError("PuzzleLevel.start is not implemented yet")

    def handleMove(self, person: person_module.Person, direction: str) -> str:
        """TODO: Implement handleMove."""
        raise NotImplementedError("PuzzleLevel.handleMove is not implemented yet")

    def onSonar(self, person: person_module.Person) -> str:
        if self.isAtIntersection(person):
            self.unlockEntrance()
            self.solved = True

    def isAtIntersection(self, person: person_module.Person) -> bool:
        return person.positionX == self.intersectionX and person.positionY == self.intersectionY

    def unlockEntrance(self) -> str:
        self.map.setTile(0, 0, Tile(x=0, y=0, tileType="open", landmark=""))
        return "After the sonar pulse is sent out, you hear a low rumbling sound outside, it seems something has shifted in the maze"
