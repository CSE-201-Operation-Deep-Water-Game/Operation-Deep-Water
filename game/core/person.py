"""Person scaffolding from the class diagram."""

from __future__ import annotations


class Person:
    """Scaffold for Person from the class diagram."""

    def __init__(
        self,
        *,
        energyAmt: int,
        maxEnergy: int,
        positionX: int,
        positionY: int,
    ) -> None:
        self._energyAmt: int = energyAmt
        self._maxEnergy: int = maxEnergy
        self._positionX: int = positionX
        self._positionY: int = positionY

    def move(self, dx: int, dy: int) -> None:
        """TODO: Implement move."""
        raise NotImplementedError("Person.move is not implemented yet")

    def setPosition(self, x: int, y: int) -> None:
        """TODO: Implement setPosition."""
        raise NotImplementedError("Person.setPosition is not implemented yet")

    def getPosition(self) -> tuple[int, int]:
        """TODO: Implement getPosition."""
        raise NotImplementedError("Person.getPosition is not implemented yet")

    def decreaseEnergy(self, amount: int) -> None:
        """TODO: Implement decreaseEnergy."""
        raise NotImplementedError("Person.decreaseEnergy is not implemented yet")

    def getEnergy(self) -> int:
        """TODO: Implement getEnergy."""
        raise NotImplementedError("Person.getEnergy is not implemented yet")

    def isDead(self) -> bool:
        """TODO: Implement isDead."""
        raise NotImplementedError("Person.isDead is not implemented yet")

    def resetEnergy(self) -> None:
        """TODO: Implement resetEnergy."""
        raise NotImplementedError("Person.resetEnergy is not implemented yet")
