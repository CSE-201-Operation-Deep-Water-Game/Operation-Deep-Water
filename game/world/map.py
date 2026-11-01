"""Map scaffolding from the class diagram."""

from __future__ import annotations


import game.world.tile as tile_module


class Map:
    """Scaffold for Map from the class diagram."""

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
        """TODO: Implement getTile."""
        raise NotImplementedError("Map.getTile is not implemented yet")

    def setTile(self, x: int, y: int, tile: tile_module.Tile) -> None:
        """TODO: Implement setTile."""
        raise NotImplementedError("Map.setTile is not implemented yet")

    def inBounds(self, x: int, y: int) -> bool:
        """TODO: Implement inBounds."""
        raise NotImplementedError("Map.inBounds is not implemented yet")

    def isPassable(self, x: int, y: int) -> bool:
        """TODO: Implement isPassable."""
        raise NotImplementedError("Map.isPassable is not implemented yet")
