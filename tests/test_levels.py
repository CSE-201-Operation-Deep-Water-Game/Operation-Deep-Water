import pytest
from unittest.mock import patch
from game.levels.tutorial_level import TutorialLevel
from game.levels.wave_room import WaveRoom
from game.levels.puzzle_level import PuzzleLevel
from game.levels.wave_room_layout import buildWaveRoom, LAYOUT, WAVES, LANDMARKS
from game.world.tile import Tile
from game.world.wave import Wave


@pytest.fixture(params=[TutorialLevel,WaveRoom])
def level(request,level_kwargs):
    extra = {'hints':[]} if request.param is TutorialLevel else {}
    return request.param(**level_kwargs,**extra)


def test_level_start_and_completion(level,person):
    level.markComplete()
    assert level.isComplete()
    person.setPosition(0,0)
    assert level.start(person) == 'Entering.'
    assert person.getPosition() == (2,2)
    assert not level.isComplete()


@pytest.mark.parametrize('direction,destination', [('up',(2,3)),('down',(2,1)),('left',(1,2)),('right',(3,2))])
def test_level_movement(level,person,direction,destination):
    level.handleMove(person,direction)
    assert person.getPosition() == destination
    assert person.getEnergy() == 19


def test_invalid_direction_is_free(level,person):
    assert level.handleMove(person,'diagonal') == 'Invalid direction.'
    assert person.getEnergy() == 20
    assert person.getPosition() == (2,2)


@pytest.mark.parametrize('obstacle',['wall','boundary'])
def test_blocked_move_costs_energy(level,person,world,obstacle):
    if obstacle == 'wall':
        world.setTile(3,2,Tile(x=3,y=2,tileType='wall',landmark='',description='Carved wall.'))
    else:
        person.setPosition(4,2)
    original = person.getPosition()
    assert 'wall' in level.handleMove(person,'right')
    assert person.getPosition() == original
    assert person.getEnergy() == 19


def test_exit_completes_level(level,person,world):
    world.setTile(3,2,Tile(x=3,y=2,tileType='exit',landmark=''))
    assert 'exit' in level.handleMove(person,'right')
    assert level.isComplete()


def test_landing_description(level,person,world):
    world.getTile(3,2).setDescription('Alien pillar.')
    assert 'Alien pillar.' in level.handleMove(person,'right')


def test_wave_push_does_not_chain(level_kwargs,person,world):
    room = WaveRoom(**level_kwargs)
    world.setTile(3,2,Wave(x=3,y=2,direction='up',magnitude=1))
    world.setTile(3,3,Wave(x=3,y=3,direction='left',magnitude=2,description='Marked pillar.'))
    message = room.handleMove(person,'right')
    assert person.getPosition() == (3,3)
    assert person.getEnergy() == 19
    assert 'Marked pillar.' in message


def test_wave_stops_at_exit_before_end_of_push(level_kwargs,person,world):
    room = WaveRoom(**level_kwargs)
    world.setTile(3,2,Wave(x=3,y=2,direction='up',magnitude=2))
    world.setTile(3,3,Tile(x=3,y=3,tileType='exit',landmark=''))
    room.handleMove(person,'right')
    assert person.getPosition() == (3,3)
    assert room.complete


def test_wave_blocked_push_stays_on_wave(level_kwargs,person,world):
    room = WaveRoom(**level_kwargs)
    world.setTile(3,2,Wave(x=3,y=2,direction='right',magnitude=3))
    world.setTile(4,2,Tile(x=4,y=2,tileType='wall',landmark=''))
    room.handleMove(person,'right')
    assert person.getPosition() == (3,2)


def test_wave_layout_builds_coordinates_landmarks_and_independent_maps():
    room = buildWaveRoom()
    other = buildWaveRoom()
    assert (room.map.width,room.map.height) == (12,9)
    assert (room.startX,room.startY) == (0,0)
    for row,text in enumerate(LAYOUT):
        for x,char in enumerate(text):
            y = 8-row
            tile = room.map.getTile(x,y)
            assert (tile.x,tile.y) == (x,y)
            assert tile is not other.map.getTile(x,y)
            if char == '~':
                assert isinstance(tile,Wave)
                assert (tile.direction,tile.magnitude) == WAVES[(x,y)]
            if (x,y) in LANDMARKS:
                assert (tile.getLandmark(),tile.getDescription()) == LANDMARKS[(x,y)]


@pytest.fixture
def puzzle(level_kwargs):
    return PuzzleLevel(**level_kwargs,intersectionX=2,intersectionY=2)


@pytest.mark.parametrize('position,expected', [((2,2),True),((2,1),False),((1,2),False),((0,0),False)])
def test_puzzle_intersection(puzzle,person,position,expected):
    person.setPosition(*position)
    assert puzzle.isAtIntersection(person) is expected


def test_puzzle_wrong_position_does_not_unlock(puzzle,person):
    person.setPosition(1,1)
    with patch.object(puzzle,'unlockEntrance') as unlock:
        puzzle.onSonar(person)
    unlock.assert_not_called()
    assert not puzzle.solved


def test_puzzle_intersection_triggers_unlock(puzzle,person):
    with patch.object(puzzle,'unlockEntrance',return_value='Opened.') as unlock:
        puzzle.onSonar(person)
    unlock.assert_called_once_with()
    assert puzzle.solved


def test_puzzle_unlock_opens_entrance(puzzle,world):
    world.setTile(0,0,Tile(x=0,y=0,tileType='wall',landmark=''))
    message = puzzle.unlockEntrance()
    assert world.isPassable(0,0)
    assert message

