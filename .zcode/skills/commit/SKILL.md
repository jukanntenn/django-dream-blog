---
name: commit
description: Use when the user asks to commit or stage changes (commit/stage/save/submit), when a task ends with dirty files to commit, or when multiple files should be split into logical commits.
---

# Commit

Group by logical change, not by file. Draft a plan, confirm, then execute. Never push, never amend.

1. `git status --porcelain` + `git log --oneline -5` for current changes and history style.
2. Separate AI-edited files from unrecognized ones; list unrecognized separately, never mix them in.
3. Group by logical unit (route+service+model, page+hook+types); order: `build/chore` → `feat` → `fix` → `refactor` → `style` → `docs` → `test`, `release` last.
4. Present the plan once; after confirmation run `git add` + `git commit` batch by batch. Rejected → stop.
5. Verify before each commit: backend `uv run pytest -v`, frontend `cd web && pnpm lint && pnpm test`; prek hooks (ruff/ty/eslint/prettier) run on commit, never `--no-verify`.
6. Single file → skip the plan, commit directly.

Message: `<type>(<scope>): <desc>` — lowercase, imperative, no trailing period. Types: `feat`/`fix`/`refactor`/`docs`/`test`/`chore`/`ci`/`build`/`style`/`perf`. Scopes: `web`/`api`/`db`/`cli`/`config`/`container`/`devops`/`i18n`/`proposal`/`ai`/`notification` (omit for cross-cutting). Match the change's language.

- Generated files (lockfile, `progress.db`) bundle into the producing commit, or as a standalone `chore` — regenerate, never hand-edit.
- Template + code, and config + code, stay together when the code depends on them; mixed-language docs (`README.md` + `README_zh.md`) one commit.
- Never silently include unrecognized files. Never amend, never push, never placeholder messages (wip, update files).
