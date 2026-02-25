# CLAUDE.md

This file provides guidance to AI assistants when working with code in this repository.

## Project Structure

Keep this section up to date with the project structure. Use it as a reference to find files and directories.

- `config/`: Django project settings & entry points (settings/urls/asgi/wsgi, etc.)
  - `config/settings/`
    - `base.py`: Base settings for all environments
    - `local.py`: Local development settings (DEBUG=True, includes debug_toolbar, etc.)
    - `test.py`: Test settings (pytest uses `config.settings.test`)
    - `production.py`: Production settings (reads sensitive config from environment variables)
- `dream_blog/`: Django apps & templates/static resources (this directory is added to Python Path)
  - `core`: Core abstract models & generic capabilities
  - `posts`: Blog posts
  - `tutorials`: Blog tutorials
  - `columns`: Blog columns
  - `tree_comments`: BLog comments
  - `users`: User system (custom user model, social login with allauth)
- `frontend/`: Vite + Tailwind frontend resources (build artifacts & source code)
- `devops/`: Deployment-related files (Ansible, Supervisor, Caddy, etc.)

## Commands

### Primary Development Commands

- `python manage.py runserver` - Start Django development server
- `python manage.py makemigrations` - Create new Django migrations
- `python manage.py migrate` - Apply pending migrations
- `python manage.py run_huey` - Start Huey consumer to process async tasks
- `pytest` - Run all tests (configured in `pyproject.toml` with `addopts`)
- `pytest -k <pattern>` - Run tests matching `<pattern>` (e.g., `test_post_detail`)
- `pytest <path>` - Run tests in `<path>` (e.g., `dream_blog/posts/tests/test_views.py`)

### Dependency Management

- `uv sync --no-install-project` - Install default dependency groups (dev/test/production)
- `uv add package --group dev --no-install-project` - Install development dependency (includes debug_toolbar, etc.)
- `uv add package --group test --no-install-project` - Install test dependency (includes pytest, etc.)

### Code Quality & Formatting

### Frontend

All commands must be executed in the frontend/ directory, i.e., after running `cd frontend/`

- `pnpm dev` - Start development server with hot reload
- `pnpm build` - Production build
- `pnpm add <package>` - Install frontend dependency

### VSCode Tasks

Quick development server management via VSCode tasks:

1. Open Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P`)
2. Run `Tasks: Run Task`
3. Select one of:
   - **Start All** - Start both Django and Vite servers in parallel (recommended)
   - **Start Django** - Start only the Django development server
   - **Start Vite** - Start only the Vite frontend server

Each server runs in its own terminal tab, allowing individual stop/restart.

### MCP Dev Server Integration

When you need to start development servers for testing, use **dev-manager-mcp** to avoid port conflicts:

**Workflow:** Start Vite first → Get its port → Start Django with VITE_PORT

```python
# Step 1: Start Vite server first (try pnpm, fallback to npm if fails)
mcp__dev-manager__start(command="pnpm dev", cwd="/path/to/project/frontend")
# If pnpm fails with "not found", retry with:
mcp__dev-manager__start(command="npm run dev", cwd="/path/to/project/frontend")
# Returns: { "port": 3011, ... }

# Step 2: Start Django with VITE_PORT set to Vite's allocated port
mcp__dev-manager__start(
    command="VITE_PORT=3011 uv run python3 manage.py runserver",
    cwd="/path/to/project"
)
```

Both servers respect the `PORT` environment variable:
- Django: Falls back to 8000 if PORT not set
- Vite: Falls back to 5173 if PORT not set
- Django needs `VITE_PORT` to know where to fetch frontend assets

See `.trellis/spec/guides/dev-server-mcp.md` for details.

## Technology Stack

- **Backend:** Django 5+ with AGSI
- **Database:** SQLite for both development and production
- **ASGI Server:** Daphne for development, Gunicorn + Uvicorn worker for production
- **Async Tasks:** Huey
- **Frontend:** Vite 5 + Tailwind CSS 4 with typography plugin + TypeScript + django-vite
- **Deployment:** Ansible + Supervisor + Caddy

## Standards

- Use English for comments, documentation, log messages and exception information in code
- Don’t modify any files under the staticfiles directory--they’re auto-collected by Django

## Pre-commit Configuration

This project uses pre-commit hooks to maintain code quality. Auto-generated files are excluded from pre-commit checks to avoid unnecessary friction.

### Auto-generated Files

The following files are marked as `linguist-generated` in `.gitattributes` and excluded from pre-commit hooks:

- `frontend/dist/manifest.json` - Vite build output (changes with every frontend build)
- `.trellis/tasks/**/*.jsonl` - Task context files (AI agent workflow)

These files are still committed to the repository but pre-commit hooks will not modify or validate them.

### How It Works

1. `.gitattributes` marks files with `linguist-generated` attribute (for GitHub and other tools)
2. `.pre-commit-config.yaml` uses regex pattern to exclude these files from all hooks
3. GitHub respects the `linguist-generated` attribute and hides these files in diffs by default

To add new auto-generated files:
1. Add the file pattern to `.gitattributes` with `linguist-generated`
2. Add the file pattern to the `exclude` regex in `.pre-commit-config.yaml`
