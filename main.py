"""Construct the game's dependencies and start its controller."""

from game.commands.command import Command
from game.commands.command_parser import CommandParser
from game.core.checkpoint_manager import CheckpointManager
from game.core.game_controller import GameController
from game.core.person import Person
from game.levels.final_level import FinalLevel
from game.levels.level import Level
from game.levels.puzzle_level import PuzzleLevel
from game.levels.tutorial_level import TutorialLevel
from game.levels.wave_room import WaveRoom
from game.levels.wave_room_layout import buildWaveRoom
from game.ui.terminal_interface import TerminalInterface
from game.world.map import Map
from game.world.tile import Tile

__all__ = [
    "CheckpointManager",
    "Command",
    "CommandParser",
    "FinalLevel",
    "GameController",
    "Level",
    "Map",
    "Person",
    "PuzzleLevel",
    "TerminalInterface",
    "Tile",
    "TutorialLevel",
    "WaveRoom",
]

def main() -> None:
    startX, startY = 6, 1
    player = Person(energyAmt=20, maxEnergy=20, positionX=startX, positionY=startY)
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
    ui = TerminalInterface(parser=parser)
    checkpoints = CheckpointManager(passwords={})

    width, height = 8, 5
    walls = {
        (3, 0), (3, 1),
        (5, 1), (6, 2),
        (2, 2), (5, 2),
        (1, 3), (4, 3), (5, 3),
    }
    grid = [
        [
            Tile(
                x=x,
                y=y,
                tileType=(
                    "wall" if (x, y) in walls
                    else "exit" if (x, y) == (0, height - 1)
                    else "open"
                ),
                landmark=(
                    "inscribed stone fragment" if (x, y) == (4, 0)
                    else "concealed alien script" if (x, y) == (3, 1)
                    else ""
                ),
                description=(
                    "A stone fragment bears precise symbols beneath centuries "
                    "of mineral growth. One matches the NAYRB sketch in your "
                    "sealed government orders."
                    if (x, y) == (4, 0)
                    else "Flaking survey paint exposes lines of alien script. "
                    "A military stencil labels the wall NATURAL FORMATION. "
                    "You cannot read the symbols; the NAYRB artifact is "
                    "rumored to be the key."
                    if (x, y) == (3, 1)
                    else ""
                ),
            )
            for x in range(width)
        ]
        for y in range(height)
    ]

    tutorial = TutorialLevel(
        name="Tutorial",
        map=Map(grid=grid, width=width, height=height),
        startX=startX,
        startY=startY,
        introText="You enter a dark, narrow passage. You must find your way " \
        "through the maze of walls to reach the exit.",
        complete=False,
        hints=["Use move up, down, left, or right to explore."],
    )

    waveRoom = buildWaveRoom()

    game_controller = GameController(
        person=player,
        levels=[tutorial, waveRoom],
        currentLevel=tutorial,
        ui=ui,
        checkpoints=checkpoints,
        running=False,
    )

    game_controller.start()


if __name__ == "__main__":
    main()
