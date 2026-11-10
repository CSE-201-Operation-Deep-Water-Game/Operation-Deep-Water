from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import game.world.map as map_module

class Person:
    def __init__(
        self,
        *,
        energyAmt: int,
        maxEnergy: int,
        positionX: int,
        positionY: int,
    ) -> None:
        self.energyAmt: int = energyAmt
        self.maxEnergy: int = maxEnergy
        self.positionX: int = positionX
        self.positionY: int = positionY

    def setPosition(self, x: int, y: int) -> None:
        self.positionX = x
        self.positionY = y

    def getPosition(self) -> tuple[int, int]:
        return self.positionX, self.positionY

    def decreaseEnergy(self, amount: int) -> None:
        self.energyAmt -= amount

    def sonar(self, map: map_module.Map, arg: str) -> str:
        surroundings = map.sonar(self, arg)
        self.decreaseEnergy(5)
        return surroundings

    def getEnergy(self) -> int:
        return self.energyAmt

    def isDead(self) -> bool:
        return self.energyAmt <= 0

    def resetEnergy(self) -> None:
        self.energyAmt = self.maxEnergy
