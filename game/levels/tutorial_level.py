from game.levels.level import Level

import game.core.person as person_module
import game.world.map as map_module


class TutorialLevel(Level):
    def __init__(
        self,
        *,
        name: str,
        map: map_module.Map,
        startX: int,
        startY: int,
        introText: str,
        complete: bool,
        hints: list[str],
    ) -> None:
        super().__init__(
            name=name,
            map=map,
            startX=startX,
            startY=startY,
            introText=introText,
            complete=complete,
        )
        self.hints: list[str] = hints

    def handleMove(self, person: person_module.Person, direction: str) -> str:
        directions = {
            "up": (0, 1),
            "down": (0, -1),
            "left": (-1, 0),
            "right": (1, 0),
        }
        if direction not in directions:
            return "Invalid direction."

        dx, dy = directions[direction]
        x, y = person.positionX + dx, person.positionY + dy
        if not self.map.inBounds(x, y) or not self.map.isPassable(x, y):
            person.decreaseEnergy(1)
            return "You bumped into a wall."

        person.setPosition(x, y)
        person.decreaseEnergy(1)

        if self.map.getTile(x, y).tileType == "exit":
            self.markComplete()
            return "You reached the exit."


        return "You moved."


    def getHint(self) -> str:
        """TODO: Implement getHint."""
        raise NotImplementedError("TutorialLevel.getHint is not implemented yet")
