"""ArtifactEvent scaffolding from the class diagram."""

from __future__ import annotations

from game.events.base_event import BaseEvent

import game.core.person as person_module
import game.levels.level as level_module


class ArtifactEvent(BaseEvent):
    """Scaffold for ArtifactEvent from the class diagram."""

    def __init__(
        self,
        *,
        name: str,
        description: str,
        isRepeatable: bool,
        hasBeenTriggered: bool,
        endingText: str,
    ) -> None:
        super().__init__(
            name=name,
            description=description,
            isRepeatable=isRepeatable,
            hasBeenTriggered=hasBeenTriggered,
        )
        self._endingText: str = endingText

    def play(self, person: person_module.Person, level: level_module.Level) -> str:
        """TODO: Implement play."""
        raise NotImplementedError("ArtifactEvent.play is not implemented yet")
