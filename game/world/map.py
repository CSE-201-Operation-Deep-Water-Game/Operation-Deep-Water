import game.world.tile as tile_module


class Map:
    def __init__(
        self,
        *,
        grid: "list[list[tile_module.Tile]]",
        width: int,
        height: int,
    ) -> None:
        self.grid: list[list[tile_module.Tile]] = grid
        self.width: int = width
        self.height: int = height

    def getTile(self, x: int, y: int) -> "tile_module.Tile":
        if not self.inBounds(x, y):
            raise IndexError(f"Tile position ({x}, {y}) is outside the map.")
        return self.grid[y][x]

    def setTile(self, x: int, y: int, tile: "tile_module.Tile") -> None:
        if not self.inBounds(x, y):
            raise IndexError(f"Tile position ({x}, {y}) is outside the map.")
        tile.x = x
        tile.y = y
        self.grid[y][x] = tile

    def inBounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def isPassable(self, x: int, y: int) -> bool:
        return self.getTile(x, y).isPassable()
