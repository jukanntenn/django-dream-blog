---
name: commit
description: Use when the user asks to commit or stage changes, when a task ends with dirty files to commit, or when multiple files should be split into logical commits.
---

# Commit

Group by logical change, not by file. Plan once, confirm, then execute. Never push, never amend.

1. `git status --porcelain` + `git log --oneline -5` for current changes and history style.
2. Separate AI-edited files from unrecognized ones; list unrecognized separately, never mix them in.
3. Group by logical unit, order: `chore` -> `feat` -> `fix` -> `refactor` -> `docs` -> `test` -> `ci`.
4. Present the plan once; after confirmation run `git add` + `git commit` batch by batch. Rejected -> stop.
5. Single file -> skip the plan, commit directly.

Message: `<type>(<scope>): <desc>` - lowercase, imperative, no trailing period. Types: `feat`/`fix`/`docs`/`style`/`refactor`/`perf`/`test`/`build`/`ci`/`chore`. Scope optional (e.g. `admin`, `search`, `alerts`, `tags`).

- prek auto-runs (ruff / djlint / pyproject-fmt / django-upgrade / mypy / agents-claude-sync); never `--no-verify`.
- `CLAUDE.md` and `AGENTS.md` must stay byte-identical - `agents-claude-sync` rejects divergence.
- Model changes and their migrations go in the same commit.
- Never silently include unrecognized files. Never placeholder messages (wip, update files).
