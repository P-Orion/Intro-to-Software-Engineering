# Priority Task Manager

**A Python/Reflex task-management application built for an Introduction to Software Engineering group project.**

The application lets users add tasks with Low, Medium, or High priority and mark tasks complete. The repository includes the original application and a refactored version that separates domain models, state management, and UI components.

## Features

- Form-based task creation with priority selection.
- Empty-input validation and completion controls.
- A refactoring example using typed models and distinct state/UI responsibilities.

## Run locally

```bash
git clone https://github.com/P-Orion/Intro-to-Software-Engineering.git
cd Intro-to-Software-Engineering
python -m venv .venv
```

Activate the environment:

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

```bash
# macOS / Linux
source .venv/bin/activate
```

Then install and launch:

```bash
python -m pip install -r requirements.txt
reflex init
reflex run
```

The normal entry point is [`todo/todo.py`](todo/todo.py), configured by [`rxconfig.py`](rxconfig.py). [`todo/refactored_todo.py`](todo/refactored_todo.py) is a separate refactoring example, not a second application started by the default configuration.

## Scope and attribution

This is a **collaborative Group 7 coursework project**. The dependency file specifies `reflex>=0.4.0` without a lockfile, so compatibility depends on the installed Reflex version.

## Repository map

- `todo/todo.py` — original application and UI.
- `todo/refactored_todo.py` — refactored implementation.
- `rxconfig.py` — app configuration.
- `requirements.txt` — Python dependencies.

[Orion's portfolio](https://orionpowers.com)
