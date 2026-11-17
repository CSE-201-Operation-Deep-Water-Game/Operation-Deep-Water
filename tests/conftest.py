import pytest

from game.core.person import Person
from game.world.map import Map
from game.world.tile import Tile


@pytest.fixture
def person():
    return Person(energyAmt=20, maxEnergy=20, positionX=2, positionY=2)


@pytest.fixture
def world():
    return Map(
        grid=[[Tile(x=x, y=y, tileType='open', landmark='') for x in range(5)] for y in range(5)],
        width=5, height=5,
    )


@pytest.fixture
def level_kwargs(world):
    return dict(name='Test room', map=world, startX=2, startY=2, introText='Entering.', complete=False)
