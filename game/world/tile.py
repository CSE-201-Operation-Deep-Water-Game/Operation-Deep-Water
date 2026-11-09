from __future__ import annotations

class Tile:
    def __init__(
        self,
        *,
        x: int,
        y: int,
        tileType: str,
        landmark: str,
    ) -> None:
        self.x: int = x
        self.y: int = y
        self.tileType: str = tileType
        self.landmark: str = landmark

    def isPassable(self) -> bool:
        return self.tileType != "wall"

    def setType(self, tileType: str) -> None:
        """TODO: Implement setType."""
        raise NotImplementedError("Tile.setType is not implemented yet")

    def getDescription(self) -> str:
        """TODO: Implement getDescription."""
        raise NotImplementedError("Tile.getDescription is not implemented yet")

    def getLandmark(self) -> str:
        return self.landmark

    def setLandmark(self, landmark: str) -> None:
        self.landmark = landmark
