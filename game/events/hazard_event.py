"""HazardEvent scaffolding from the class diagram."""

from __future__ import annotations

from game.events.base_event import BaseEvent

import game.core.person as person_module
import game.levels.level as level_module


class HazardEvent(BaseEvent):
    """Scaffold for HazardEvent from the class diagram."""

    def __init__(
        self,
        *,
        name: str,
        description: str,
        isRepeatable: bool,
        hasBeenTriggered: bool,
        damage: int,
        crashMessage: str,
    ) -> None:
        super().__init__(
            name=name,
            description=description,
            isRepeatable=isRepeatable,
            hasBeenTriggered=hasBeenTriggered,
        )
        self._damage: int = damage
        self._crashMessage: str = crashMessage

    def play(self, person: person_module.Person, level: level_module.Level) -> str:
        """TODO: Implement play."""
        raise NotImplementedError("HazardEvent.play is not implemented yet")
