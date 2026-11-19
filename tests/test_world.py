"""Tests for the world: Tile, Map (including sonar) and Wave."""

import pytest

from game.world.tile import Tile
from game.world.wave import Wave


# ---------- Tile ----------

def test_wall_tile_cannot_be_entered():
    tile = Tile(x=0, y=0, tileType="wall", landmark="")
    assert not tile.isPassable()


def test_open_tile_can_be_entered():
    tile = Tile(x=0, y=0, tileType="open", landmark="")
    assert tile.isPassable()


def test_tile_landmark_and_description_can_be_changed():
    """A new tile has no description. setLandmark/setDescription change them."""
    tile = Tile(x=0, y=0, tileType="open", landmark="pillar")
    assert tile.getLandmark() == "pillar"
    assert tile.getDescription() == ""

    tile.setLandmark("arch")
    tile.setDescription("Alien script.")
    assert tile.getLandmark() == "arch"
    assert tile.getDescription() == "Alien script."


# ---------- Map ----------

def test_map_knows_what_is_inside_it(world):
    """The 5x5 map covers x and y from 0 to 4."""
    assert world.inBounds(0, 0)
    assert world.inBounds(4, 4)
    assert not world.inBounds(5, 0)
    assert not world.inBounds(0, -1)


def test_map_rejects_tiles_outside_it(world):
    """Asking for a tile off the map is an error, not a silent mistake."""
    with pytest.raises(IndexError):
        world.getTile(5, 5)


def test_setting_a_tile_gives_it_the_right_coordinates(world):
    """We hand in a tile with wrong coordinates (99, 99); the map fixes them."""
    wall = Tile(x=99, y=99, tileType="wall", landmark="")
    world.setTile(1, 3, wall)

    assert world.getTile(1, 3) is wall
    assert (wall.x, wall.y) == (1, 3)
    assert not world.isPassable(1, 3)


# ---------- Sonar ----------
# Sonar shows a 3x3 picture around the player:
#   S = you, # = wall, E = exit, L = landmark, ~ = wave, . = open water

def test_sonar_shows_player_in_the_middle(world, person):
    """With no direction, sonar is centered on the player."""
    rows = world.sonar(person, "").splitlines()[:3]
    assert rows[1].split()[1] == "S"


def test_sonar_up_looks_further_up(world, person):
    """Sonar 'up' shifts the picture up, so the player is on the bottom row."""
    rows = world.sonar(person, "up").splitlines()[:3]
    assert rows[2].split()[1] == "S"


def test_sonar_left_looks_further_left(world, person):
    """Sonar 'left' shifts the picture left, so the player is on the right."""
    rows = world.sonar(person, "left").splitlines()[:3]
    assert rows[1].split()[2] == "S"


def test_sonar_draws_each_tile_type_with_its_symbol(world, person):
    """Put a wall, exit, wave and landmark around the player and read them back."""
    world.setTile(1, 3, Tile(x=1, y=3, tileType="wall", landmark=""))
    world.setTile(2, 3, Tile(x=2, y=3, tileType="exit", landmark=""))
    world.setTile(3, 3, Tile(x=3, y=3, tileType="wave", landmark=""))
    world.setTile(1, 2, Tile(x=1, y=2, tileType="open", landmark="pillar"))

    rows = world.sonar(person, "").splitlines()[:3]

    # The top row of the picture is the row above the player (y = 3).
    assert rows[0] == "# E ~"
    assert rows[1] == "L S ."
    assert rows[2] == ". . ."


def test_sonar_shows_walls_past_the_edge_of_the_map(world, person):
    """In the bottom-left corner, 5 of the 9 squares are off the map, so they show '#'."""
    person.setPosition(0, 0)
    rows = world.sonar(person, "").splitlines()[:3]
    wall_count = sum(row.split().count("#") for row in rows)
    assert wall_count == 5


# ---------- Wave ----------

def test_wave_pushes_in_its_direction():
    """Each direction pushes the player by one step (dx, dy) at a time."""
    assert Wave(x=0, y=0, direction="up", magnitude=1).getPushVector() == (0, 1)
    assert Wave(x=0, y=0, direction="down", magnitude=1).getPushVector() == (0, -1)
    assert Wave(x=0, y=0, direction="left", magnitude=1).getPushVector() == (-1, 0)
    assert Wave(x=0, y=0, direction="right", magnitude=1).getPushVector() == (1, 0)


def test_wave_is_a_wave_tile():
    wave = Wave(x=0, y=0, direction="up", magnitude=1)
    assert wave.tileType == "wave"


def test_wave_rejects_bad_direction():
    with pytest.raises(ValueError):
        Wave(x=0, y=0, direction="diagonal", magnitude=1)


def test_wave_rejects_negative_magnitude():
    with pytest.raises(ValueError):
        Wave(x=0, y=0, direction="up", magnitude=-1)


def test_wave_pushes_up_to_its_magnitude(world):
    """A strength-2 wave at (1, 2) pushing right carries you 2 tiles."""
    wave = Wave(x=1, y=2, direction="right", magnitude=2)
    assert wave.getPath(world) == [(2, 2), (3, 2)]
    assert wave.getDestination(world) == (3, 2)


def test_wave_stops_at_the_edge_of_the_map(world):
    """A strength-10 wave can only go as far as the map allows."""
    wave = Wave(x=1, y=2, direction="right", magnitude=10)
    assert wave.getDestination(world) == (4, 2)


def test_wave_stops_before_a_wall(world):
    """A wall at (3, 2) stops the push after only one tile."""
    world.setTile(3, 2, Tile(x=3, y=2, tileType="wall", landmark=""))
    wave = Wave(x=1, y=2, direction="right", magnitude=10)
    assert wave.getPath(world) == [(2, 2)]
    assert wave.getDestination(world) == (2, 2)
