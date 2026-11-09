from __future__ import annotations

from game.levels.level import Level
from game.world.wave import Wave

import game.core.person as person_module
import game.world.map as map_module


class WaveRoom(Level):
    """A room full of currents. Stepping on a Wave tile pushes the player on.

    Movement follows the tutorial: every move attempt costs 1 energy and
    walking into a wall or off the map leaves the player in place. If the
    player lands on a Wave tile, the wave carries them further. A push only
    happens once per move (waves do not chain), and if the push passes over or
    ends on an exit tile the level is complete.
    """

    DIRECTIONS: dict[str, tuple[int, int]] = {
        "up": (0, 1),
        "down": (0, -1),
        "left": (-1, 0),
        "right": (1, 0),
    }

    def __init__(
        self,
        *,
        name: str,
        map: map_module.Map,
        startX: int,
        startY: int,
        introText: str,
        complete: bool,
    ) -> None:
        super().__init__(
            name=name,
            map=map,
            startX=startX,
            startY=startY,
            introText=introText,
            complete=complete,
        )

    def handleMove(self, person: person_module.Person, direction: str) -> str:
        if direction not in self.DIRECTIONS:
            return "Invalid direction."

        dx, dy = self.DIRECTIONS[direction]
        x, y = person.positionX + dx, person.positionY + dy
        person.decreaseEnergy(1)

        if not self.map.inBounds(x, y):
            return "You bumped into a wall."

        tile = self.map.getTile(x, y)
        if not tile.isPassable():
            message = "You bumped into a wall."
            if tile.getDescription():
                message += f" {tile.getDescription()}"
            return message

        person.setPosition(x, y)

        if tile.tileType == "exit":
            self.markComplete()
            return "You reached the exit."

        if isinstance(tile, Wave):
            return self.applyCurrent(person, tile)

        if tile.getDescription():
            return f"You moved. {tile.getDescription()}"

        return "You moved."

    def applyCurrent(self, person: person_module.Person, wave: Wave) -> str:
        """Carry the player along the wave's path and report what they feel.

        Passing over an exit tile stops the push there and completes the
        level. Otherwise the player ends on the last open tile of the path,
        and the message stays vague so they must work out where they are.
        """
        path = wave.getPath(self.map)

        for x, y in path:
            if self.map.getTile(x, y).tileType == "exit":
                person.setPosition(x, y)
                self.markComplete()
                return f"{wave.getPushMessage()}\nThe current sweeps you to the exit."

        if path:
            person.setPosition(path[-1][0], path[-1][1])

        return f"You moved.\n{wave.getPushMessage()}"
