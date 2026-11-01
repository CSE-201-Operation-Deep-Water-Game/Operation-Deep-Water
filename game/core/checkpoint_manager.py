"""CheckpointManager scaffolding from the class diagram."""

from __future__ import annotations


class CheckpointManager:
    """Scaffold for CheckpointManager from the class diagram."""

    def __init__(
        self,
        *,
        passwords: dict[str, int],
    ) -> None:
        self.passwords: dict[str, int] = passwords

    def award(self, levelIndex: int) -> str:
        """TODO: Implement award."""
        raise NotImplementedError("CheckpointManager.award is not implemented yet")

    def isValid(self, password: str) -> bool:
        """TODO: Implement isValid."""
        raise NotImplementedError("CheckpointManager.isValid is not implemented yet")

    def validate(self, password: str) -> int:
        """TODO: Implement validate."""
        raise NotImplementedError("CheckpointManager.validate is not implemented yet")
