from __future__ import annotations

from typing import TYPE_CHECKING

from game.world.tile import Tile

if TYPE_CHECKING:
    import game.world.map as map_module


class Wave(Tile):
    """A current tile that pushes the player a fixed distance in one direction.

    Each wave stores its own direction and magnitude, chosen when the map is
    built. The tile only works out where the push ends up; the level is
    responsible for moving the player there. One wave pushes once per move, so
    landing on another wave tile does not chain.
    """

    DIRECTIONS: dict[str, tuple[int, int]] = {
        "up": (0, 1),
        "down": (0, -1),
        "left": (-1, 0),
        "right": (1, 0),
    }

    DEFAULT_MESSAGE: str = "A strong current tugs at you..."

    def __init__(
        self,
        *,
        x: int,
        y: int,
        direction: str,
        magnitude: int,
        landmark: str = "",
        description: str = "",
        message: str = DEFAULT_MESSAGE,
    ) -> None:
        direction = direction.lower()
        if direction not in self.DIRECTIONS:
            raise ValueError(
                f"Invalid wave direction '{direction}'. "
                f"Use one of: {', '.join(self.DIRECTIONS)}."
            )
        if isinstance(magnitude, bool) or not isinstance(magnitude, int) or magnitude < 0:
            raise ValueError("Wave magnitude must be a non-negative integer.")

        super().__init__(
            x=x,
            y=y,
            tileType="wave",
            landmark=landmark,
            description=description,
        )
        self.direction: str = direction
        self.magnitude: int = magnitude
        self.message: str = message

    def getPushVector(self) -> tuple[int, int]:
        """Return the (dx, dy) of a single step in this wave's direction."""
        return self.DIRECTIONS[self.direction]

    def getPath(self, map: map_module.Map) -> list[tuple[int, int]]:
        """Return every tile the push carries the player over, in order.

        The starting (wave) tile is not included. The player is carried one
        tile at a time for up to `magnitude` tiles and stops before a wall or
        the map edge. A fully blocked push returns an empty list.
        """
        dx, dy = self.getPushVector()
        x, y = self.x, self.y
        path: list[tuple[int, int]] = []

        for _ in range(self.magnitude):
            nextX, nextY = x + dx, y + dy
            if not map.inBounds(nextX, nextY) or not map.isPassable(nextX, nextY):
                break
            x, y = nextX, nextY
            path.append((x, y))

        return path

    def getDestination(self, map: map_module.Map) -> tuple[int, int]:
        """Return where a player standing on this tile ends up after the push.

        A fully blocked push leaves them on this tile.
        """
        path = self.getPath(map)
        return path[-1] if path else (self.x, self.y)

    def getPushMessage(self) -> str:
        """Return the vague message shown when the wave pushes the player.

        It deliberately omits direction and distance, so players must work out
        where they ended up from landmarks and sonar.
        """
        return self.message
