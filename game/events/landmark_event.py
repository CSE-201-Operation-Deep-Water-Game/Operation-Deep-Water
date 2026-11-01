"""LandmarkEvent scaffolding from the class diagram."""

from __future__ import annotations

from game.events.base_event import BaseEvent

import game.core.person as person_module
import game.levels.level as level_module


class LandmarkEvent(BaseEvent):
    """Scaffold for LandmarkEvent from the class diagram."""

    def __init__(
        self,
        *,
        name: str,
        description: str,
        isRepeatable: bool,
        hasBeenTriggered: bool,
        landmarkText: str,
    ) -> None:
        super().__init__(
            name=name,
            description=description,
            isRepeatable=isRepeatable,
            hasBeenTriggered=hasBeenTriggered,
        )
        self.landmarkText: str = landmarkText

    def play(self, person: person_module.Person, level: level_module.Level) -> str:
        """TODO: Implement play."""
        raise NotImplementedError("LandmarkEvent.play is not implemented yet")
