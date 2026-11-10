from unittest.mock import Mock, patch
import pytest
import main
from game.commands.command import Command
from game.commands.command_parser import CommandParser
from game.core.game_controller import GameController
from game.core.checkpoint_manager import CheckpointManager
from game.levels.tutorial_level import TutorialLevel
from game.ui.terminal_interface import TerminalInterface


@pytest.fixture
def controller(person,level_kwargs):
    level = TutorialLevel(**level_kwargs,hints=[])
    ui = Mock(spec=TerminalInterface)
    ui.parser = CommandParser(validVerbs={'quit':'quit','move':'move','sonar':'sonar'})
    return GameController(person=person,levels=[level],currentLevel=level,ui=ui,
                          checkpoints=CheckpointManager(passwords={}),running=True)


def output(controller):
    return '\n'.join(call.args[0] for call in controller.ui.print.call_args_list)


def test_controller_move_reports_new_landmark(controller):
    controller.currentLevel.map.getTile(3,2).setLandmark('Pillar')
    controller.handleCommand(Command(verb='move',arg='right'))
    assert 'Pillar' in output(controller)
    assert 'Energy: 19' in output(controller)


def test_controller_blocked_move_does_not_repeat_current_landmark(controller):
    controller.person.setPosition(0,0)
    controller.currentLevel.map.getTile(0,0).setLandmark('Pillar')
    controller.handleCommand(Command(verb='move',arg='left'))
    assert 'Pillar' not in output(controller)


def test_controller_sonar_uses_person_and_charges_energy(controller):
    controller.handleCommand(Command(verb='sonar',arg='up'))
    assert controller.person.getEnergy() == 15
    assert 'S: submarine' in output(controller)
    assert 'Energy: 15' in output(controller)


def test_status_does_not_cost_energy(controller):
    controller.handleCommand(Command(verb='status',arg=''))
    assert controller.person.getEnergy() == 20
    assert '20' in output(controller)


@pytest.mark.parametrize('verb',['quit','end'])
def test_quit_does_not_prompt_for_restart(controller,verb):
    controller.person.decreaseEnergy(20)
    controller.handleCommand(Command(verb=verb,arg=''))
    assert not controller.running
    controller.ui.prompt.assert_not_called()


@pytest.mark.parametrize('verb,arg,energy',[('move','right',1),('sonar','up',5)])
def test_energy_consuming_commands_trigger_death(controller,verb,arg,energy):
    controller.person.energyAmt = energy
    with patch.object(controller,'handleDeath') as death:
        controller.handleCommand(Command(verb=verb,arg=arg))
    death.assert_called_once_with()


def test_advance_level_resets_energy_and_position(controller,level_kwargs):
    next_level = TutorialLevel(**dict(level_kwargs,startX=1,startY=1),hints=[])
    controller.levels.append(next_level)
    controller.person.decreaseEnergy(7)
    controller.advanceLevel()
    assert controller.currentLevel is next_level
    assert controller.person.getPosition() == (1,1)
    assert controller.person.getEnergy() == 20


def test_last_level_ends_game(controller):
    controller.advanceLevel()
    assert not controller.running
    assert 'Mission complete' in output(controller)


@pytest.mark.parametrize('won,fragment',[(True,'Mission complete'),(False,'failed')])
def test_end_game(controller,won,fragment):
    controller.endGame(won)
    assert not controller.running
    assert fragment in output(controller)


def test_death_restart_resets_all_levels(controller):
    controller.currentLevel.complete = True
    controller.person.decreaseEnergy(20)
    controller.ui.prompt.side_effect = ['invalid','yes']
    controller.handleDeath()
    assert controller.running
    assert controller.person.getEnergy() == 20
    assert not controller.currentLevel.complete
    assert controller.person.getPosition() == (2,2)


def test_death_declining_restart_stops_game(controller):
    controller.ui.prompt.return_value = 'no'
    controller.handleDeath()
    assert not controller.running


def test_run_recovers_from_invalid_input(controller):
    controller.ui.prompt.side_effect = ['unknown','quit']
    controller.run()
    assert 'Unrecognized command' in output(controller)
    assert not controller.running


def test_start_initializes_before_running(controller):
    controller.person.decreaseEnergy(8)
    controller.currentLevel.complete = True
    with patch.object(controller,'run') as run:
        controller.start()
    run.assert_called_once_with()
    assert controller.person.getEnergy() == 20
    assert not controller.currentLevel.complete
    controller.ui.showBriefing.assert_called_once_with()


def test_terminal_print_prompt_and_briefing(capsys,monkeypatch):
    ui = TerminalInterface(parser=CommandParser(validVerbs={}))
    ui.print('hello')
    assert capsys.readouterr().out == 'hello\n'
    monkeypatch.setattr('builtins.input',lambda prompt: 'sonar up' if prompt == '> ' else '')
    assert ui.prompt() == 'sonar up'
    ui.showBriefing()
    briefing = capsys.readouterr().out
    assert 'NAYRB' in briefing and 'sonar' in briefing


def test_main_builds_playable_levels_without_starting_input():
    with patch.object(main.GameController,'start',autospec=True) as start:
        main.main()
    game = start.call_args.args[0]
    assert game.currentLevel is game.levels[0]
    assert len(game.levels) >= 2
    assert game.ui.parser.parse('sonar up').arg == 'up'
    for level in game.levels:
        assert level.map.inBounds(level.startX,level.startY)
        assert level.map.isPassable(level.startX,level.startY)
