# Dev Server Orchestrator

## Goal

Create a unified solution to start/restart/stop all development servers with a single command, working in both VSCode and terminal environments.

## What I already know

**Current servers to manage:**
- **Frontend**: Vite dev server (`cd frontend && pnpm dev`) - port 5173
- **Backend**: Django runserver (`python manage.py runserver`) - port 8000

**Current state:**
- VSCode only has Django debug configurations (no Vite integration)
- No tasks.json exists
- No Procfile or process manager configured
- No Makefile in project

**Current pain point:**
- Must open 2 terminals and run commands separately
- Restart requires stopping each server individually

## Assumptions (temporary)

- User is on Linux/WSL (based on env info)
- Huey consumer may also need to be started for async tasks (not explicitly mentioned)
- User prefers native/zero-dependency solutions when possible

## Decisions

- **Scope**: Django + Vite only (no Huey)
- **Approach**: VSCode tasks.json (zero dependencies)

## Requirements

- Single command to start all dev servers (Django + Vite)
- Works in VSCode via tasks.json
- Each server runs in its own terminal tab (easy to view logs separately)
- Can stop/restart individual servers independently
- Optional: keyboard shortcut for quick access

## Acceptance Criteria

- [x] `Tasks: Run Task` → "Start All" launches both servers in parallel
- [x] Each server has its own terminal tab with clear label
- [x] Can kill individual terminal without affecting the other
- [x] Individual tasks exist for "Start Django" and "Start Vite"

## Definition of Done (team quality bar)

- [x] Documentation added to CLAUDE.md or README
- [x] Tested on WSL2 environment

## Technical Approach

Create `.vscode/tasks.json` with:

1. **"Start Django"** task — runs `python manage.py runserver` in integrated terminal
2. **"Start Vite"** task — runs `cd frontend && pnpm dev` in integrated terminal
3. **"Start All"** compound task — runs both in parallel via `dependsOn`

Each task uses `"presentation": { "reveal": "always", "panel": "new" }` to create separate terminal tabs.

## Out of Scope (explicit)

- Production deployment configuration
- Hot reload configuration (already working)
- CI/CD integration

## Technical Notes

- Frontend: `frontend/package.json` has `pnpm dev`
- Backend: `manage.py runserver` (Django)
- Possible third: `manage.py run_huey` (async tasks)
- VSCode launch.json exists but only for Django debugging
