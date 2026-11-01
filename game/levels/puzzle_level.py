"""PuzzleLevel scaffolding from the class diagram."""

from __future__ import annotations

from game.levels.level import Level

import game.core.person as person_module
import game.puzzles.puzzle as puzzle_module
import game.world.map as map_module


class PuzzleLevel(Level):
    """Scaffold for PuzzleLevel from the class diagram."""

    def __init__(
        self,
        *,
        name: str,
        map: map_module.Map,
        startX: int,
        startY: int,
        introText: str,
        complete: bool,
        puzzles: dict[str, puzzle_module.Puzzle],
        solvedOrder: list[str],
        validOrders: list[list[str]],
        wrongOrderCost: int,
    ) -> None:
        super().__init__(
            name=name,
            map=map,
            startX=startX,
            startY=startY,
            introText=introText,
            complete=complete,
        )
        self._puzzles: dict[str, puzzle_module.Puzzle] = puzzles
        self._solvedOrder: list[str] = solvedOrder
        self._validOrders: list[list[str]] = validOrders
        self._wrongOrderCost: int = wrongOrderCost

    def handleMove(self, person: person_module.Person, direction: str) -> str:
        """TODO: Implement handleMove."""
        raise NotImplementedError("PuzzleLevel.handleMove is not implemented yet")

    def interact(self, person: person_module.Person, puzzleId: str) -> str:
        """TODO: Implement interact."""
        raise NotImplementedError("PuzzleLevel.interact is not implemented yet")

    def recordSolved(self, puzzleId: str) -> None:
        """TODO: Implement recordSolved."""
        raise NotImplementedError("PuzzleLevel.recordSolved is not implemented yet")

    def checkOrder(self) -> bool:
        """TODO: Implement checkOrder."""
        raise NotImplementedError("PuzzleLevel.checkOrder is not implemented yet")

    def isStuck(self) -> bool:
        """TODO: Implement isStuck."""
        raise NotImplementedError("PuzzleLevel.isStuck is not implemented yet")
