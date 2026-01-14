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
- `uv add package --group dev` - Install development dependency (includes debug_toolbar, etc.)
- `uv add package --group test` - Install test dependency (includes pytest, etc.)

### Code Quality & Formatting

### Frontend

All commands must be executed in the frontend/ directory, i.e., after running `cd frontend/`

- `pnpm dev` - Start development server with hot reload
- `pnpm build` - Production build
- `pnpm add <package>` - Install frontend dependency

## Technology Stack

- **Backend:** Django 5+ with AGSI
- **Database:** SQLite for both development and production
- **ASGI Server:** Daphne for development, Gunicorn + Uvicorn worker for production
- **Async Tasks:** Huey
- **Frontend:** Vite 5 + Tailwind CSS 4 with typography plugin + TypeScript + django-vite
- **Deployment:** Ansible + Supervisor + Caddy

## Standards

- Use English for comments, documentation, log messages and exception information in code
