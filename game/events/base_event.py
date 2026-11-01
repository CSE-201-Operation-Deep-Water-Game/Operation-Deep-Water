"""BaseEvent scaffolding from the class diagram."""

from __future__ import annotations

from abc import ABC, abstractmethod

import game.core.person as person_module
import game.levels.level as level_module


class BaseEvent(ABC):
    """Scaffold for BaseEvent from the class diagram."""

    def __init__(
        self,
        *,
        name: str,
        description: str,
        isRepeatable: bool,
        hasBeenTriggered: bool,
    ) -> None:
        self._name: str = name
        self._description: str = description
        self._isRepeatable: bool = isRepeatable
        self._hasBeenTriggered: bool = hasBeenTriggered

    @abstractmethod
    def play(self, person: person_module.Person, level: level_module.Level) -> str:
        """TODO: Implement play."""
        raise NotImplementedError("BaseEvent.play is not implemented yet")

    def getDescription(self) -> str:
        """TODO: Implement getDescription."""
        raise NotImplementedError("BaseEvent.getDescription is not implemented yet")

    def canTrigger(self) -> bool:
        """TODO: Implement canTrigger."""
        raise NotImplementedError("BaseEvent.canTrigger is not implemented yet")
