from __future__ import annotations

import game.commands.command as command_module
import game.core.checkpoint_manager as checkpoint_manager_module
import game.core.person as person_module
import game.levels.level as level_module
import game.ui.terminal_interface as terminal_interface_module


class GameController:
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
            try:
                command = self.ui.parser.parse(raw)
            except ValueError:
                self.ui.print("Unrecognized command. To move, enter: move up, move down, move left, or move right.")
                continue
            self.handleCommand(command)
            if self.currentLevel.complete:
                self.ui.print("You reached the exit.")
                self.advanceLevel()

    def handleCommand(self, cmd: command_module.Command) -> None:
        if cmd.verb == "move":
            oldPosition = self.person.getPosition()
            message = self.currentLevel.handleMove(self.person, cmd.arg)

            x, y = self.person.getPosition()
            if (x, y) != oldPosition:
                tile = self.currentLevel.map.getTile(x, y)
                landmark = tile.getLandmark()
                if landmark:
                    message += f"\n{landmark}"

            self.ui.print(f"{message}\nEnergy: {self.person.getEnergy()}")

        elif cmd.verb == "status":
            self.ui.print("ENERGY: " + str(self.person.getEnergy()))

        elif cmd.verb == "sonar":
            message = self.person.sonar(self.currentLevel.map)
            self.ui.print(f"{message}\nEnergy: {self.person.getEnergy()}")

        elif cmd.verb in ("end", "quit"):
            self.ui.print("Thanks for playing!")
            self.running = False
            return

        if self.person.isDead():
            self.handleDeath()


    def loadCheckpoint(self, password: str) -> bool:
        """TODO: Implement loadCheckpoint."""
        raise NotImplementedError("GameController.loadCheckpoint is not implemented yet")

    def advanceLevel(self) -> None:
        currentLevelIndex = self.levels.index(self.currentLevel)
        if currentLevelIndex < len(self.levels) - 1:
            self.currentLevel = self.levels[currentLevelIndex + 1]
            self.ui.print(self.currentLevel.start(self.person))
            self.person.resetEnergy()
        else:
            self.endGame(won=True)      

    def handleDeath(self) -> None:
        self.ui.print("You died! Your energy reached zero.")

        while True:
            self.ui.print("Would you like to restart? (yes/no)")
            choice = self.ui.prompt().strip().lower()

            if choice in ("yes", "y"):
                self.person.resetEnergy()

                for level in self.levels:
                    level.complete = False

                self.currentLevel = self.levels[0]
                self.ui.showBriefing()
                self.ui.print(self.currentLevel.start(self.person))

                self.running = True
                return

            if choice in ("no", "n"):
                self.ui.print("Thanks for playing!")
                self.running = False
                return

            self.ui.print("Please enter yes or no.")

    def endGame(self, won: bool) -> None:
        """TODO: Implement endGame."""
        raise NotImplementedError("GameController.endGame is not implemented yet")
