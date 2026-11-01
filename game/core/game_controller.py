"""GameController scaffolding from the class diagram."""

from __future__ import annotations


import game.commands.command as command_module
import game.core.checkpoint_manager as checkpoint_manager_module
import game.core.person as person_module
import game.levels.level as level_module
import game.ui.terminal_interface as terminal_interface_module


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
        self._person: person_module.Person = person
        self._levels: list[level_module.Level] = levels
        self._currentLevel: level_module.Level = currentLevel
        self._ui: terminal_interface_module.TerminalInterface = ui
        self._checkpoints: checkpoint_manager_module.CheckpointManager = checkpoints
        self._running: bool = running

    def start(self) -> None:
        """TODO: Implement start."""
        raise NotImplementedError("GameController.start is not implemented yet")

    def run(self) -> None:
        """TODO: Implement run."""
        raise NotImplementedError("GameController.run is not implemented yet")

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
