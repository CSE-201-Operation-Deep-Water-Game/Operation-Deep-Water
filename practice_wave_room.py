"""Practice mockup of the Wave Room, separate from the real game flow.

Run it from the project folder with:  python practice_wave_room.py

It drops you straight into a 12x9 Wave Room with the same commands as the real
game (move, status, sonar, end/quit). Nothing here is imported by main.py, so it
can be edited or deleted freely.

Coordinates: x grows to the right, y grows UP (so "move up" is +y). The LAYOUT
below is written top row first, so the first line is y=8 and the last is y=0.
"""

from game.commands.command_parser import CommandParser
from game.core.checkpoint_manager import CheckpointManager
from game.core.game_controller import GameController
from game.core.person import Person
from game.levels.wave_room import WaveRoom
from game.ui.terminal_interface import TerminalInterface
from game.world.map import Map
from game.world.tile import Tile
from game.world.wave import Wave

# S = start, E = exit, # = wall, . = open water, ~ = wave (see WAVES below)
LAYOUT = [
    "..#.#......E",  # y=8
    ".....#..#~.~",  # y=7
    "##..#~.....#",  # y=6
    "#~~##.......",  # y=5
    "..#...#.#.#.",  # y=4
    "...##~..#...",  # y=3
    ".#...~.##..#",  # y=2
    "#.~#.#..##..",  # y=1
    "S~.###..##~~",  # y=0
]

# (x, y): (direction, magnitude). Every "~" in LAYOUT needs an entry here.
WAVES = {
    (1, 0): ("down", 3),
    (10, 0): ("up", 3),
    (11, 0): ("left", 4),
    (2, 1): ("right", 4),
    (5, 2): ("up", 4),
    (5, 3): ("down", 4),
    (1, 5): ("right", 3),
    (2, 5): ("left", 3),
    (5, 6): ("down", 3),
    (9, 7): ("right", 2),
    (11, 7): ("left", 2),
}

INTRO = (
    "You drift into a flooded chamber where strong currents surge through the "
    "passages. Your sub is shoved around and you can't tell exactly where. "
    "Map the room and find the exit."
)


def buildWaveRoom() -> WaveRoom:
    height = len(LAYOUT)
    width = len(LAYOUT[0])
    grid: list[list[Tile]] = []
    start = (0, 0)

    for row, text in enumerate(LAYOUT):
        y = height - 1 - row
        tiles: list[Tile] = []
        for x, ch in enumerate(text):
            if ch == "#":
                tiles.append(Tile(x=x, y=y, tileType="wall", landmark=""))
            elif ch == "E":
                tiles.append(Tile(x=x, y=y, tileType="exit", landmark=""))
            elif ch == "~":
                direction, magnitude = WAVES[(x, y)]
                tiles.append(Wave(x=x, y=y, direction=direction, magnitude=magnitude))
            else:
                if ch == "S":
                    start = (x, y)
                tiles.append(Tile(x=x, y=y, tileType="open", landmark=""))
        grid.append(tiles)

    # Row 0 of the grid must be y=0, so flip the top-first layout.
    grid.reverse()

    return WaveRoom(
        name="Wave Room (practice)",
        map=Map(grid=grid, width=width, height=height),
        startX=start[0],
        startY=start[1],
        introText=INTRO,
        complete=False,
    )


class PracticeController(GameController):
    """GameController that prints a win message when the room is cleared."""

    def endGame(self, won: bool) -> None:
        self.ui.print("You escaped the Wave Room! (practice mode complete)")


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
    controller = PracticeController(
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
