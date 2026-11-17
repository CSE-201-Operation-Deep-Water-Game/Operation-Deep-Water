import pytest

from game.world.tile import Tile
from game.world.wave import Wave


@pytest.mark.parametrize('kind,passable', [('wall', False), ('open', True), ('wave', True), ('exit', True)])
def test_tile_passability(kind, passable):
    assert Tile(x=0, y=0, tileType=kind, landmark='').isPassable() is passable


def test_tile_landmark_and_description():
    tile = Tile(x=0, y=0, tileType='open', landmark='pillar')
    assert tile.getLandmark() == 'pillar'
    assert tile.getDescription() == ''
    tile.setLandmark('arch')
    tile.setDescription('Alien script.')
    assert tile.getLandmark() == 'arch'
    assert tile.getDescription() == 'Alien script.'


@pytest.mark.parametrize('x,y,inside', [(0,0,True),(4,4,True),(-1,0,False),(0,-1,False),(5,0,False),(0,5,False)])
def test_map_bounds(world, x, y, inside):
    assert world.inBounds(x,y) is inside
    if not inside:
        with pytest.raises(IndexError):
            world.getTile(x,y)
        with pytest.raises(IndexError):
            world.setTile(x,y,Tile(x=0,y=0,tileType='open',landmark=''))


def test_map_replacement_updates_coordinates(world):
    tile = Tile(x=99,y=99,tileType='wall',landmark='')
    world.setTile(1,3,tile)
    assert world.getTile(1,3) is tile
    assert (tile.x,tile.y) == (1,3)
    assert not world.isPassable(1,3)


@pytest.mark.parametrize('direction,row,column', [('',1,1),('up',2,1),('down',0,1),('left',1,2),('right',1,0)])
def test_sonar_direction_and_dimensions(world, person, direction, row, column):
    person.setPosition(3,1)  # Unequal coordinates catch mixed x/y range bounds.
    rows = world.sonar(person,direction).splitlines()[:3]
    assert len(rows) == 3
    assert all(len(line.split()) == 3 for line in rows)
    assert rows[row].split()[column] == 'S'


def test_sonar_symbols_and_orientation(world, person):
    for x,y,kind,landmark in [(1,3,'wall',''),(2,3,'exit',''),(3,3,'wave',''),(1,2,'open','pillar'),(3,1,'unknown','')]:
        world.setTile(x,y,Tile(x=x,y=y,tileType=kind,landmark=landmark))
    assert world.sonar(person,'').splitlines()[:3] == ['# E ~','L S .','. . ?']


@pytest.mark.parametrize('position', [(0,0),(0,4),(4,0),(4,4)])
def test_sonar_edges_are_walls(world, person, position):
    person.setPosition(*position)
    rows = world.sonar(person,'').splitlines()[:3]
    assert sum(row.split().count('#') for row in rows) == 5
    assert rows[1].split()[1] == 'S'


@pytest.mark.parametrize('direction,vector', [('UP',(0,1)),('down',(0,-1)),('left',(-1,0)),('right',(1,0))])
def test_wave_vectors(direction, vector):
    wave = Wave(x=2,y=2,direction=direction,magnitude=1)
    assert wave.getPushVector() == vector
    assert wave.tileType == 'wave'


@pytest.mark.parametrize('magnitude', [-1,True,1.5,'2'])
def test_wave_rejects_invalid_magnitude(magnitude):
    with pytest.raises(ValueError):
        Wave(x=0,y=0,direction='up',magnitude=magnitude)


def test_wave_rejects_invalid_direction():
    with pytest.raises(ValueError):
        Wave(x=0,y=0,direction='diagonal',magnitude=1)


def test_wave_path_stops_at_boundary_and_wall(world):
    wave = Wave(x=1,y=2,direction='right',magnitude=10,message='Current!')
    assert wave.getPath(world) == [(2,2),(3,2),(4,2)]
    assert wave.getDestination(world) == (4,2)
    world.setTile(3,2,Tile(x=3,y=2,tileType='wall',landmark=''))
    assert wave.getPath(world) == [(2,2)]
    world.setTile(2,2,Tile(x=2,y=2,tileType='wall',landmark=''))
    assert wave.getPath(world) == []
    assert wave.getDestination(world) == (1,2)
    assert wave.getPushMessage() == 'Current!'


def test_zero_magnitude_wave(world):
    wave = Wave(x=2,y=2,direction='up',magnitude=0)
    assert wave.getPath(world) == []
    assert wave.getDestination(world) == (2,2)
