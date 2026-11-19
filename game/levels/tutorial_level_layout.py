"""The 8x5 Tutorial level: layout, landmarks and a builder.

Coordinates: x grows to the right, y grows UP (so "move up" is +y). LAYOUT is
written top row first, so its first line is y=4 and its last line is y=0.

main.py calls buildTutorialLevel(), so this is the only place the level is
defined.
"""

from __future__ import annotations

from game.levels.tutorial_level import TutorialLevel
from game.world.map import Map
from game.world.tile import Tile

# S = start, E = exit, # = wall, . = open water
LAYOUT: list[str] = [
    "E.......",  # y=4
    ".#..##..",  # y=3
    "..#..##.",  # y=2
    "...#.#S.",  # y=1
    "...#....",  # y=0
]

# (x, y): (landmark label, description). Landmarks on walls show their
# description when you bump into them.
LANDMARKS: dict[tuple[int, int], tuple[str, str]] = {
    (4, 0): (
        "inscribed stone fragment",
        "A stone fragment bears precise symbols beneath centuries "
        "of mineral growth. One matches the NAYRB sketch in your "
        "sealed government orders.",
    ),
    (3, 1): (
        "concealed alien script",
        "Flaking survey paint exposes lines of alien script. "
        "A military stencil labels the wall NATURAL FORMATION. "
        "You cannot read the symbols; the NAYRB artifact is "
        "rumored to be the key.",
    ),
}

INTRO: str = (
    "You enter a dark, narrow passage. You must find your way "
    "through the maze of walls to reach the exit."
)

HINTS: list[str] = ["Use move up, down, left, or right to explore."]


def buildTutorialLevel() -> TutorialLevel:
    """Build a fresh TutorialLevel from LAYOUT and LANDMARKS."""
    height = len(LAYOUT)
    width = len(LAYOUT[0])
    start = (0, 0)
    grid: list[list[Tile]] = []

    for row, text in enumerate(LAYOUT):
        if len(text) != width:
            raise ValueError(f"Tutorial row {row} is not {width} tiles wide.")
        y = height - 1 - row
        tiles: list[Tile] = []
        for x, ch in enumerate(text):
            landmark, description = LANDMARKS.get((x, y), ("", ""))
            if landmark and ch == "E":
                raise ValueError(f"Landmark at ({x}, {y}) is on the exit.")

            if ch == "#":
                tileType = "wall"
            elif ch == "E":
                tileType = "exit"
            else:
                tileType = "open"
                if ch == "S":
                    start = (x, y)
            tiles.append(
                Tile(
                    x=x,
                    y=y,
                    tileType=tileType,
                    landmark=landmark,
                    description=description,
                )
            )
        grid.append(tiles)

    # Row 0 of the grid must be y=0, so flip the top-first layout.
    grid.reverse()

    return TutorialLevel(
        name="Tutorial",
        map=Map(grid=grid, width=width, height=height),
        startX=start[0],
        startY=start[1],
        introText=INTRO,
        complete=False,
        hints=list(HINTS),
    )
