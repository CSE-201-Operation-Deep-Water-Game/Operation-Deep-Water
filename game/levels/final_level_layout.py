"""The flooded escape maze and its landmarks."""

from game.levels.final_level import FinalLevel
from game.world.map import Map
from game.world.tile import Tile

# Rows run from highest y to lowest. A marks the NAYRB artifact.
LAYOUT = [
    "#######..E#",
    "#.....#..##",
    "#.###.#...#",
    "#...#...#.#",
    "###.###.#.#",
    "#.......#.#",
    "#S###A###.#",
]

LANDMARKS = {
    (7, 1): (
        "vent marker",
        "A bent marker points up toward the surface vent.",
    ),
    (7, 3): (
        "cracked observation window",
        "On the other side of the glass, something keeps pace with your lights. "
        "Bubbles rise through the passage above.",
    ),
    (5, 0): (
        "NAYRB pedestal",
        "The NAYRB shivers on its stone pedestal in a narrow alcove.",
    ),
}

INTRO = (
    "Something is chasing you. You hear it scraping through the passage behind "
    "your submarine. Find the NAYRB and escape to the exit."
)


def buildFinalLevel() -> FinalLevel:
    """Build a fresh final level from the escape maze."""
    grid: list[list[Tile]] = []
    for y, row in enumerate(reversed(LAYOUT)):
        tiles: list[Tile] = []
        for x, symbol in enumerate(row):
            tileType = {"#": "wall", "E": "exit"}.get(symbol, "open")
            landmark, description = LANDMARKS.get((x, y), ("", ""))
            if symbol == "S":
                startX, startY = x, y
            elif symbol == "A":
                artifactX, artifactY = x, y
            tiles.append(
                Tile(x=x, y=y, tileType=tileType, landmark=landmark, description=description)
            )
        grid.append(tiles)

    return FinalLevel(
        name="Final Level",
        map=Map(grid=grid, width=len(LAYOUT[0]), height=len(LAYOUT)),
        startX=startX,
        startY=startY,
        introText=INTRO,
        complete=False,
        artifactX=artifactX,
        artifactY=artifactY,
        isTimerStarted=False,
        isTimerOver=False,
        timer=None
    )
