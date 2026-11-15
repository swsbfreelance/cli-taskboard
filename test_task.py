import pytest

from task import Board, Task, ProjectTask, save_tasks, load_board


def test_add_task():
    board = Board("Sprint")
    assert len(board) == 0

    plain = Task("Write docs", priority=1)
    project = ProjectTask("Ship v1", owner="Ali", due_date="2026-11-20")

    board.add(plain)
    board.add(project)

    assert len(board) == 2
    assert board.tasks == [plain, project]

    # Only Task (or subclass) instances are accepted
    with pytest.raises(TypeError):
        board.add("not a task")
    assert len(board) == 2


def test_board_to_dict_roundtrip(tmp_path):
    board = Board("Roundtrip")
    board.add(Task("Plain task", priority=3))

    done_task = ProjectTask("Finish report", owner="Sara",
                            due_date="2026-11-30", priority=3)
    done_task.complete()
    board.add(done_task)

    original = board.to_dict()

    # Save to JSON and load it back into a new board
    path = tmp_path / "tasks.json"
    save_tasks(board, path)
    restored = load_board(path, "Roundtrip")

    assert restored.to_dict() == original
    assert len(restored) == len(board)

    # Spot-check types and restored state
    assert type(restored.tasks[0]) is Task
    assert isinstance(restored.tasks[1], ProjectTask)
    assert restored.tasks[1].done is True
    assert restored.tasks[1].owner == "Sara"