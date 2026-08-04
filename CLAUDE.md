# AGENTS.md

> Project instructions for AI agents (Claude Code, Codex, ZCode, Cursor, etc.).
> `CLAUDE.md` is an independent copy of this file; a pre-commit hook enforces
> that the two stay byte-identical. When you edit one, copy it to the other.

## Identity

You are a senior pair-programming partner proficient in Python 3 and Django,
focused on writing secure, maintainable, and performant code that adheres to
Python and Django best practices.

## Tech Stack

- **Python**: 3.10+ (`requires-python = ">=3.10, <4"`)
- **Django**: 5.2+ with ASGI
- **Database**: SQLite for both development and production
- **ASGI Server**: Daphne for development, Gunicorn + Uvicorn worker for production
- **Async Tasks**: Huey
- **Frontend**: Vite 5 + Tailwind CSS 4 with typography plugin + TypeScript + django-vite
- **Deployment**: Ansible + Supervisor + Caddy
- **Packaging**: hatchling; dependency management via `uv`
- **e2e**: TypeScript + Playwright (Node toolchain, lives under `e2e/`)

## Project Structure

```text
├── config/                     # Django project settings & entry points
│   └── settings/
│       ├── base.py             # Base settings for all environments
│       ├── local.py            # Local development settings (DEBUG=True)
│       ├── test.py             # Test settings (pytest uses config.settings.test)
│       └── production.py       # Production settings (reads from env vars)
├── dream_blog/                 # Django apps & templates/static resources
│   ├── core/                   # Core abstract models & generic capabilities
│   ├── posts/                  # Blog posts
│   ├── tutorials/              # Blog tutorials
│   ├── columns/                # Blog columns
│   ├── tree_comments/          # Blog comments (django-tree-comments)
│   ├── notify/                 # User notifications (comment replies, mentions)
│   ├── users/                  # User system (custom user model, social login)
│   ├── search/                 # Full-text search with Chinese support
│   ├── tags/                   # Tagging system
│   ├── favorites/              # User favorites
│   ├── newsletters/            # Newsletter subscriptions
│   ├── alerts/                 # Alert system
│   ├── donate/                 # Donation system
│   ├── friendlinks/            # Friend links
│   ├── share/                  # Social sharing
│   ├── webtools/               # Web tools
│   ├── templates/              # Django templates
│   ├── static/                 # Static files (auto-collected)
│   ├── conftest.py             # Shared test fixtures
│   └── factories.py            # Test data factories
├── frontend/                   # Vite + Tailwind frontend resources
├── devops/                     # Deployment-related files (Ansible, Supervisor, Caddy)
├── e2e/                        # Playwright TypeScript e2e (independent Node project)
│   ├── package.json / playwright.config.ts / tsconfig.json
│   ├── tests/*.spec.ts
│   └── docker-compose.yml      # e2e-dedicated database
├── .claude/hooks/              # AI agent hook scripts (shared by Claude/Codex/ZCode configs)
├── pyproject.toml              # ruff/djlint/pytest/mypy config all live here
├── prek.toml                   # prek gate (ruff/djlint/pyproject-fmt/django-upgrade/mypy/sync)
├── manage.py                   # Django management script
├── AGENTS.md                   # this file
└── CLAUDE.md                   # independent copy of this file (kept in sync by a hook)
```

## Commands

Dev server:
```bash
uv sync --no-install-project
python manage.py migrate
python manage.py runserver                # http://127.0.0.1:8000
```

Tests:
```bash
uv run pytest                                    # full unit suite (--reuse-db)
uv run pytest dream_blog/posts/tests/test_views.py -v  # single file
uv run pytest -k test_post_detail               # pattern match
```

e2e (TypeScript Playwright):
```bash
bash e2e/setup-db.sh                             # setup DB + migrate
cd e2e && npm test                               # run all e2e
cd e2e && npm run test:headed                    # with browser UI
```

Lint / format / typecheck (config in pyproject.toml):
```bash
prek run --all-files                             # full gate (shared by local + CI)
uv run ruff check --fix                          # ruff only
uv run ruff format .                             # format only
uv run djlint dream_blog/templates --reformat    # templates only
uv run mypy dream_blog                           # typecheck (strict)
```

Migrations:
```bash
python manage.py makemigrations                  # create new migrations
python manage.py migrate                         # apply pending migrations
python manage.py makemigrations --check --dry-run  # CI gate: detect model drift
```

Frontend (must run in frontend/ directory):
```bash
cd frontend && pnpm dev                          # dev server with hot reload
cd frontend && pnpm build                        # production build
```

## Code Style

- **ruff** (`[tool.ruff]` in pyproject.toml): line-length 120, strict-usable rule
  set including `DJ`/`S`/`UP`/`B`/`SIM`. Test files exempt security rules.
- **djlint** (`[tool.djlint]`): `profile="django"`; HTMX `hx-*` attributes are
  supported natively, no special config needed.
- **prettier** (e2e/): formats `.css/.js/.ts/.json/.yaml/.toml`.
- **mypy** (`[tool.mypy]`): `strict=true`. All functions must have type annotations.
- **Write docstrings and module docstrings** — they are required. Other inline
  comments should be avoided; when necessary, only explain *why*, not *what*.
- After editing a file, a PostToolUse hook silently runs the matching formatter
  (ruff / djlint / prettier) by extension.
- Before the agent stops, a Stop hook runs `ruff check` + `djlint --lint` +
  `mypy --strict` (+ `tsc` if e2e changed); on failure it blocks the stop with
  `{"decision":"block","reason":...}` (exit 0 + JSON).

## Testing Conventions

- Unit tests live in each app's `tests/` directory, filenames matching the module
  under test (`dream_blog/posts/views.py` ↔ `dream_blog/posts/tests/test_views.py`).
- Test data via factory-boy; do not mock the database.
- `config.settings.test` is the test settings module.
- e2e tests live in `e2e/tests/*.spec.ts` (TypeScript Playwright), independent
  of pytest. They run against the Django dev server with SQLite.
- e2e covers core business contracts: post CRUD, tutorial navigation, comment
  submission, search, authentication.

## Database Migrations

This is a Django application; migrations follow Django's standard rules:

1. **When you change a model, immediately run `makemigrations` and commit the
   model change and the migration in the same commit.**
2. CI gate: `makemigrations --check --dry-run` must exit 0.
3. Data migrations (`RunPython`) rules:
   - Use `apps.get_model("app", "Model")`; never import the model directly
     (historical model).
   - Keep schema migrations and data migrations in separate files.
   - Provide `reverse_code` so the migration is reversible (use
     `migrations.RunPython.noop` for a no-op reverse).
   - Mark `elidable=True` so squash can drop them.

## Git Workflow

- Main branch is `main`; development happens on `main` (frequent direct commits).
- pre-commit gate (`prek.toml`): runs ruff/djlint/pyproject-fmt/django-upgrade/
  mypy/hygiene hooks automatically before each commit.
- Skip a single hook: `SKIP=ruff git commit ...`. Skip all: `git commit --no-verify`
  (use sparingly; CI still enforces).
- CI triggers per path filter (docs-only changes run no lint/test/e2e).

## Boundaries

**Always do**:
- Generate a migration right after changing a model; commit both together.
- Respect the ruff/djlint/mypy rules in pyproject.toml (do not add `# type: ignore`
  or `# noqa` without a strong reason, and document the reason inline).
- Add type annotations to every new function (mypy strict).
- Add tests for any new public API.

**Ask first**:
- Changing dependency version ranges in `pyproject.toml`.
- Removing or renaming a public API (breaking change).
- Changing CI workflow triggers or path filters.

**Never do**:
- Commit `.env`, `SECRET_KEY`, or anything under `.local/contexts/`.
- Hand-edit migration files — always regenerate via `makemigrations`.
- Claim "migrations are in sync" or "types pass" without running the check command.
- Modify any files under the `staticfiles/` directory — they're auto-collected by Django.

## Agent Hooks

This project ships AI agent hooks (`.claude/hooks/`), configured independently
for Claude Code (`.claude/settings.json`), Codex (`.codex/config.toml`), and
ZCode (`.zcode/config.json`):

- **PostToolUse** (`format_on_edit.py`): after the agent edits a file, silently
  runs the matching formatter by extension — ruff (`.py`), djlint (`.html`),
  prettier (`.css/.js/.ts/.json/.yaml/.toml`).
- **Stop** (`lint_gate.py`): before the agent stops, runs `ruff check` +
  `djlint --lint` + `mypy --strict` (+ `tsc` if e2e changed); on failure blocks
  the stop with `{"decision":"block","reason":...}` (exit 0 + JSON).

Exit-code semantics (identical for Claude Code, Codex, ZCode): exit 0 = proceed
(stdout parsed as JSON; `decision:"block"` with required `reason` blocks the
stop and feeds the reason back as a continuation prompt); exit 2 = legacy block
via stderr (also works but not used here); exit 1 = non-blocking error.
