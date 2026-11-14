import sys
from typing import List
sys.stdout.reconfigure(encoding='utf-8')
from datetime import date
from typing import List, Optional, Dict, Any

class Task:
    def __init__(self, title: str, priority:int =1):
        self.title = title
        self.done = False
        self.priority = priority # 1 = low, 2 = med, 3 = high

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
    def __init__(self, title:str, owner:str, due_date:str, priority : int=2):
        super().__init__(title, priority)   # calls Task.__init__
        self.owner = owner
        self.due_date = due_date            # "2026-11-20" for now

    def __repr__(self) -> str:
        return (f'ProjectTasks(title={self.title!r}, owner={self.owner!r}, '
                f'due={self.due_date!r}, priority={self.priority})')

    def __str__(self) -> str:
        base = super().__str__()            # reuses Task.__str__
        return f"{base} [{self.owner} . due {self.due_date}]"
    
class Board:
    def __init__(self, name:str = "Board"):
        self.name = name
        self._tasks: List[Task] = []   # private by convention

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
                    continue    # plain Task has no .owner
                if t.owner != owner:
                    continue
        return result

    def to_dict(self)-> List[Dict[str,Any]]:
        out = []
        for t in self._tasks:
            d = {'title':t.title, "done": t.done,
                 "priority":t.priority, "type": "task"}
            if isinstance(t, ProjectTask):
                d["owner"] = t.owner
                d["due_date"] = t.due_date
                d["type"] = "project"
            out.append
        return out

    def __str__(self) -> str:
        header = f"-- {self.name} ({len(self._tasks)} tasks)"
        if not self._tasks:
            return header + "\n (empty)"
        lines = [f" {t} " for t in self._tasks]
        return "\n".join([header] + lines)

    def __len__(self) -> int:
        return len(self._tasks) 

"""
t1 = Task("Buy milk", priority=2)
#print(t1)
t2 = Task("Read Ch 9", priority=3)
t3 = Task("Stretch")
print([t1,t2,t3])

t1.complete()
print(t1)

print(t1.status)
print(t1.status)

pt = ProjectTask("Ship W2 pipeline", owner="ali",due_date="2026-11-20", priority=3)

print(pt.status)
pt.complete()
print(pt.status)
print([pt,t1])
print(isinstance(pt, Task))
print(isinstance(t1,ProjectTask))

"""
'''
b = Board("Sprint 11")
b.add(Task("Buy Milk", priority=2))
b.add(ProjectTask("Ship W2 pipeline", owner="ali",due_date="2026-11-20", priority=3))
b.add(Task("Stretch"))

print(b)

print(len(b))
print(b.filter(done=False))
print(b.filter(owner="ali"))

print(b.to_dict())
#b.add(42)
'''