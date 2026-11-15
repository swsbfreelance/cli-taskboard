# CLI Task Board

A small command-line task manager built during week 1 of an AI-Engineering learning path. Python 3.11+, 'argparse','rich'.

## What it does

- 'add' a task with an optional priority
- 'list' all tasks in a coloured table
- 'done' mark a task complete by ID
- 'save' / 'load' presist to 'tasks.json'

## install
```bash \ cmd
git clone https://github.com/swsbfreelance/cli-taskboard
cd ai-journey
python -m venv .venv
[bash] - source .venv/bin/activate
[cmd] - .venv/scripts/activate
pip install -r requirements.txt

## Tests

pip install pytest
pytest cli-taskboard/test_task.py