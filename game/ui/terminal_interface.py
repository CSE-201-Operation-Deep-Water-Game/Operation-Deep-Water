"""TerminalInterface scaffolding from the class diagram."""

from __future__ import annotations


import game.commands.command_parser as command_parser_module


class TerminalInterface:
    """Scaffold for TerminalInterface from the class diagram."""

    def __init__(
        self,
        *,
        parser: command_parser_module.CommandParser,
    ) -> None:
        self.parser: command_parser_module.CommandParser = parser

    def print(self, text: str) -> None:
        """TODO: Implement print."""
        raise NotImplementedError("TerminalInterface.print is not implemented yet")

    def prompt(self) -> str:
        """TODO: Implement prompt."""
        raise NotImplementedError("TerminalInterface.prompt is not implemented yet")

    def showBriefing(self) -> None:
        """TODO: Implement showBriefing."""
        raise NotImplementedError("TerminalInterface.showBriefing is not implemented yet")

    def askNewOrPassword(self) -> str:
        """TODO: Implement askNewOrPassword."""
        raise NotImplementedError("TerminalInterface.askNewOrPassword is not implemented yet")

    def showHelp(self, lines: list[str]) -> None:
        """TODO: Implement showHelp."""
        raise NotImplementedError("TerminalInterface.showHelp is not implemented yet")

    def showStatus(self, energy: int) -> None:
        """TODO: Implement showStatus."""
        raise NotImplementedError("TerminalInterface.showStatus is not implemented yet")
