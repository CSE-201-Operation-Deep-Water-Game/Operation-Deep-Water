from __future__ import annotations

import game.commands.command_parser as command_parser_module


class TerminalInterface:
    def __init__(
        self,
        *,
        parser: command_parser_module.CommandParser,
    ) -> None:
        self.parser: command_parser_module.CommandParser = parser

    def print(self, text: str) -> None:
        print(text)

    def prompt(self) -> str:
        return input("> ")

    def showBriefing(self) -> None:
        self.print(
            "=== Operation Deep Water ===\n"
            "Your mission: explore the underwater facility and recover the artifact.\n"
            "Find each level's exit to continue. Watch for walls and hazards.\n"
            "Each successful move costs energy. If your energy reaches zero, you die.\n"
            "\n"
            "To move, enter: move up, move down, move left, or move right.\n"
        )

    def askNewOrPassword(self) -> str:
        """TODO: Implement askNewOrPassword."""
        raise NotImplementedError("TerminalInterface.askNewOrPassword is not implemented yet")

    def showHelp(self, lines: list[str]) -> None:
        """TODO: Implement showHelp."""
        raise NotImplementedError("TerminalInterface.showHelp is not implemented yet")

    def showStatus(self, energy: int) -> None:
        """TODO: Implement showStatus."""
        raise NotImplementedError("TerminalInterface.showStatus is not implemented yet")
