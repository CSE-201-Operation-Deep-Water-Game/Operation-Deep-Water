from game.commands.command import Command
from unittest.mock import Mock
from game.core.game_controller import GameController
from game.levels.puzzle_room_layout import buildPuzzleRoom, LANDMARKS


def test_four_landmarks_and_unmarked_crossing():
    room = buildPuzzleRoom()
    assert len(LANDMARKS) == 4
    for (x, y), (label, description) in LANDMARKS.items():
        tile = room.map.getTile(x, y)
        assert tile.isPassable()
        assert (tile.landmark, tile.description) == (label, description)
        assert (10 - x, 8 - y) in LANDMARKS
    center = room.map.getTile(room.intersectionX, room.intersectionY)
    assert center.isPassable() and not center.landmark


def test_puzzle_sonar_controller_and_restart(person):
    room = buildPuzzleRoom()
    controller = GameController(person=person, levels=[room], currentLevel=room,
                                ui=Mock(), checkpoints=Mock(), running=True)
    room.start(controller.person)
    controller.handleCommand(Command(verb='sonar', arg='up'))
    assert not room.solved
    assert not room.map.isPassable(9, 8)
    controller.person.setPosition(9, 7)
    room.handleMove(controller.person, 'up')
    assert controller.person.getPosition() == (9, 7)
    assert not room.complete
    controller.person.setPosition(5, 4)
    controller.handleCommand(Command(verb='sonar', arg='left'))
    assert room.solved and not room.complete
    assert room.map.getTile(9, 8).tileType == 'exit'
    assert 'exit is unlocked' in controller.ui.print.call_args.args[0]
    controller.person.setPosition(9, 7)
    room.handleMove(controller.person, 'up')
    assert room.complete
    room.start(controller.person)
    assert not room.solved and not room.complete
    assert not room.map.isPassable(9, 8)
    assert 'sealed' in room.map.getTile(9, 8).description
    assert not buildPuzzleRoom().map.isPassable(9, 8)


def path_to(room, start, goal):
    from collections import deque
    queue = deque([(start, [])])
    seen = {start}
    for_position = {'up': (0, 1), 'down': (0, -1),
                    'left': (-1, 0), 'right': (1, 0)}
    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == goal:
            return path
        for direction, (dx, dy) in for_position.items():
            next_position = (x + dx, y + dy)
            if (next_position not in seen and room.map.inBounds(*next_position)
                    and room.map.isPassable(*next_position)):
                seen.add(next_position)
                queue.append((next_position, path + [direction]))
    raise AssertionError(f'Unreachable tile: {goal}')


def test_exploring_all_clues_and_solving_fits_energy_budget(person):
    room = buildPuzzleRoom()
    room.start(person)
    assert (room.map.width, room.map.height) == (11, 9)
    moves = 0
    for goal in [(2, 2), (2, 6), (8, 6), (8, 2), (5, 4)]:
        # Allow a scouting pulse while searching for each landmark.
        if goal in LANDMARKS:
            person.sonar(room.map, 'up')
        for direction in path_to(room, person.getPosition(), goal):
            room.handleMove(person, direction)
            moves += 1
            assert not person.isDead()
    person.sonar(room.map, '')
    room.onSonar(person)
    assert not person.isDead()
    for direction in path_to(room, person.getPosition(), (9, 8)):
        room.handleMove(person, direction)
        assert not person.isDead()
    assert room.complete
    assert moves > 20
    assert len(room.usedPowerCells) == 4


def test_power_cells_only_recharge_once_and_reset_on_restart(person):
    room = buildPuzzleRoom()
    room.start(person)
    person.setPosition(1, 2)
    room.handleMove(person, 'right')
    assert person.getEnergy() == person.maxEnergy
    room.handleMove(person, 'left')
    room.handleMove(person, 'right')
    assert person.getEnergy() == person.maxEnergy - 2
    room.start(person)
    person.setPosition(1, 2)
    room.handleMove(person, 'right')
    assert person.getEnergy() == person.maxEnergy
