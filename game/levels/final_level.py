from __future__ import annotations

from operator import truediv

from game.levels.level import Level

import game.core.person as person_module
import game.world.map as map_module
import threading


class FinalLevel(Level):
    def __init__(
        self,
        *,
        name: str,
        map: map_module.Map,
        startX: int,
        startY: int,
        introText: str,
        complete: bool,
        artifactX: int,
        artifactY: int,
        isTimerStarted: bool,
        isTimerOver: bool
    ) -> None:
        super().__init__(
            name=name,
            map=map,
            startX=startX,
            startY=startY,
            introText=introText,
            complete=complete,
        )
        self.isTimerOver = False
        self.isTimerStarted = True
        self.artifactX: int = artifactX
        self.artifactY: int = artifactY


    def handleMove(self, person: person_module.Person, direction: str) -> str:
        if not self.isTimerStarted:
            self.startTimer()

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

    def getArtifactPosition(self) -> tuple[int, int]:
        return self.artifactX, self.artifactY

    def on_timer_end(self):
        self.isTimerOver = True

    def startTimer(self):
        timer = threading.Timer(5.0, self.on_timer_end)
        timer.start()
        self.isTimerStarted = True


