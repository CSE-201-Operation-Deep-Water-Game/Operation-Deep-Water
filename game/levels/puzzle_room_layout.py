"""Puzzle Room layout. Rows run top to bottom; x points right and y points up.

The four landmarks at (2, 2), (8, 2), (2, 6), (8, 6) define two
diagonals crossing at (5, 4). E is a sealed wall until sonar unlocks it.
The crossing deliberately has no special map symbol.
"""

from game.levels.puzzle_level import PuzzleLevel
from game.world.map import Map
from game.world.tile import Tile


LAYOUT: list[str] = [
    "#########E#",  # y=8
    "#...#.....#",  # y=7
    "#.L.#.#.L.#",  # y=6
    "#.#...#.#.#",  # y=5
    "#...#...#.#",  # y=4
    "###.#.#...#",  # y=3
    "#.L...#.L.#",  # y=2
    "#.###...#.#",  # y=1
    "#S#########",  # y=0
]

LANDMARKS: dict[tuple[int, int], tuple[str, str]] = {
    (2, 2): (
        "drowned survey tablet",
        "A military tablet displays four survey points. Its final entry reads: "
        "'These four relics are markers. Plot their positions on your grid.' "
        "The report was filed years before your supposedly first expedition.",
    ),
    (8, 2): (
        "carved navigator",
        "A faceless stone navigator points toward the opposite corner. A diver's "
        "translation tag reads: 'Join each marker to the one diagonally opposite. "
        "Their paths form an X.' The figure holds a miniature NAYRB artifact.",
    ),
    (2, 6): (
        "broken listening shrine",
        "A government hydrophone has been bolted to an ancient shrine. A scratched "
        "note reads: 'Go to the tile where both diagonals cross. The listener "
        "waits beneath that spot.' Something below answers with a faint knock.",
    ),
    (8, 6): (
        "silent choir pillar",
        "Four carved mouths surround a closed stone iris. A recovered field "
        "note reads: 'Send a sonar pulse while sitting at the X's intersection "
        "to open the northern exit. Pinging from a marker does nothing.' "
        "Below it: 'Command knew this was a lock. What did they leave inside?'",
    ),
}

INTRO: str = (
    "You enter a still chamber. Broken partitions divide the chamber into winding galleries. "
    "A sealed stone iris blocks the northern exit.")


def buildPuzzleRoom() -> PuzzleLevel:
    """Build a fresh room with four clues and a locked exit."""
    height, width = len(LAYOUT), len(LAYOUT[0])
    grid: list[list[Tile]] = []
    start = (1, 0)
    exit_position = (9, 8)
    for row_index, row in enumerate(LAYOUT):
        y = height - 1 - row_index
        tiles = []
        for x, symbol in enumerate(row):
            landmark, description = LANDMARKS.get((x, y), ("", ""))
            if symbol == "E":
                description = "A sealed stone iris blocks the exit. Four grooves meet at its center."
            tiles.append(Tile(
                x=x, y=y,
                tileType="wall" if symbol in "#E" else "open",
                landmark=landmark, description=description,
            ))
        grid.append(tiles)
    # Row 0 of the grid must be y=0, so flip the top-first layout.
    grid.reverse()
    return PuzzleLevel(
        name="Puzzle Room", map=Map(grid=grid, width=width, height=height),
        startX=start[0], startY=start[1], introText=INTRO, complete=False,
        intersectionX=5, intersectionY=4,
        rechargeLandmarks=True,
        exitX=exit_position[0], exitY=exit_position[1],
    )
