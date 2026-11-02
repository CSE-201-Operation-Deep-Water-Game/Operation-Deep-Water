from game.levels.level import Level

import game.core.person as person_module
import game.world.map as map_module


class FinalLevel(Level):
    def __init__(
        self,
        *,
        name: str,
        map: map_module.Map,
        startX: int,
        startY: int,
        introText: str,
        complete: bool,
        artifactX: int,
        artifactY: int,
    ) -> None:
        super().__init__(
            name=name,
            map=map,
            startX=startX,
            startY=startY,
            introText=introText,
            complete=complete,
        )
        self.artifactX: int = artifactX
        self.artifactY: int = artifactY

    def handleMove(self, person: person_module.Person, direction: str) -> str:
        """TODO: Implement handleMove."""
        raise NotImplementedError("FinalLevel.handleMove is not implemented yet")

    def getArtifactPosition(self) -> tuple[int, int]:
        """TODO: Implement getArtifactPosition."""
        raise NotImplementedError("FinalLevel.getArtifactPosition is not implemented yet")
