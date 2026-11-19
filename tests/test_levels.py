"""Tests for levels: moving around, the Wave Room, and the Puzzle Level.

Most tests use TutorialLevel because it has the plain, basic movement rules.
The scene (from conftest.py) is a 5x5 open map with the player at (2, 2).
Remember: y grows UP, so 'up' is y + 1.
"""

import pytest

from game.levels.puzzle_level import PuzzleLevel
from game.levels.tutorial_level import TutorialLevel
from game.levels.wave_room import WaveRoom
from game.levels.wave_room_layout import LANDMARKS, LAYOUT, WAVES, buildWaveRoom
from game.world.tile import Tile
from game.world.wave import Wave


@pytest.fixture
def level(level_kwargs):
    """A basic tutorial level on the 5x5 map."""
    return TutorialLevel(**level_kwargs, hints=[])


def make_wall(world, x, y):
    """Turn the tile at (x, y) into a wall."""
    world.setTile(x, y, Tile(x=x, y=y, tileType="wall", landmark=""))


# ---------- Basic movement ----------

def test_move_up_goes_to_y_plus_one(level, person):
    level.handleMove(person, "up")
    assert person.getPosition() == (2, 3)


def test_move_down_goes_to_y_minus_one(level, person):
    level.handleMove(person, "down")
    assert person.getPosition() == (2, 1)


def test_move_left_goes_to_x_minus_one(level, person):
    level.handleMove(person, "left")
    assert person.getPosition() == (1, 2)


def test_move_right_goes_to_x_plus_one(level, person):
    level.handleMove(person, "right")
    assert person.getPosition() == (3, 2)


def test_each_move_costs_1_energy(level, person):
    level.handleMove(person, "right")
    assert person.getEnergy() == 19


def test_invalid_direction_is_free_and_does_not_move(level, person):
    """'diagonal' is not a direction: nothing happens and it costs nothing."""
    message = level.handleMove(person, "diagonal")
    assert message == "Invalid direction."
    assert person.getPosition() == (2, 2)
    assert person.getEnergy() == 20


# ---------- Walls ----------

def test_wall_blocks_the_move(level, person, world):
    make_wall(world, 3, 2)
    level.handleMove(person, "right")
    assert person.getPosition() == (2, 2)


def test_bumping_a_wall_still_costs_energy(level, person, world):
    make_wall(world, 3, 2)
    level.handleMove(person, "right")
    assert person.getEnergy() == 19


def test_cannot_move_off_the_edge_of_the_map(level, person):
    person.setPosition(4, 2)
    level.handleMove(person, "right")
    assert person.getPosition() == (4, 2)


def test_validate_move_only_checks_and_never_moves(level, person, world):
    """validateMove returns a warning message for a wall but changes nothing."""
    make_wall(world, 3, 2)
    message = level.validateMove(person, "right")
    assert message != ""
    assert person.getPosition() == (2, 2)
    assert person.getEnergy() == 20


# ---------- Exit, descriptions, starting ----------

def test_reaching_the_exit_completes_the_level(level, person, world):
    world.setTile(3, 2, Tile(x=3, y=2, tileType="exit", landmark=""))
    level.handleMove(person, "right")
    assert level.isComplete()


def test_landing_on_a_tile_shows_its_description(level, person, world):
    world.getTile(3, 2).setDescription("Alien pillar.")
    message = level.handleMove(person, "right")
    assert "Alien pillar." in message


def test_start_returns_intro_and_puts_player_at_start(level, person):
    person.setPosition(0, 0)
    intro = level.start(person)
    assert intro == "Entering."
    assert person.getPosition() == (2, 2)


def test_start_clears_a_finished_level(level, person):
    """Starting a level again (after dying, for example) resets 'complete'."""
    level.markComplete()
    level.start(person)
    assert not level.isComplete()


# ---------- Wave Room ----------
# A wave tile pushes you one extra time after you step onto it.

def test_wave_pushes_player_after_stepping_on_it(level_kwargs, person, world):
    """Step right onto an 'up' wave of strength 2: you end up 2 tiles higher."""
    room = WaveRoom(**level_kwargs)
    world.setTile(3, 2, Wave(x=3, y=2, direction="up", magnitude=2))
    room.handleMove(person, "right")
    assert person.getPosition() == (3, 4)


def test_wave_does_not_chain_into_a_second_wave(level_kwargs, person, world):
    """The first wave drops you on a second wave. You stay there; no second push."""
    room = WaveRoom(**level_kwargs)
    world.setTile(3, 2, Wave(x=3, y=2, direction="up", magnitude=1))
    world.setTile(3, 3, Wave(x=3, y=3, direction="left", magnitude=2))
    room.handleMove(person, "right")
    assert person.getPosition() == (3, 3)


def test_wave_move_still_costs_only_1_energy(level_kwargs, person, world):
    room = WaveRoom(**level_kwargs)
    world.setTile(3, 2, Wave(x=3, y=2, direction="up", magnitude=2))
    room.handleMove(person, "right")
    assert person.getEnergy() == 19


def test_wave_stops_at_an_exit(level_kwargs, person, world):
    """If the push passes over the exit, you stop on it and the level is done."""
    room = WaveRoom(**level_kwargs)
    world.setTile(3, 2, Wave(x=3, y=2, direction="up", magnitude=2))
    world.setTile(3, 3, Tile(x=3, y=3, tileType="exit", landmark=""))
    room.handleMove(person, "right")
    assert person.getPosition() == (3, 3)
    assert room.isComplete()


def test_wave_blocked_by_a_wall_leaves_player_on_the_wave(level_kwargs, person, world):
    room = WaveRoom(**level_kwargs)
    world.setTile(3, 2, Wave(x=3, y=2, direction="right", magnitude=3))
    make_wall(world, 4, 2)
    room.handleMove(person, "right")
    assert person.getPosition() == (3, 2)


# ---------- The real Wave Room layout ----------

def test_wave_room_is_12_wide_and_9_tall():
    room = buildWaveRoom()
    assert room.map.width == 12
    assert room.map.height == 9


def test_wave_room_starts_in_the_bottom_left():
    room = buildWaveRoom()
    assert (room.startX, room.startY) == (0, 0)


def test_every_wave_symbol_becomes_a_wave_tile():
    """Each '~' in the LAYOUT text must turn into a Wave with the right push."""
    room = buildWaveRoom()
    for row, text in enumerate(LAYOUT):
        for x, symbol in enumerate(text):
            if symbol == "~":
                y = 8 - row  # the first line of LAYOUT is the top row (y = 8)
                tile = room.map.getTile(x, y)
                assert isinstance(tile, Wave)
                assert (tile.direction, tile.magnitude) == WAVES[(x, y)]


def test_every_landmark_is_placed_on_its_tile():
    room = buildWaveRoom()
    for (x, y), (label, description) in LANDMARKS.items():
        tile = room.map.getTile(x, y)
        assert tile.getLandmark() == label
        assert tile.getDescription() == description


def test_each_build_gives_a_fresh_map():
    """Changing one room must not change another one built later."""
    first = buildWaveRoom()
    second = buildWaveRoom()
    assert first.map.getTile(0, 0) is not second.map.getTile(0, 0)


# ---------- Puzzle Level ----------
# Sonar pinged while standing on the "intersection" tile unlocks the entrance.

@pytest.fixture
def puzzle(level_kwargs):
    """A puzzle level whose intersection is the middle tile (2, 2)."""
    return PuzzleLevel(**level_kwargs, intersectionX=2, intersectionY=2)


def test_puzzle_knows_when_player_is_on_the_intersection(puzzle, person):
    person.setPosition(2, 2)
    assert puzzle.isAtIntersection(person)


def test_puzzle_knows_when_player_is_not_on_the_intersection(puzzle, person):
    person.setPosition(2, 1)
    assert not puzzle.isAtIntersection(person)


def test_sonar_away_from_the_intersection_does_not_solve_it(puzzle, person):
    person.setPosition(1, 1)
    puzzle.onSonar(person)
    assert not puzzle.solved


def test_sonar_on_the_intersection_solves_it(puzzle, person):
    person.setPosition(2, 2)
    puzzle.onSonar(person)
    assert puzzle.solved


def test_unlocking_opens_the_walled_entrance(puzzle, world):
    make_wall(world, 0, 0)
    puzzle.unlockEntrance()
    assert world.isPassable(0, 0)
