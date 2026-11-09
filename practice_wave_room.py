"""Practice mode: drop straight into the Wave Room, skipping the tutorial.

Run it from the project folder with:  python practice_wave_room.py

It uses the same room, commands and controller as the real game. The room
itself (layout, currents, landmarks) lives in game/levels/wave_room_layout.py,
so edit it there and both this script and main.py pick up the change.
"""

from game.commands.command_parser import CommandParser
from game.core.checkpoint_manager import CheckpointManager
from game.core.game_controller import GameController
from game.core.person import Person
from game.levels.wave_room_layout import buildWaveRoom
from game.ui.terminal_interface import TerminalInterface


def main() -> None:
    room = buildWaveRoom()
    player = Person(
        energyAmt=20,
        maxEnergy=20,
        positionX=room.startX,
        positionY=room.startY,
    )
    parser = CommandParser(
        validVerbs={
            "move": "move",
            "look": "look",
            "help": "help",
            "status": "status",
            "sonar": "sonar",
            "quit": "quit",
            "end": "end",
        }
    )
    controller = GameController(
        person=player,
        levels=[room],
        currentLevel=room,
        ui=TerminalInterface(parser=parser),
        checkpoints=CheckpointManager(passwords={}),
        running=False,
    )
    controller.start()


if __name__ == "__main__":
    main()
