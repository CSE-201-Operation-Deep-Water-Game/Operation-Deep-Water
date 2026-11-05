from __future__ import annotations

from game.levels.level import Level

import game.core.person as person_module
import game.world.map as map_module


class CurrentLevel(Level):
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
        super().__init__(
            name=name,
            map=map,
            startX=startX,
            startY=startY,
            introText=introText,
            complete=complete,
        )

    def handleMove(self, person: person_module.Person, direction: str) -> str:
        """TODO: Implement handleMove."""
        raise NotImplementedError("CurrentLevel.handleMove is not implemented yet")

    def applyCurrent(self, person: person_module.Person) -> str:
        """TODO: Implement applyCurrent."""
        raise NotImplementedError("CurrentLevel.applyCurrent is not implemented yet")
