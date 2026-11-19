from __future__ import annotations

import game.commands.command as command_module
import game.core.checkpoint_manager as checkpoint_manager_module
import game.core.person as person_module
import game.levels.level as level_module
import game.ui.terminal_interface as terminal_interface_module
from game.levels.final_level import FinalLevel

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
        """Start a new game or resume from a checkpoint password."""
        self.ui.showBriefing()

        if self.checkpoints.passwords:
            while True:
                self.ui.print(
                    "Enter a checkpoint password, or press Enter to start a new game."
                )
                password = self.ui.prompt().strip()
                if not password:
                    break
                if self.loadCheckpoint(password):
                    self.running = True
                    self.run()
                    return
                self.ui.print("Invalid checkpoint password.")

        self.person.resetEnergy()
        self.currentLevel = self.levels[0]
        self.ui.print(self.currentLevel.start(self.person))
        self.running = True
        self.run()

    def run(self) -> None:
        """Game loop with user prompting"""
        while self.running:
            raw = self.ui.prompt()
            try:
                command = self.ui.parser.parse(raw)
            except ValueError:
                self.ui.print("Unrecognized command. To move, enter: move up, move down, move left, or move right.")
                continue
            if (
                isinstance(self.currentLevel, FinalLevel)
                and self.currentLevel.isTimerOver
                and command.verb not in ("end", "quit")
            ):
                self.handleDeath("BRYAN caught up to you and crushed your submarine.")
                continue
            self.handleCommand(command)

            if self.currentLevel.complete:
                self.ui.print("You reached the exit.")
                self.advanceLevel()


    def handleCommand(self, cmd: command_module.Command) -> None:
        """handles user input

        params:
            cmd: command to handle
        """
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
            message = self.person.sonar(self.currentLevel.map, cmd.arg)
            response = self.currentLevel.onSonar(self.person)
            if response:
                message += f"\n{response}"
            self.ui.print(f"{message}\nEnergy: {self.person.getEnergy()}")

        elif cmd.verb in ("end", "quit"):
            self.ui.print("Thanks for playing!")
            self.running = False
            return

        if self.person.isDead():
            self.handleDeath()


    def loadCheckpoint(self, password: str) -> bool:
        """Start the level associated with the supplied password."""
        if not self.checkpoints.isValid(password):
            return False

        levelIndex = self.checkpoints.validate(password)
        if not 0 <= levelIndex < len(self.levels):
            return False

        self.currentLevel = self.levels[levelIndex]
        self.person.resetEnergy()
        self.ui.print(self.currentLevel.start(self.person))
        return True

    def advanceLevel(self) -> None:
        """Enter the next level or end the game after the final exit."""
        nextLevelIndex = self.levels.index(self.currentLevel) + 1
        if nextLevelIndex >= len(self.levels):
            won = not isinstance(self.currentLevel, FinalLevel) or self.currentLevel.hasArtifact
            self.endGame(won=won)
            return

        self.currentLevel = self.levels[nextLevelIndex]
        self.person.resetEnergy()
        self.ui.print(self.currentLevel.start(self.person))

        password = self.checkpoints.award(nextLevelIndex)
        if password is not None:
            self.ui.print(f"Checkpoint password: {password}")

    def handleDeath(self, message: str = "You died! Your energy reached zero.") -> None:
        """handles death and prompts user to restart game"""
        self.ui.print(message)

        while True:
            self.ui.print("Would you like to restart? (yes/no)")
            choice = self.ui.prompt().strip().lower()

            if choice in ("yes", "y"):
                self.person.resetEnergy()

                self.ui.print(self.currentLevel.start(self.person))

                self.running = True
                return

            if choice in ("no", "n"):
                self.ui.print("Thanks for playing!")
                self.running = False
                return

            self.ui.print("Please enter yes or no.")

    def endGame(self, won: bool) -> None:
        if won:
            self.ui.print(
                "Mission complete. An underwater geyser carries your submarine to the "
                "surface. The NAYRB is secure. A radio signal breaks through the static. "
                "It's time to go home. YOU WON!"
            )
        elif isinstance(self.currentLevel, FinalLevel) and self.currentLevel.isComplete():
            self.ui.print(
                "You reach the surface empty-handed."
                "The NAYRB still below. The mission has failed."
                "Your commander is not going to be happy about this."
            )

        self.ui.print("Thanks for playing!")
        self.running = False
