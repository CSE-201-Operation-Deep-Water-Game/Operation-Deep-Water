from __future__ import annotations

import game.world.tile as tile_module
import game.core.person as person_module


class Map:
    def __init__(
        self,
        *,
        grid: list[list[tile_module.Tile]],
        width: int,
        height: int,
    ) -> None:
        self.grid: list[list[tile_module.Tile]] = grid
        self.width: int = width
        self.height: int = height

    def getTile(self, x: int, y: int) -> tile_module.Tile:
        if not self.inBounds(x, y):
            raise IndexError(f"Tile position ({x}, {y}) is outside the map.")
        return self.grid[y][x]

    def setTile(self, x: int, y: int, tile: tile_module.Tile) -> None:
        if not self.inBounds(x, y):
            raise IndexError(f"Tile position ({x}, {y}) is outside the map.")
        tile.x = x
        tile.y = y
        self.grid[y][x] = tile

    def inBounds(self, x: int, y: int) -> bool:
        """Check if tile position (x, y) is within the map.

        Args:
            x (int): x position
            y (int): y position

        :return: True if tile position (x, y) is within the map, False otherwise

        """
        return 0 <= x < self.width and 0 <= y < self.height

    def isPassable(self, x: int, y: int) -> bool:
        """check if tile position (x, y) is passable.
        Args:
            x (int): x position
            y (int): y position

        :return True if tile position (x, y) is passable, False otherwise
        """
        return self.getTile(x, y).isPassable()

    def sonar(self, person: person_module.Person, dir: str) -> str:
        """Creates a string represenation of the players surroundings

        args:
            person (person_module.Person): person for checking position
            dir (str): direction of the sonar

        :return string a representation of the players surroundings.
        """
        playerX, playerY = person.getPosition()

        startX, startY = playerX, playerY

        match dir:
            case "up":
                startY += 1
            case "down":
                startY -= 1
            case "left":
                startX -= 1
            case "right":
                startX += 1

        rows = []
        symbols = {"wall": "#", "open": ".", "exit": "E", "wave": "~"}

        for y in range(startY + 1, startY - 2, -1):
            row = []
            for x in range(startX - 1, startX + 2):
                if (x, y) == (playerX, playerY):
                    symbol = "S"
                elif not self.inBounds(x, y):
                    symbol = "#"
                else:
                    tile = self.getTile(x, y)
                    symbol = symbols.get(tile.tileType, "?")
                    if tile.landmark and tile.tileType == "open":
                        symbol = "L"
                row.append(symbol)
            rows.append(" ".join(row))

        return "\n".join(rows) + (
            "\nS: submarine | #: wall | .: open | E: exit | L: landmark"
            " | ~: wave | ?: unknown"
        )
