from __future__ import annotations

import threading
from time import monotonic

from game.levels.level import Level

import game.core.person as person_module
import game.world.map as map_module


class FinalLevel(Level):
    CHASE_SECONDS = 30

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
        isTimerOver: bool,
        timer: threading.Timer

    ) -> None:
        super().__init__(
            name=name,
            map=map,
            startX=startX,
            startY=startY,
            introText=introText,
            complete=complete,
        )
        self.timer = None
        self.isTimerOver = False
        self.isTimerStarted = False
        self.artifactX: int = artifactX
        self.artifactY: int = artifactY
        self.hasArtifact = False


    def start(self, person: person_module.Person) -> str:
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None

        self.isTimerOver = False
        self.isTimerStarted = False
        self.hasArtifact = False
        return super().start(person)

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

        description = tile.getDescription()
        message = f"You moved. {description}" if description else "You moved."
        if (x, y) == self.getArtifactPosition() and not self.hasArtifact:
            message += f"\n{self.grabArtifact()}"

        return message

    def grabArtifact(self) -> str:
        self.hasArtifact = True
        return "You grab the NAYRB and secure it inside the submarine."

    def getArtifactPosition(self) -> tuple[int, int]:
        return self.artifactX, self.artifactY

    def onTimerEnd(self) -> None:
        self.isTimerOver = True

    def startTimer(self) -> None:
        if self.timer is not None:
            self.timer.cancel()

        self.isTimerOver = False
        self.isTimerStarted = True
        self.timer = threading.Timer(self.CHASE_SECONDS, self.onTimerEnd)
        self.timer.start()
