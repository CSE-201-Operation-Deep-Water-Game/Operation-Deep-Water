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
        return 0 <= x < self.width and 0 <= y < self.height

    def isPassable(self, x: int, y: int) -> bool:
        return self.getTile(x, y).isPassable()

    def sonar(self, person: person_module.Person) -> str:
        playerX, playerY = person.getPosition()
        rows = []
        symbols = {"wall": "#", "open": ".", "exit": "E", "wave": "~"}

        for y in range(playerY + 1, playerY - 2, -1):
            row = []
            for x in range(playerX - 1, playerX + 2):
                if (x, y) == (playerX, playerY):
                    symbol = "P"
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
            "\nP: player | #: wall | .: open | E: exit | L: landmark"
            " | ~: wave | ?: unknown"
        )
