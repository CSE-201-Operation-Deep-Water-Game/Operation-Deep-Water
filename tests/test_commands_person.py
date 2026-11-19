"""Tests for the command parser (turns typed text into commands) and the Person."""

import pytest

from game.commands.command_parser import CommandParser


@pytest.fixture
def parser():
    # Maps the word the player types to the command it becomes.
    return CommandParser(
        validVerbs={"move": "move", "sonar": "sonar", "quit": "quit", "inspect": "look"}
    )


# ---------- CommandParser ----------

def test_parser_reads_verb_and_direction(parser):
    """'move left' becomes verb 'move' with argument 'left'."""
    command = parser.parse("move left")
    assert command.verb == "move"
    assert command.arg == "left"


def test_parser_ignores_capitals_and_extra_spaces(parser):
    """'  MOVE   LEFT ' is understood the same as 'move left'."""
    command = parser.parse("  MOVE   LEFT ")
    assert command.verb == "move"
    assert command.arg == "left"


def test_parser_lowercases_the_sonar_direction(parser):
    """'sonar UP' must give the direction 'up', same as 'sonar up'."""
    command = parser.parse("sonar UP")
    assert command.verb == "sonar"
    assert command.arg == "up"


def test_parser_treats_a_bare_direction_as_a_move(parser):
    """Typing just 'up' is a shortcut for 'move up'."""
    command = parser.parse("up")
    assert command.verb == "move"
    assert command.arg == "up"


def test_parser_command_with_no_argument(parser):
    """'quit' has no argument, so the argument is empty."""
    command = parser.parse("quit")
    assert command.verb == "quit"
    assert command.arg == ""


def test_parser_uses_the_mapped_verb(parser):
    """Typing 'inspect' gives the 'look' command, as set up in validVerbs."""
    assert parser.parse("inspect pillar").verb == "look"


def test_parser_rejects_nonsense(parser):
    """Unknown words are invalid, and parse() raises an error for them."""
    assert not parser.isValid("nonsense")
    with pytest.raises(ValueError):
        parser.parse("nonsense")


def test_parser_rejects_empty_input(parser):
    """Pressing enter with nothing typed is invalid."""
    assert not parser.isValid("")
    with pytest.raises(ValueError):
        parser.parse("")


# ---------- Person ----------

def test_person_can_change_position(person):
    """setPosition moves the player and getPosition reports it."""
    person.setPosition(1, 4)
    assert person.getPosition() == (1, 4)


def test_person_loses_energy(person):
    """decreaseEnergy(3) takes the player from 20 to 17."""
    person.decreaseEnergy(3)
    assert person.getEnergy() == 17


def test_person_energy_can_be_reset(person):
    """resetEnergy puts the player back to full energy."""
    person.decreaseEnergy(10)
    person.resetEnergy()
    assert person.getEnergy() == 20


def test_person_is_alive_with_energy_left(person):
    """A player with energy left is not dead."""
    person.decreaseEnergy(19)
    assert not person.isDead()


def test_person_dies_at_zero_energy(person):
    """A player with 0 energy is dead."""
    person.decreaseEnergy(20)
    assert person.isDead()


def test_person_sonar_costs_5_energy_and_does_not_move(person, world):
    """Sonar is a scan: it costs 5 energy but the player stays put."""
    person.sonar(world, "up")
    assert person.getEnergy() == 15
    assert person.getPosition() == (2, 2)
