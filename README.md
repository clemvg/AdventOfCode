# Advent of Code

My solutions for [Advent of Code](https://adventofcode.com/) challenges.

## Setup

This project uses [uv](https://docs.astral.sh/uv/) for Python package management and virtual environment handling.

### Installation

Create and activate virtual environment with uv:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

Install dependencies:
```bash
uv pip install -r requirements.txt
```

- uv works flawlessly with both pyproject.toml and requirements.txt.
- It is fast, simple, and compatible with pip, while offering Poetry-like workflows.
- The most common commands are uv sync, uv add, uv remove, uv lock, uv venv, and uv run.

### When to choose pyproject vs requirements with uv?

| Use case                      | Recommended                |
| ----------------------------- | -------------------------- |
| Standard package/project      | pyproject.toml + uv lock   |
| ML experiments, quick scripts | requirements.txt           |
| Replacing Poetry seamlessly   | pyproject.toml + uv sync   |
| Deploying in Azure/Kubernetes | export to requirements.txt |

## Import module error for folders

`Key Python behavior`: When you run `python tasks/day_1_the_elves.py`, Python adds the directory containing the script (`tasks/`) to `sys.path`, NOT the current working directory.
So the root directory is never automatically added when you run scripts in subdirectories directly.

### Option 1: Install Your Project as an Editable Package (Best for reusable code)

Create a `pyproject.toml` at your project root:
```toml
[project]
name = "adventofcode"
version = "0.1.0"
requires-python = ">=3.10"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

Then install it in editable mode:
```bash
uv pip install -e .
```

Now `from utils import common` works everywhere, and you can run `python tasks/day_1_the_elves.py` from anywhere.

### Option 2: Restructure Your Project (Best for scripts)

Separate executable scripts from packages:
```text
AdventOfCode/
├── src/
│   ├── __init__.py
│   └── utils/
│       ├── __init__.py
│       └── common.py
├── scripts/          # or "bin/"
│   └── day_1_the_elves.py
└── pyproject.toml
```

In scripts, import as:
```python
from src.utils import common
```

### Option 3: Accept -m as Standard (Pythonic way)

This is actually the intended Python behavior for package-structured projects. Just always use:
```bash
python -m tasks.day_1_the_elves
```

Many professional Python projects (Django, Flask apps, etc.) use this pattern. It's not a workaround—it's the design.

### Debugging personal notes

Look at select Interpreter:
```bash
python3 -c "import sys, pprint; pprint.pprint(sys.path)"
echo $PYTHONPATH
```

The first empty string `''` means “current working directory” at runtime.

If `python -m` works but `python day_1_the_elves.py` doesn’t, you’re hitting path/package resolution differences. Using `-m` ensures the project root is treated as a package root.

TODO: solve this issue.

So three working options for now:
- export `PYTHONPATH="$PWD:$PYTHONPATH"` to modify PYTHONPATH.
- add `sys.path` at beginning of py script:
  ```python
  import sys
  sys.path.insert(0, '/Users/clementvangoethem/Library/Mobile Documents/com~apple~CloudDocs/Code_projects/AdventOfCode')
  ```
- run via `python -m` (without the `.py` at the end and `__init__` with underscores)

Other option that currently does not work:
- in `.env` to modify PYTHONPATH - though I updated `settings.json` vscode