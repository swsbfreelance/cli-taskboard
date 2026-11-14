import sys
import json
import logging
from pathlib import Path
from typing import List, Optional, Dict, Any

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

# Make sure ✓ / ✗ print correctly on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


class Task:
    def __init__(self, title: str, priority: int = 1):
        self.title = title
        self.done = False
        self.priority = priority  # 1 = low, 2 = med, 3 = high

    @property
    def status(self) -> str:
        return "done" if self.done else "open"

    def complete(self) -> None:
        self.done = True

    def __repr__(self) -> str:
        return f"Task(title={self.title!r}, done={self.done}, priority={self.priority})"

    def __str__(self) -> str:
        mark = "✓" if self.done else "✗"
        return f"[{mark} {self.title} (p={self.priority})]"


class ProjectTask(Task):
    def __init__(self, title: str, owner: str, due_date: str, priority: int = 2):
        super().__init__(title, priority)  # calls Task.__init__
        self.owner = owner
        self.due_date = due_date  # e.g. "2026-11-20"

    def __repr__(self) -> str:
        return (f"ProjectTask(title={self.title!r}, owner={self.owner!r}, "
                f"due={self.due_date!r}, priority={self.priority})")

    def __str__(self) -> str:
        base = super().__str__()  # reuses Task.__str__
        return f"{base} [{self.owner} . due {self.due_date}]"


class Board:
    def __init__(self, name: str = "Board"):
        self.name = name
        self._tasks: List[Task] = []  # private by convention

    @property
    def tasks(self) -> List[Task]:
        return self._tasks

    def add(self, task: Task) -> None:
        if not isinstance(task, Task):
            raise TypeError(f"Expected Task, got {type(task).__name__}")
        self._tasks.append(task)

    def filter(self, done: Optional[bool] = None, owner: Optional[str] = None) -> List[Task]:
        result = []
        for t in self._tasks:
            if done is not None and t.done != done:
                continue
            if owner is not None:
                if not isinstance(t, ProjectTask):
                    continue  # plain Task has no .owner
                if t.owner != owner:
                    continue
            result.append(t)
        return result

    def to_dict(self) -> List[Dict[str, Any]]:
        out = []
        for t in self._tasks:
            d = {"title": t.title, "done": t.done,
                 "priority": t.priority, "type": "task"}
            if isinstance(t, ProjectTask):
                d["owner"] = t.owner
                d["due_date"] = t.due_date
                d["type"] = "project"
            out.append(d)
        return out

    def __iter__(self):
        return iter(self._tasks)

    def __str__(self) -> str:
        header = f"-- {self.name} ({len(self._tasks)} tasks)"
        if not self._tasks:
            return header + "\n (empty)"
        lines = [f" {t} " for t in self._tasks]
        return "\n".join([header] + lines)

    def __len__(self) -> int:
        return len(self._tasks)


def save_tasks(tasks, path):
    """Write a list (or Board) of Task/ProjectTask objects to a JSON file."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)

    records = []
    for t in tasks:
        d = {"title": t.title, "done": t.done, "priority": t.priority}
        if hasattr(t, "owner"):
            d["owner"] = t.owner
            d["due_date"] = t.due_date
            d["type"] = "project"
        else:
            d["type"] = "task"
        records.append(d)

    p.write_text(json.dumps(records, indent=2), encoding="utf-8")
    logging.info(f"Saved {len(records)} tasks → {p}")


def load_tasks(path):
    """Read a JSON file back into a list of Task / ProjectTask objects."""
    p = Path(path)
    if not p.exists():
        logging.warning(f"{p} not found, starting with empty board")
        return []

    raw = p.read_text(encoding="utf-8")
    try:
        records = json.loads(raw)
    except json.JSONDecodeError:
        logging.error(f"Corrupt JSON in {p}. Back it up and start fresh.")
        return []

    tasks = []
    for d in records:
        # Validate: title must be a non-empty string
        if not d.get("title", "").strip():
            logging.warning(f"Skipping task with empty title: {d}")
            continue

        if d.get("type") == "project":
            task = ProjectTask(
                title=d["title"],
                owner=d.get("owner", "unknown"),
                due_date=d.get("due_date", ""),
                priority=d.get("priority", 2),
            )
        else:
            task = Task(
                title=d["title"],
                priority=d.get("priority", 1),
            )
        task.done = d.get("done", False)  # restore completed state
        tasks.append(task)

    logging.info(f"Loaded {len(tasks)} tasks from {p}")
    return tasks


def load_board(path, name: str = "Board") -> Board:
    """Convenience: load a JSON file straight into a Board."""
    board = Board(name)
    for t in load_tasks(path):
        board.add(t)
    return board


class EmptyBoardError(Exception):
    """Raised when trying to save a board with zero tasks."""
    pass


def safe_save(tasks, path):
    if not tasks:
        raise EmptyBoardError("Board is empty — nothing to save.")
    save_tasks(tasks, path)
