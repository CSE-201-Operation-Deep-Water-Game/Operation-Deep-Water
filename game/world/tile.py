from __future__ import annotations

class Tile:
    def __init__(
        self,
        *,
        x: int,
        y: int,
        tileType: str,
        landmark: str,
        description: str = "",
    ) -> None:
        self.x: int = x
        self.y: int = y
        self.tileType: str = tileType
        self.landmark: str = landmark
        self.description: str = description

    def isPassable(self) -> bool:
        """Checks if this tile can be passed"""
        return self.tileType != "wall"

    def setType(self, tileType: str) -> None:
        """TODO: Implement setType."""
        raise NotImplementedError("Tile.setType is not implemented yet")

    def getLandmark(self) -> str:
        return self.landmark

    def setLandmark(self, landmark: str) -> None:
        self.landmark = landmark

    def getDescription(self) -> str:
        return self.description

    def setDescription(self, description: str) -> None:
        self.description = description
