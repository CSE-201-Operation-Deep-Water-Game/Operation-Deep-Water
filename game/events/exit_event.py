from __future__ import annotations

from game.events.base_event import BaseEvent

import game.core.person as person_module
import game.levels.level as level_module


class ExitEvent(BaseEvent):
    def __init__(
        self,
        *,
        name: str,
        description: str,
        isRepeatable: bool,
        hasBeenTriggered: bool,
        levelIndex: int,
        successText: str,
    ) -> None:
        super().__init__(
            name=name,
            description=description,
            isRepeatable=isRepeatable,
            hasBeenTriggered=hasBeenTriggered,
        )
        self.levelIndex: int = levelIndex
        self.successText: str = successText

    def play(self, person: person_module.Person, level: level_module.Level) -> str:
        """Complete the current level and return the exit message."""
        level.markComplete()
        self.hasBeenTriggered = True
        return self.successText
