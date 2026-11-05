from __future__ import annotations

import game.commands.command as command_module


class CommandParser:
    def __init__(
        self,
        *,
        validVerbs: dict[str, str],
    ) -> None:
        self.validVerbs: dict[str, str] = validVerbs

    DIRECTIONS = {"up", "down", "left", "right"}

    def parse(self, raw: str) -> command_module.Command:
        if not self.isValid(raw):
            raise ValueError("Enter a recognized command.")

        parts = raw.strip().split(maxsplit=1)
        first = parts[0].lower()

        if first in self.DIRECTIONS:
            return command_module.Command(verb="move", arg=first)

        verb = self.validVerbs[first]
        arg = parts[1] if len(parts) > 1 else ""

        if verb == "move":
            arg = arg.lower()

        return command_module.Command(verb=verb, arg=arg)

    def isValid(self, raw: str) -> bool:
        parts = raw.split(maxsplit=1)
        if not parts:
            return False

        first = parts[0].lower()
        if first in self.DIRECTIONS:
            return len(parts) == 1

        return first in self.validVerbs