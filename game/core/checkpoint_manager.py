from __future__ import annotations

class CheckpointManager:
    def __init__(
        self,
        *,
        passwords: dict[str, int],
    ) -> None:
        self.passwords: dict[str, int] = passwords

    def award(self, levelIndex: int) -> str | None:
        """Return the password for this level, if one is configured."""
        for password, index in self.passwords.items():
            if index == levelIndex:
                return password
        return None

    def isValid(self, password: str) -> bool:
        """Check if the password is valid."""
        return password.strip().upper() in self.passwords

    def validate(self, password: str) -> int:
        return self.passwords[password.strip().upper()]
