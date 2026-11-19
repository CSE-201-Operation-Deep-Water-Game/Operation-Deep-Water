"""Construct the game's dependencies and start its controller."""

from game.commands.command import Command
from game.commands.command_parser import CommandParser
from game.core.checkpoint_manager import CheckpointManager
from game.core.game_controller import GameController
from game.core.person import Person
from game.levels.final_level import FinalLevel
from game.levels.level import Level
from game.levels.puzzle_level import PuzzleLevel
from game.levels.puzzle_room_layout import buildPuzzleRoom
from game.levels.tutorial_level import TutorialLevel
from game.levels.tutorial_level_layout import buildTutorialLevel
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
            "status": "status",
            "sonar": "sonar",
            "quit": "quit",
            "end": "end",
        }
    )
    ui = TerminalInterface(parser=parser)
    checkpoints = CheckpointManager(passwords={
        "WAVE": 1,
        "PUZZLE": 2,
    })

    tutorial = buildTutorialLevel()
    waveRoom = buildWaveRoom()
    puzzleRoom = buildPuzzleRoom()

    game_controller = GameController(
        person=player,
        levels=[tutorial, waveRoom, puzzleRoom],
        currentLevel=puzzleRoom,
        ui=ui,
        checkpoints=checkpoints,
        running=False,
    )

    game_controller.start()


if __name__ == "__main__":
    main()
