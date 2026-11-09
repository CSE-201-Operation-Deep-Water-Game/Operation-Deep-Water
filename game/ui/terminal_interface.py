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
            "=== OPERATION DEEP WATER ===\n"
            "The hatch seals behind you. Welded inside a Soviet submarine, you begin\n"
            "your descent into the crushing dark of the Mariana Trench.\n"
            "\n"
            "An unknown signal pulses from somewhere below. Its source is the NAYRB,\n"
            "an artifact hidden in a maze of caves and an ancient temple carved into\n"
            "the trench wall. Follow the signal, chart the passages, and find a way\n"
            "deeper. Keep a map as you explore; the route ahead will not reveal itself\n"
            "all at once.\n"
            "\n"
            "Your submarine is your only lifeline. Watch for walls and hazards:\n"
            "every move costs energy, and if it runs out, the mission ends.\n"
            "\n"
            "Avoid getting lost by using your sonar to locate the exit. Be warned, the sonar\n"
            "requires a lot of energy to use, so use it sparingly.\n"
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
