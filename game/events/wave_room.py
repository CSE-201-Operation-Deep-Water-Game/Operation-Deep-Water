"""WaveRoom scaffolding from the class diagram."""

from __future__ import annotations

from game.events.base_event import BaseEvent

import game.core.person as person_module
import game.levels.level as level_module


class WaveRoom(BaseEvent):
    """Scaffold for WaveRoom from the class diagram."""

    def __init__(
        self,
        *,
        name: str,
        description: str,
        isRepeatable: bool,
        hasBeenTriggered: bool,
        direction: str,
        strength: int,
    ) -> None:
        super().__init__(
            name=name,
            description=description,
            isRepeatable=isRepeatable,
            hasBeenTriggered=hasBeenTriggered,
        )
        self.direction: str = direction
        self.strength: int = strength

    def play(self, person: person_module.Person, level: level_module.Level) -> str:
        """TODO: Implement play."""
        raise NotImplementedError("WaveRoom.play is not implemented yet")

    def getPush(self) -> tuple[int, int]:
        """TODO: Implement getPush."""
        raise NotImplementedError("WaveRoom.getPush is not implemented yet")
