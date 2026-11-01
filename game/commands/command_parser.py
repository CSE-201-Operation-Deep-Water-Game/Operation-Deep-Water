"""CommandParser scaffolding from the class diagram."""

from __future__ import annotations


import game.commands.command as command_module


class CommandParser:
    """Scaffold for CommandParser from the class diagram."""

    def __init__(
        self,
        *,
        validVerbs: dict[str, str],
    ) -> None:
        self.validVerbs: dict[str, str] = validVerbs

    def parse(self, raw: str) -> command_module.Command:
        """TODO: Implement parse."""
        raise NotImplementedError("CommandParser.parse is not implemented yet")

    def isValid(self, raw: str) -> bool:
        """TODO: Implement isValid."""
        raise NotImplementedError("CommandParser.isValid is not implemented yet")

    def getHelpText(self) -> list[str]:
        """TODO: Implement getHelpText."""
        raise NotImplementedError("CommandParser.getHelpText is not implemented yet")
