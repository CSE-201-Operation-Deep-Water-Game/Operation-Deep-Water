"""The 12x9 Wave Room: layout, currents and landmarks, plus a builder.

Coordinates: x grows to the right, y grows UP (so "move up" is +y). LAYOUT is
written top row first, so its first line is y=8 and its last line is y=0.

main.py calls buildWaveRoom(), so this is the only place the room is defined.
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
        "unmarked survey wreck",
        "A survey submarine lies crushed against the stone, its identifying "
        "numbers ground away. Inside its open chart case is a government seal "
        "matching your orders. You were told this passage had never been explored.",
    ),
    (3, 1): (
        "buried inscription",
        "Beneath a broken layer of concrete, rows of unfamiliar symbols cover "
        "the wall. The concrete bears a recent military survey stamp. Someone "
        "found this writing before you, then paid to bury it.",
    ),
    (0, 3): (
        "sealed research canister",
        "A split canister holds photographs of towers beneath the seabed. "
        "A classified note reads: 'Settlement predates all known human sites. "
        "Public designation remains geological formation.'",
    ),
    (2, 5): (
        "carved stone figures",
        "A frieze shows slender, jointed figures gathered around a ring of "
        "symbols. None has a human face. Their hands reach toward an empty "
        "recess shaped like the artifact in your mission dossier.",
    ),
    (5, 6): (
        "severed listening cable",
        "A government listening cable is wrapped around an inscribed pillar. "
        "Its armored sheath has been pulled apart, leaving fresh copper "
        "exposed. Your receiver catches three slow knocks. Then three more, "
        "from somewhere beyond the pillar.",
    ),
    (7, 0): (
        "NAYRB research case",
        "A waterproof case contains failed translations of the same alien "
        "inscription. One line is underlined: 'NAYRB may supply the missing "
        "reference needed to read their language.' Every proposed translation "
        "has been crossed out.",
    ),
    (9, 4): (
        "abandoned diving bell",
        "An empty diving bell rests beside a survey marker. Its tether is "
        "still secure, but the hatch has buckled inward. The last log entry "
        "reads: 'Movement below the excavation. No matching sonar contact. "
        "Requesting instructions.' There is no reply.",
    ),
    (10, 3): (
        "damaged survey recorder",
        "A recorder repeats a clipped voice: 'Command, the marks are not "
        "erosion. Something is moving through the lower galleries.' A second "
        "voice asks for a visual identification. Only scraping follows.",
    ),
    (11, 7): (
        "alien observation window",
        "A seamless pane looks into a chamber lined with the same unreadable "
        "script. Sediment lifts from the floor in a long, narrow trail. Your "
        "lights reach the far wall, but you cannot see what disturbed it.",
    ),
    (10, 8): (
        "resonant doorway",
        "Symbols around a stone doorway pulse in time with the NAYRB signal. "
        "Your orders say to recover the artifact and leave all inscriptions "
        "untouched. Beyond the doorway, something scrapes once against stone. "
        "The mission dossier lists no living organisms at this depth.",
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
