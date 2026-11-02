from game.events.base_event import BaseEvent

import game.core.person as person_module
import game.levels.level as level_module


class WallEvent(BaseEvent):
    def __init__(
        self,
        *,
        name: str,
        description: str,
        isRepeatable: bool,
        hasBeenTriggered: bool,
        blockMessage: str,
        energyPenalty: int,
    ) -> None:
        super().__init__(
            name=name,
            description=description,
            isRepeatable=isRepeatable,
            hasBeenTriggered=hasBeenTriggered,
        )
        self.blockMessage: str = blockMessage
        self.energyPenalty: int = energyPenalty

    def play(self, person: person_module.Person, level: level_module.Level) -> str:
        """TODO: Implement play."""
        raise NotImplementedError("WallEvent.play is not implemented yet")
