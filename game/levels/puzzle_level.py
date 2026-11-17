from __future__ import annotations

from game.levels.level import Level

import game.core.person as person_module
import game.world.map as map_module


class PuzzleLevel(Level):
    """Sonar at the crossing of four landmarks unseals the exit."""

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
        exitX: int = 0,
        exitY: int = 0,
        rechargeLandmarks: bool = False,
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
        self.exitX = exitX
        self.exitY = exitY
        self.rechargeLandmarks = rechargeLandmarks
        self.usedPowerCells: set[tuple[int, int]] = set()
        self.lockedExitDescription = self.map.getTile(exitX, exitY).getDescription()

    def start(self, person: person_module.Person) -> str:
        self.solved = False
        self.usedPowerCells.clear()
        self.map.getTile(self.exitX, self.exitY).tileType = "wall"
        self.map.getTile(self.exitX, self.exitY).description = self.lockedExitDescription
        return super().start(person)

    def handleMove(self, person: person_module.Person, direction: str) -> str:
        invalidMoveResponse = self.validateMove(person, direction)
        if direction in self.DIRECTIONS:
            person.decreaseEnergy(1)
        if invalidMoveResponse:
            return invalidMoveResponse

        dx, dy = self.DIRECTIONS[direction]
        x, y = person.positionX + dx, person.positionY + dy
        person.setPosition(x, y)
        tile = self.map.getTile(x, y)

        if tile.tileType == "exit":
            self.markComplete()
            return "You reached the exit."
        
        message = "You moved." + (f" {tile.getDescription()}" if tile.getDescription() else "")
        if self.rechargeLandmarks and tile.landmark and (x, y) not in self.usedPowerCells:
            self.usedPowerCells.add((x, y))
            person.resetEnergy()
            message += " You connect the relic's survey power cell. Energy restored; the cell is now empty."
        return message

    def onSonar(self, person: person_module.Person) -> str:
        if self.solved:
            return "The exit is already open."
        if self.isAtIntersection(person):
            message = self.unlockEntrance()
            self.solved = True
            return message
        return "The pulse fades. The sealed exit remains silent."

    def isAtIntersection(self, person: person_module.Person) -> bool:
        return person.positionX == self.intersectionX and person.positionY == self.intersectionY

    def unlockEntrance(self) -> str:
        tile = self.map.getTile(self.exitX, self.exitY)
        tile.tileType = "exit"
        return "Your sonar wakes a buried resonator. Four notes converge beneath you and the stone iris rumbles open. The exit is unlocked."
