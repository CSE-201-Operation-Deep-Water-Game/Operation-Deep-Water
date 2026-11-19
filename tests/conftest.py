"""Shared test setup. pytest hands these to any test that asks for them by name.

Every test starts from the same simple scene:
  - a 5x5 map of open water
  - the player in the middle at (2, 2) with 20 energy
"""

import pytest

from game.core.person import Person
from game.world.map import Map
from game.world.tile import Tile


@pytest.fixture
def person():
    """A player in the middle of the map with full energy (20)."""
    return Person(energyAmt=20, maxEnergy=20, positionX=2, positionY=2)


@pytest.fixture
def world():
    """A 5x5 map where every tile is open water."""
    grid = []
    for y in range(5):
        row = []
        for x in range(5):
            row.append(Tile(x=x, y=y, tileType="open", landmark=""))
        grid.append(row)
    return Map(grid=grid, width=5, height=5)


@pytest.fixture
def level_kwargs(world):
    """The arguments every level needs. Start position matches the player."""
    return dict(
        name="Test room",
        map=world,
        startX=2,
        startY=2,
        introText="Entering.",
        complete=False,
    )


class FakeUI:
    """A stand-in for the terminal so tests can run without a real keyboard.

    - print() saves what the game says into self.printed
    - prompt() hands back the typed answers we give it, one at a time
    """

    def __init__(self, inputs=()):
        self.printed = []
        self.inputs = list(inputs)
        self.briefing_shown = False

    def print(self, text):
        self.printed.append(text)

    def prompt(self):
        return self.inputs.pop(0)

    def showBriefing(self):
        self.briefing_shown = True

    def said(self):
        """Everything the game printed, joined into one string."""
        return "\n".join(self.printed)
