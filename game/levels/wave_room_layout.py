"""The 12x9 Wave Room: layout, currents and landmarks, plus a builder.

Coordinates: x grows to the right, y grows UP (so "move up" is +y). LAYOUT is
written top row first, so its first line is y=8 and its last line is y=0.

Both main.py and practice_wave_room.py call buildWaveRoom(), so this is the
only place the room is defined.
"""

from __future__ import annotations

from game.levels.wave_room import WaveRoom
from game.world.map import Map
from game.world.tile import Tile
from game.world.wave import Wave

# S = start, E = exit, # = wall, . = open water, ~ = wave (see WAVES below)
LAYOUT: list[str] = [
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
WAVES: dict[tuple[int, int], tuple[str, int]] = {
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

# (x, y): (landmark label, description). The label is what sonar and the move
# message point at; the description is the longer text shown when you land
# there. Landmarks on open tiles show as "L" on sonar. Landmarks on wave tiles
# still print their text when a current drops you there, but sonar draws them
# as "~". Landmarks on walls show their description when you bump into them.
# Some landing spots are left blank on purpose.
LANDMARKS: dict[tuple[int, int], tuple[str, str]] = {
    (1, 1): (
        "submarine wreckage",
        "A pile of twisted metal scraps lies on the ground. They look like the "
        "remains of another submarine.",
    ),
    (3, 1): (
        "weathered wall",
        "The wall is incredibly smooth, worn down by years of relentless "
        "currents.",
    ),
    (0, 3): (
        "faded poster",
        "A water-stained propaganda poster clings to the wall. It promises a "
        "glorious future and, in smaller print, a mandatory safety briefing.",
    ),
    (2, 5): (
        "rope ladder",
        "A rope ladder sways in the current, leading nowhere. Someone tied it "
        "with great confidence and no visible plan.",
    ),
    (5, 6): (
        "cable tangle",
        "A thick tangle of cable drifts like a regulation-gray jellyfish. A "
        "tag on it says DO NOT TOUCH, which is exactly what you were thinking.",
    ),
    (7, 0): (
        "ration crate",
        "A sealed ration crate rests on the floor, stamped 'Property of the "
        "State'. It is empty. The State got here first.",
    ),
    (9, 4): (
        "diving bell",
        "A toppled diving bell lies on its side, hatch rusted open. The manual "
        "inside is forty pages of warnings and one page of instructions.",
    ),
    (10, 3): (
        "stern buoy",
        "A battered buoy is wedged against the rock, its peeling paint forming "
        "a very stern face. It does not approve of you.",
    ),
    (11, 7): (
        "cracked porthole",
        "A cracked porthole is set into the wall. Beyond it, only dark water "
        "and the faint sense of being filed under 'pending review'.",
    ),
    (10, 8): (
        "red glow",
        "A faint red glow bleeds around the corner. Either the exit, or "
        "something that wants you to think so.",
    ),
}

INTRO: str = (
    "You enter a new room, where a strong current surges through the "
    "passages. You can feel your submarine being pushed around. Map the room "
    "and find the exit."
)


def buildWaveRoom() -> WaveRoom:
    """Build a fresh WaveRoom from LAYOUT, WAVES and LANDMARKS."""
    height = len(LAYOUT)
    width = len(LAYOUT[0])
    start = (0, 0)
    grid: list[list[Tile]] = []

    for row, text in enumerate(LAYOUT):
        if len(text) != width:
            raise ValueError(f"Wave Room row {row} is not {width} tiles wide.")
        y = height - 1 - row
        tiles: list[Tile] = []
        for x, ch in enumerate(text):
            landmark, description = LANDMARKS.get((x, y), ("", ""))
            if landmark and ch == "E":
                raise ValueError(f"Landmark at ({x}, {y}) is on the exit.")

            if ch == "#":
                tiles.append(
                    Tile(
                        x=x,
                        y=y,
                        tileType="wall",
                        landmark=landmark,
                        description=description,
                    )
                )
            elif ch == "E":
                tiles.append(Tile(x=x, y=y, tileType="exit", landmark=""))
            elif ch == "~":
                direction, magnitude = WAVES[(x, y)]
                tiles.append(
                    Wave(
                        x=x,
                        y=y,
                        direction=direction,
                        magnitude=magnitude,
                        landmark=landmark,
                        description=description,
                    )
                )
            else:
                if ch == "S":
                    start = (x, y)
                tiles.append(
                    Tile(
                        x=x,
                        y=y,
                        tileType="open",
                        landmark=landmark,
                        description=description,
                    )
                )
        grid.append(tiles)

    # Row 0 of the grid must be y=0, so flip the top-first layout.
    grid.reverse()

    return WaveRoom(
        name="Wave Room",
        map=Map(grid=grid, width=width, height=height),
        startX=start[0],
        startY=start[1],
        introText=INTRO,
        complete=False,
    )
