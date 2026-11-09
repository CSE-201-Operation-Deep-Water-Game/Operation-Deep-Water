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
from game.puzzles.puzzle import Puzzle
from game.ui.terminal_interface import TerminalInterface
from game.world.map import Map
from game.world.tile import Tile
from game.world.wave import Wave

__all__ = [
    "CheckpointManager",
    "Command",
    "CommandParser",
    "FinalLevel",
    "GameController",
    "Level",
    "Map",
    "Person",
    "Puzzle",
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
                    "jagged rock" if (x, y) == (4, 0)
                    else "suspicious carving" if (x, y) == (3, 1)
                    else ""
                ),
                description=(
                    "A jagged rock juts from the trench floor, its sharp edges "
                    "catching the beam of your lights."
                    if (x, y) == (4, 0)
                    else "A series of strange symbols has been carved into the "
                    "wall. The marks look deliberate, but you cannot make sense "
                    "of them."
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

    waveRoomWalls = {
        (2, 0), (2, 1),
        (4, 1), (6, 2),
        (1, 3), (3, 3), (5, 3),
    }
    waveRoomWaves = {
        (4, 2): ("left", 2),
        (5, 2): ("left", 2),
        (6, 3): ("up", 1),
    }
    waveRoomGrid = [
        [
            Wave(
                x=x,
                y=y,
                direction=waveRoomWaves[(x, y)][0],
                magnitude=waveRoomWaves[(x, y)][1],
            )
            if (x, y) in waveRoomWaves else Tile(
                x=x,
                y=y,
                tileType=(
                    "wall" if (x, y) in waveRoomWalls
                    else "exit" if (x, y) == (0, height - 1)
                    else "open"
                ),
                landmark="",
            )
            for x in range(width)
        ]
        for y in range(height)
    ]
    waveRoom = WaveRoom(
        name="Wave Room",
        map=Map(grid=waveRoomGrid, width=width, height=height),
        startX=startX,
        startY=startY,
        introText=(
            "You enter a new room, where a strong current surges through the "
            "passages. You can feel your submarine being pushed around. Map the room and find the exit."
        ),
        complete=False,
    )

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
