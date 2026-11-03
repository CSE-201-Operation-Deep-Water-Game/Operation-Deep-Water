from __future__ import annotations

import game.world.map as map_module


class Puzzle:
    def __init__(
        self,
        *,
        puzzleId: str,
        description: str,
        solution: str,
        solved: bool,
        mapChanges: list[tuple[int, int, str]],
    ) -> None:
        self.puzzleId: str = puzzleId
        self.description: str = description
        self.solution: str = solution
        self.solved: bool = solved
        self.mapChanges: list[tuple[int, int, str]] = mapChanges

    def attempt(self, input: str) -> bool:
        """TODO: Implement attempt."""
        raise NotImplementedError("Puzzle.attempt is not implemented yet")

    def isSolved(self) -> bool:
        """TODO: Implement isSolved."""
        raise NotImplementedError("Puzzle.isSolved is not implemented yet")

    def applyEffect(self, map: map_module.Map) -> str:
        """TODO: Implement applyEffect."""
        raise NotImplementedError("Puzzle.applyEffect is not implemented yet")

    def getDescription(self) -> str:
        """TODO: Implement getDescription."""
        raise NotImplementedError("Puzzle.getDescription is not implemented yet")
