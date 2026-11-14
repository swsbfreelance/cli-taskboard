import sys
from typing import List
sys.stdout.reconfigure(encoding='utf-8')

class Task:
    def __init__(self, title: str, priority: int = 1):
        self.title = title
        self.done = False
        self.priority = priority

    @property
    def status(self) -> str:
        return "done" if self.done else "open"

    def complete(self) -> None:
        self.done = True

    def __repr__(self) -> str:
        return f"Task(title={self.title!r}, done={self.done}, priority={self.priority})"

    def __str__(self) -> str:
        return f"[{'✓' if self.done else '✗'}] {self.title} (p{self.priority})"


class ProjectTask(Task):
    def __init__(self, title: str, owner: str, due_date: str, priority: int = 2):
        super().__init__(title, priority)
        self.owner = owner
        self.due_date = due_date

    def __repr__(self) -> str:
        return (f"ProjectTask(title={self.title!r}, owner={self.owner!r}, "
                f"due={self.due_date!r}, done={self.done})")

    def __str__(self) -> str:
        base = super().__str__()
        return f"{base} → {self.owner}, due {self.due_date}"

class Board:
    def __init__(self, name: str):
        self.name = name
        self._tasks: List[Task] = []          # private by convention

    def add(self, task: Task) -> None:
        if not isinstance(task, Task):
            raise TypeError(f"Expected Task, got {type(task).__name__}")
        self._tasks.append(task)

    def filter(self, done: bool | None = None, owner: str | None = None) -> List[Task]:
        results = []
        for t in self._tasks:
            if done is not None and t.done != done:
                continue
            if owner is not None:
                # only ProjectTask has .owner
                if not isinstance(t, ProjectTask) or t.owner != owner:
                    continue
            results.append(t)
        return results

    def to_dict(self) -> list[dict]:
        out = []
        for t in self._tasks:
            d = {"title": t.title, "done": t.done, "priority": t.priority}
            if isinstance(t, ProjectTask):
                d["owner"] = t.owner
                d["due_date"] = t.due_date
            out.append(d)
        return out

    def __repr__(self) -> str:
        return f"Board(name={self.name!r}, tasks={len(self._tasks)})"

    def __str__(self) -> str:
        lines = [f"📋 {self.name} ({len(self._tasks)} tasks)"]
        for t in self._tasks:
            lines.append(f"  {t}")          # calls Task.__str__ or ProjectTask.__str__
        return "\n".join(lines)

    def __len__(self) -> int:
        return len(self._tasks)

'''
t = Task("Write report", priority=3)
print(t)           # [✗] Write report (p3)
print(repr(t))     # Task(title='Write report', done=False, priority=3)
print(t.status)    # open
t.complete()
print(t.status)    # done
print(t)           # [✓] Write report (p3)

tasks = [Task("A"), Task("B"), t]
print(tasks)       # [Task(title='A', ...), Task(title='B', ...), Task(title='Write report', ...)]
                   #  ^ uses __repr__ because it's inside a list

pt = ProjectTask("Ship v1", owner="ali", due_date="2026-11-22")
print(pt)          # [✗] Ship v1 (p2) → ali, due 2026-11-22
print(repr(pt))    # ProjectTask(title='Ship v1', owner='ali', due='2026-11-22', done=False)
print(pt.status)   # open          ← inherited from Task
pt.complete()
print(pt.status)   # done          ← inherited method


b = Board("Sprint 11")
b.add(Task("Read McKinney Ch 5", priority=2))
b.add(ProjectTask("Ship v1", owner="ali", due_date="2026-11-22", priority=3))
b.add(ProjectTask("Write docs", owner="sam", due_date="2026-11-25"))
b.add(Task("Stretch break", priority=1))

print(b)
# 📋 Sprint 11 (4 tasks)
#   [✗] Read McKinney Ch 5 (p2)
#   [✗] Ship v1 (p3) → ali, due 2026-11-22
#   [✗] Write docs (p2) → sam, due 2026-11-25
#   [✗] Stretch break (p1)

print(len(b))              # 4
print(b.filter(done=False))  # [Task(...), ProjectTask(...), ProjectTask(...), Task(...)]
print(b.filter(owner="ali")) # [ProjectTask(title='Ship v1', ...)]
print(b.to_dict())
# [{"title": "Read McKinney Ch 5", "done": False, "priority": 2},
#  {"title": "Ship v1", "done": False, "priority": 3, "owner": "ali", "due_date": "2026-11-22"},
#  ...]
'''