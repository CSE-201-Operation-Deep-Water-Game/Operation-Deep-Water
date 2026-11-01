"""TutorialLevel scaffolding from the class diagram."""

from __future__ import annotations

from game.levels.level import Level

import game.core.person as person_module
import game.world.map as map_module


class TutorialLevel(Level):
    """Scaffold for TutorialLevel from the class diagram."""

    def __init__(
        self,
        *,
        name: str,
        map: map_module.Map,
        startX: int,
        startY: int,
        introText: str,
        complete: bool,
        hints: list[str],
    ) -> None:
        super().__init__(
            name=name,
            map=map,
            startX=startX,
            startY=startY,
            introText=introText,
            complete=complete,
        )
        self._hints: list[str] = hints

    def handleMove(self, person: person_module.Person, direction: str) -> str:
        """TODO: Implement handleMove."""
        raise NotImplementedError("TutorialLevel.handleMove is not implemented yet")

    def getHint(self) -> str:
        """TODO: Implement getHint."""
        raise NotImplementedError("TutorialLevel.getHint is not implemented yet")
