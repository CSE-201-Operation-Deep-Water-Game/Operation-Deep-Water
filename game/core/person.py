from __future__ import annotations

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

    def getEnergy(self) -> int:
        return self.energyAmt

    def isDead(self) -> bool:
        return self.energyAmt <= 0

    def resetEnergy(self) -> None:
        self.energyAmt = self.maxEnergy
