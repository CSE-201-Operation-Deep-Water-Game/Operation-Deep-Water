"""Tests for the real Puzzle Room (built by buildPuzzleRoom in puzzle_room_layout.py).

The idea of the room:
  - 4 landmarks sit in the corners of a rectangle.
  - Imagine lines joining opposite landmarks. They cross in an X at (5, 4).
  - Sending sonar from the crossing tile unlocks the exit at (9, 8).
  - Stepping on a landmark recharges your energy (once per landmark).
"""

from game.levels.puzzle_room_layout import LANDMARKS, buildPuzzleRoom

EXIT = (9, 8)       # the sealed exit, top right
CROSSING = (5, 4)   # where the two diagonals cross
STAND_NEXT_TO_EXIT = (9, 7)


# ---------- Layout ----------

def test_room_has_exactly_four_landmarks():
    assert len(LANDMARKS) == 4


def test_each_landmark_has_its_text_on_the_map():
    room = buildPuzzleRoom()
    for (x, y), (label, description) in LANDMARKS.items():
        tile = room.map.getTile(x, y)
        assert tile.landmark == label
        assert tile.description == description


def test_the_crossing_tile_is_open_but_has_no_landmark():
    """The crossing is the secret: nothing on the map marks it."""
    room = buildPuzzleRoom()
    tile = room.map.getTile(*CROSSING)
    assert tile.isPassable()
    assert tile.landmark == ""


# ---------- Solving the puzzle ----------

def test_exit_starts_sealed():
    room = buildPuzzleRoom()
    assert not room.map.isPassable(*EXIT)


def test_sonar_away_from_the_crossing_leaves_exit_sealed(person):
    room = buildPuzzleRoom()
    room.start(person)
    person.setPosition(1, 1)
    room.onSonar(person)
    assert not room.solved
    assert not room.map.isPassable(*EXIT)


def test_sonar_on_the_crossing_unlocks_the_exit(person):
    room = buildPuzzleRoom()
    room.start(person)
    person.setPosition(*CROSSING)
    message = room.onSonar(person)
    assert room.solved
    assert room.map.getTile(*EXIT).tileType == "exit"
    assert "unlocked" in message


def test_walking_into_the_sealed_exit_does_not_finish_the_level(person):
    room = buildPuzzleRoom()
    room.start(person)
    person.setPosition(*STAND_NEXT_TO_EXIT)
    room.handleMove(person, "up")
    assert person.getPosition() == STAND_NEXT_TO_EXIT
    assert not room.isComplete()


def test_walking_into_the_unlocked_exit_finishes_the_level(person):
    room = buildPuzzleRoom()
    room.start(person)
    person.setPosition(*CROSSING)
    room.onSonar(person)
    person.setPosition(*STAND_NEXT_TO_EXIT)
    room.handleMove(person, "up")
    assert room.isComplete()


def test_restarting_the_room_seals_the_exit_again(person):
    room = buildPuzzleRoom()
    room.start(person)
    person.setPosition(*CROSSING)
    room.onSonar(person)

    room.start(person)

    assert not room.solved
    assert not room.map.isPassable(*EXIT)


# ---------- Landmarks recharge energy ----------

def test_stepping_on_a_landmark_refills_energy(person):
    room = buildPuzzleRoom()
    room.start(person)
    person.setPosition(1, 2)          # next to the landmark at (2, 2)
    room.handleMove(person, "right")  # step onto it
    assert person.getEnergy() == person.maxEnergy


def test_a_landmark_only_recharges_once(person):
    """Leave and come back: the second visit gives nothing (just the 2 move costs)."""
    room = buildPuzzleRoom()
    room.start(person)
    person.setPosition(1, 2)
    room.handleMove(person, "right")  # recharges to full
    room.handleMove(person, "left")   # -1
    room.handleMove(person, "right")  # -1, no recharge this time
    assert person.getEnergy() == person.maxEnergy - 2


def test_restarting_makes_landmarks_recharge_again(person):
    room = buildPuzzleRoom()
    room.start(person)
    person.setPosition(1, 2)
    room.handleMove(person, "right")

    room.start(person)
    person.setPosition(1, 2)
    person.decreaseEnergy(5)
    room.handleMove(person, "right")

    assert person.getEnergy() == person.maxEnergy
