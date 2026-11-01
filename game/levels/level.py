"""Level scaffolding from the class diagram."""

from __future__ import annotations

from abc import ABC, abstractmethod

import game.core.person as person_module
import game.world.map as map_module


class Level(ABC):
    """Scaffold for Level from the class diagram."""

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
        self._name: str = name
        self._map: map_module.Map = map
        self._startX: int = startX
        self._startY: int = startY
        self._introText: str = introText
        self._complete: bool = complete

    def start(self, person: person_module.Person) -> str:
        """TODO: Implement start."""
        raise NotImplementedError("Level.start is not implemented yet")

    @abstractmethod
    def handleMove(self, person: person_module.Person, direction: str) -> str:
        """TODO: Implement handleMove."""
        raise NotImplementedError("Level.handleMove is not implemented yet")

    def describe(self, person: person_module.Person) -> str:
        """TODO: Implement describe."""
        raise NotImplementedError("Level.describe is not implemented yet")

    def isComplete(self) -> bool:
        """TODO: Implement isComplete."""
        raise NotImplementedError("Level.isComplete is not implemented yet")

    def markComplete(self) -> None:
        """TODO: Implement markComplete."""
        raise NotImplementedError("Level.markComplete is not implemented yet")

    def reset(self, person: person_module.Person) -> None:
        """TODO: Implement reset."""
        raise NotImplementedError("Level.reset is not implemented yet")
