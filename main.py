"""Construct the game's dependencies and start its controller."""

from game.commands.command import Command
from game.commands.command_parser import CommandParser
from game.core.checkpoint_manager import CheckpointManager
from game.core.game_controller import GameController
from game.core.person import Person
from game.events.artifact_event import ArtifactEvent
from game.events.base_event import BaseEvent
from game.events.exit_event import ExitEvent
from game.events.hazard_event import HazardEvent
from game.events.landmark_event import LandmarkEvent
from game.events.wall_event import WallEvent
from game.events.wave_room import WaveRoom
from game.levels.current_level import CurrentLevel
from game.levels.final_level import FinalLevel
from game.levels.level import Level
from game.levels.puzzle_level import PuzzleLevel
from game.levels.tutorial_level import TutorialLevel
from game.puzzles.puzzle import Puzzle
from game.ui.terminal_interface import TerminalInterface
from game.world.map import Map
from game.world.tile import Tile

__all__ = [
    "ArtifactEvent",
    "BaseEvent",
    "CheckpointManager",
    "Command",
    "CommandParser",
    "CurrentLevel",
    "ExitEvent",
    "FinalLevel",
    "GameController",
    "HazardEvent",
    "LandmarkEvent",
    "Level",
    "Map",
    "Person",
    "Puzzle",
    "PuzzleLevel",
    "TerminalInterface",
    "Tile",
    "TutorialLevel",
    "WallEvent",
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
            "quit": "quit",
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
                event=None,
                landmark="",
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
        introText="Welcome to Operation Deep Water. Find your way to the exit.",
        complete=False,
        hints=["Use move up, down, left, or right to explore."],
    )
    game_controller = GameController(
        person=player,
        levels=[tutorial],
        currentLevel=tutorial,
        ui=ui,
        checkpoints=checkpoints,
        running=False,
    )

    game_controller.start()


if __name__ == "__main__":
    main()
