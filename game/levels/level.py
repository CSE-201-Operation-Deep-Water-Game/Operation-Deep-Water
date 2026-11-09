from __future__ import annotations

from abc import ABC, abstractmethod

import game.core.person as person_module
import game.world.map as map_module


class Level(ABC):
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
        self.name: str = name
        self.map: map_module.Map = map
        self.startX: int = startX
        self.startY: int = startY
        self.introText: str = introText
        self.complete: bool = complete

    def start(self, person: person_module.Person) -> str:
        person.setPosition(self.startX, self.startY)
        self.complete = False
        return self.introText

    @abstractmethod
    def handleMove(self, person: person_module.Person, direction: str) -> str:
        """TODO: Implement handleMove."""
        raise NotImplementedError("Level.handleMove is not implemented yet")

    def isComplete(self) -> bool:
        return self.complete

    def markComplete(self) -> None:
        self.complete = True
