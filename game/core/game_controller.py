"""GameController scaffolding from the class diagram."""

from __future__ import annotations


import game.commands.command as command_module
import game.core.checkpoint_manager as checkpoint_manager_module
import game.core.person as person_module
import game.levels.level as level_module
import game.ui.terminal_interface as terminal_interface_module
from game.levels import tutorial_level


class GameController:
    """Scaffold for GameController from the class diagram."""

    def __init__(
        self,
        *,
        person: person_module.Person,
        levels: list[level_module.Level],
        currentLevel: level_module.Level,
        ui: terminal_interface_module.TerminalInterface,
        checkpoints: checkpoint_manager_module.CheckpointManager,
        running: bool,
    ) -> None:
        self.person: person_module.Person = person
        self.levels: list[level_module.Level] = levels
        self.currentLevel: level_module.Level = currentLevel
        self.ui: terminal_interface_module.TerminalInterface = ui
        self.checkpoints: checkpoint_manager_module.CheckpointManager = checkpoints
        self.running: bool = running

    def start(self) -> None:
        self.ui.showBriefing()
        self.person.resetEnergy()

        self.currentLevel = self.levels[0]
        intro = self.currentLevel.start(self.person)
        self.ui.print(intro)

        self.running = True
        self.run()

    def run(self) -> None:
        while self.running:
            raw = self.ui.prompt()
            command = self.ui.parser.parse(raw)
            self.handleCommand(command)

    def handleCommand(self, cmd: command_module.Command) -> None:
        """TODO: Implement handleCommand."""
        raise NotImplementedError("GameController.handleCommand is not implemented yet")

    def loadCheckpoint(self, password: str) -> bool:
        """TODO: Implement loadCheckpoint."""
        raise NotImplementedError("GameController.loadCheckpoint is not implemented yet")

    def advanceLevel(self) -> None:
        """TODO: Implement advanceLevel."""
        raise NotImplementedError("GameController.advanceLevel is not implemented yet")

    def handleDeath(self) -> None:
        """TODO: Implement handleDeath."""
        raise NotImplementedError("GameController.handleDeath is not implemented yet")

    def endGame(self, won: bool) -> None:
        """TODO: Implement endGame."""
        raise NotImplementedError("GameController.endGame is not implemented yet")
