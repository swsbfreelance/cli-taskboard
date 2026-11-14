""" CLI Task Board - Week 1 capstone """

import argparse
import sys

from rich.console import Console
from rich.table import Table

# Works both as `python -m m1_w1.taskboard` and as `python taskboard.py`
try:
    from .task import Task, load_board, save_tasks
except ImportError:
    from task import Task, load_board, save_tasks

console = Console()

TASKS_FILE = "tasks.json"
PRIORITY = {"low": 1, "med": 2, "high": 3}
LABEL = {v: k for k, v in PRIORITY.items()}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="taskboard",
        description="A small CLI task manager"
    )

    sub = parser.add_subparsers(dest="command", help="Available commands")

    # add
    p_add = sub.add_parser("add", help="Add a new task")
    p_add.add_argument("title", help="Task Title")
    p_add.add_argument("--priority", default="med", choices=["high", "med", "low"])

    # list
    sub.add_parser("list", help="List all tasks")

    # done
    p_done = sub.add_parser("done", help="Mark a task as done")
    p_done.add_argument("id", type=int, help="Task ID (the number shown by 'list')")

    # save
    sub.add_parser("save", help="Save board to tasks.json")

    # load
    sub.add_parser("load", help="Load board from tasks.json")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    # load existing board (or start empty)
    board = load_board(TASKS_FILE)

    if args.command == "add":
        task = Task(title=args.title, priority=PRIORITY[args.priority])
        board.add(task)
        save_tasks(board, TASKS_FILE)
        console.print(f"[green]✓ Added:[/green] {task.title}")

    elif args.command == "list":
        if len(board) == 0:
            console.print("[yellow]No tasks yet.[/yellow]")
            return
        table = Table(title="Tasks")
        table.add_column("ID", justify="right")
        table.add_column("Title")
        table.add_column("Priority")
        table.add_column("Done", justify="center")
        for i, t in enumerate(board.tasks, start=1):
            table.add_row(
                str(i),
                t.title,
                LABEL.get(t.priority, str(t.priority)),
                "[green]✓[/green]" if t.done else "-",
            )
        console.print(table)

    elif args.command == "done":
        idx = args.id - 1
        if 0 <= idx < len(board):
            board.tasks[idx].complete()
            save_tasks(board, TASKS_FILE)
            console.print(f"[green]✓ Done:[/green] {board.tasks[idx].title}")
        else:
            console.print(f"[red]No task with id {args.id}[/red]")
            sys.exit(1)

    elif args.command == "save":
        save_tasks(board, TASKS_FILE)
        console.print(f"[green]✓[/green] Saved {len(board)} tasks.")

    elif args.command == "load":
        console.print(f"[green]✓ Loaded[/green] {len(board)} tasks.")


if __name__ == "__main__":
    main()
