"""Tests for the GameController (runs the game) and the terminal screen.

The controller normally talks to a real terminal. Here we give it a FakeUI
(see conftest.py) that records what the game prints and feeds it typed answers.
"""

from conftest import FakeUI
from game.commands.command import Command
from game.commands.command_parser import CommandParser
from game.core.checkpoint_manager import CheckpointManager
from game.core.game_controller import GameController
from game.levels.tutorial_level import TutorialLevel
from game.ui.terminal_interface import TerminalInterface


def make_controller(person, level_kwargs, typed_inputs=()):
    """Build a controller with one level and a FakeUI that 'types' typed_inputs."""
    level = TutorialLevel(**level_kwargs, hints=[])
    ui = FakeUI(inputs=typed_inputs)
    ui.parser = CommandParser(validVerbs={"quit": "quit", "move": "move", "sonar": "sonar"})
    return GameController(
        person=person,
        levels=[level],
        currentLevel=level,
        ui=ui,
        checkpoints=CheckpointManager(passwords={}),
        running=True,
    )


# ---------- Commands ----------

def test_move_prints_the_landmark_you_arrive_at(person, level_kwargs):
    controller = make_controller(person, level_kwargs)
    controller.currentLevel.map.getTile(3, 2).setLandmark("Pillar")

    controller.handleCommand(Command(verb="move", arg="right"))

    assert "Pillar" in controller.ui.said()


def test_move_prints_the_remaining_energy(person, level_kwargs):
    controller = make_controller(person, level_kwargs)

    controller.handleCommand(Command(verb="move", arg="right"))

    assert "Energy: 19" in controller.ui.said()


def test_bumping_a_wall_does_not_repeat_the_landmark_you_stand_on(person, level_kwargs):
    """You are on a landmark at the corner and walk into the map edge: no new landmark."""
    controller = make_controller(person, level_kwargs)
    person.setPosition(0, 0)
    controller.currentLevel.map.getTile(0, 0).setLandmark("Pillar")

    controller.handleCommand(Command(verb="move", arg="left"))

    assert "Pillar" not in controller.ui.said()


def test_sonar_costs_5_energy(person, level_kwargs):
    controller = make_controller(person, level_kwargs)

    controller.handleCommand(Command(verb="sonar", arg="up"))

    assert person.getEnergy() == 15
    assert "Energy: 15" in controller.ui.said()


def test_status_shows_energy_and_costs_nothing(person, level_kwargs):
    controller = make_controller(person, level_kwargs)

    controller.handleCommand(Command(verb="status", arg=""))

    assert "20" in controller.ui.said()
    assert person.getEnergy() == 20


def test_quit_stops_the_game(person, level_kwargs):
    controller = make_controller(person, level_kwargs)

    controller.handleCommand(Command(verb="quit", arg=""))

    assert not controller.running


# ---------- Death ----------

def test_running_out_of_energy_asks_to_restart(person, level_kwargs):
    controller = make_controller(person, level_kwargs, typed_inputs=["no"])
    person.energyAmt = 1  # one move away from dying

    controller.handleCommand(Command(verb="move", arg="right"))

    assert "You died" in controller.ui.said()


def test_answering_yes_restarts_the_level(person, level_kwargs):
    controller = make_controller(person, level_kwargs, typed_inputs=["yes"])
    person.setPosition(0, 0)
    person.decreaseEnergy(20)

    controller.handleDeath()

    assert controller.running
    assert person.getEnergy() == 20
    assert person.getPosition() == (2, 2)  # back at the level start


def test_answering_no_ends_the_game(person, level_kwargs):
    controller = make_controller(person, level_kwargs, typed_inputs=["no"])

    controller.handleDeath()

    assert not controller.running


def test_a_bad_answer_asks_again(person, level_kwargs):
    controller = make_controller(person, level_kwargs, typed_inputs=["banana", "no"])

    controller.handleDeath()

    assert "Please enter yes or no." in controller.ui.said()


# ---------- Levels and ending ----------

def test_advancing_moves_to_the_next_level(person, level_kwargs):
    controller = make_controller(person, level_kwargs)
    next_level = TutorialLevel(**dict(level_kwargs, startX=1, startY=1), hints=[])
    controller.levels.append(next_level)

    controller.advanceLevel()

    assert controller.currentLevel is next_level


def test_advancing_resets_energy_and_position(person, level_kwargs):
    controller = make_controller(person, level_kwargs)
    next_level = TutorialLevel(**dict(level_kwargs, startX=1, startY=1), hints=[])
    controller.levels.append(next_level)
    person.decreaseEnergy(7)

    controller.advanceLevel()

    assert person.getEnergy() == 20
    assert person.getPosition() == (1, 1)


def test_finishing_the_last_level_wins_the_game(person, level_kwargs):
    controller = make_controller(person, level_kwargs)

    controller.advanceLevel()  # there is no next level

    assert not controller.running
    assert "Mission complete" in controller.ui.said()


def test_losing_ending_says_the_mission_failed(person, level_kwargs):
    controller = make_controller(person, level_kwargs)

    controller.endGame(False)

    assert not controller.running
    assert "failed" in controller.ui.said()


# ---------- The game loop ----------

def test_unknown_input_prints_help_and_the_game_keeps_going(person, level_kwargs):
    """The player types nonsense, then 'quit'. The game must survive the nonsense."""
    controller = make_controller(person, level_kwargs, typed_inputs=["blah", "quit"])

    controller.run()

    assert "Unrecognized command" in controller.ui.said()
    assert not controller.running


def test_start_shows_the_briefing_and_the_level_intro(person, level_kwargs):
    controller = make_controller(person, level_kwargs, typed_inputs=["quit"])

    controller.start()

    assert controller.ui.briefing_shown
    assert "Entering." in controller.ui.said()


# ---------- TerminalInterface (the real screen) ----------

def test_terminal_prints_text(capsys):
    ui = TerminalInterface(parser=CommandParser(validVerbs={}))

    ui.print("hello")

    assert capsys.readouterr().out == "hello\n"


def test_terminal_prompt_returns_what_the_player_typed(monkeypatch):
    ui = TerminalInterface(parser=CommandParser(validVerbs={}))
    monkeypatch.setattr("builtins.input", lambda prompt: "sonar up")

    assert ui.prompt() == "sonar up"


def test_terminal_briefing_mentions_the_mission(capsys):
    ui = TerminalInterface(parser=CommandParser(validVerbs={}))

    ui.showBriefing()

    assert "NAYRB" in capsys.readouterr().out
