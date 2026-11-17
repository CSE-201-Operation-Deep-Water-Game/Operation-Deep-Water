import pytest
from game.commands.command import Command
from game.commands.command_parser import CommandParser


@pytest.fixture
def parser():
    return CommandParser(validVerbs={'move':'move','sonar':'sonar','quit':'quit','status':'status','inspect':'look'})


@pytest.mark.parametrize('raw,verb,arg', [(' UP ','move','up'),('move LEFT','move','left'),('sonar right','sonar','right'),('quit','quit',''),('inspect ancient pillar','look','ancient pillar')])
def test_parse_commands(parser,raw,verb,arg):
    command = parser.parse(raw)
    assert isinstance(command,Command)
    assert (command.verb,command.arg) == (verb,arg)


@pytest.mark.parametrize('raw', ['', '   ', 'nonsense', 'up extra'])
def test_invalid_commands(parser,raw):
    assert not parser.isValid(raw)
    with pytest.raises(ValueError):
        parser.parse(raw)


def test_person_position_energy_and_reset(person):
    person.setPosition(1,4)
    assert person.getPosition() == (1,4)
    person.decreaseEnergy(3)
    assert person.getEnergy() == 17
    assert not person.isDead()
    person.resetEnergy()
    assert person.getEnergy() == 20


@pytest.mark.parametrize('remaining', [0,-2])
def test_person_death(person,remaining):
    person.decreaseEnergy(20-remaining)
    assert person.isDead()


def test_person_sonar_costs_five_without_moving(person,world):
    result = person.sonar(world,'up')
    assert result == world.sonar(person,'up')
    assert person.getEnergy() == 15
    assert person.getPosition() == (2,2)
