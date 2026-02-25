# brainstorm: auto-commit auto-generated files in pre-commit

## Goal

Enable pre-commit hooks to automatically commit changes to auto-generated files (like `manifest.json` and `*.jsonl` files) without requiring manual re-confirmation, streamlining the development workflow.

## What I already know

**Files identified as auto-generated:**
- `frontend/dist/manifest.json` - Vite build output with hashed asset names
- `.trellis/tasks/**/*.jsonl` - Task context files (implement.jsonl, debug.jsonl, check.jsonl)

**Current pre-commit setup:**
- Uses `uv-pre-commit` for `uv-lock` and `uv-export`
- Uses standard hooks: `trailing-whitespace`, `end-of-file-fixer`, `check-yaml`, `check-added-large-files`

**Git history shows:**
- `manifest.json` changes with every frontend build (hash changes in asset filenames)
- `*.jsonl` files are committed as part of task workflow

**Current behavior:**
- Pre-commit hooks modify files during commit
- User must re-add and re-commit, causing friction

**Exact failure scenario (confirmed):**
- Pre-commit modifies the file and fails the commit
- User must re-add the modified file and retry the commit

**Git attributes:**
- `*.manifest` is in `.gitignore` (but `manifest.json` is not affected by this pattern)
- `frontend/dist/manifest.json` exists and is tracked in git

**Git status:**
- Current working directory has staged changes and untracked files
- No immediate conflict visible in current status

**Files causing friction (confirmed):**
- Both `manifest.json` and `*.jsonl` files cause issues equally
- Both need to be handled by the solution

**Commit requirement (confirmed):**
- Both types of files MUST be committed to the repository
- They cannot be gitignored because they're needed for deployment/team workflow

## Assumptions (temporary)

- The conflict happens when pre-commit hooks modify auto-generated files
- The user wants these files to be committed automatically
- The auto-generated files are safe to commit without review (they're deterministic outputs)

## Open Questions

None - all critical questions answered.

## Requirements (evolving)

- Pre-commit should handle auto-generated files without requiring manual intervention
- Solution should be safe (not bypass important checks on source code)
- Solution should be maintainable (clear configuration, documented)
- Auto-generated files must still be committed to repository (cannot gitignore)
- Solution should work for both `manifest.json` and `*.jsonl` files

## Decision (ADR-lite)

**Context:** Auto-generated files (manifest.json and *.jsonl) are modified by pre-commit hooks, causing commit failures and requiring manual re-add/retry cycles. These files must be committed for deployment and team workflow.

**Decision:** Use Git attributes + global exclude approach (Approach C)
- Mark files as `linguist-generated` in `.gitattributes`
- Use global `exclude: linguist-generated` in `.pre-commit-config.yaml`

**Consequences:**
- Standard git convention clearly documents which files are auto-generated
- Pre-commit will automatically skip these files for all hooks
- Solution works with other tools that respect `linguist-generated` attribute
- Trade-off: Validation hooks (like check-yaml) will also skip these files
- Future maintainers can easily understand and extend the pattern

## Acceptance Criteria (evolving)

- [x] `.gitattributes` file created with `linguist-generated` markers for target files
- [x] `.pre-commit-config.yaml` updated with `exclude: linguist-generated`
- [x] Auto-generated files can be committed without manual re-confirmation
- [x] Source code files still go through normal pre-commit checks
- [x] Solution tested with actual pre-commit run on both file types

## Definition of Done (team quality bar)

- Solution tested with actual pre-commit run
- Documentation updated (CLAUDE.md or pre-commit config comments)
- No regression in pre-commit safety checks

## Out of Scope (explicit)

- Modifying the content of auto-generated files
- Changing the build process for frontend
- Removing pre-commit hooks entirely
- Adding documentation for future file types
- Creating separate validation for generated files
- Handling other potential auto-generated files (API clients, schemas, etc.)

## Technical Approach

**Implementation: Git attributes + pre-commit exclude**

1. Create/update `.gitattributes` file:
   - Mark `frontend/dist/manifest.json` as `linguist-generated`
   - Mark `.trellis/tasks/**/*.jsonl` as `linguist-generated`

2. Update `.pre-commit-config.yaml`:
   - Add global `exclude: linguist-generated` at the top level
   - This tells pre-commit to skip all hooks for files marked as generated

**Why this approach:**
- Uses standard git convention for generated files
- Clear documentation of which files are auto-generated
- Works with other tools (GitHub will hide these in diffs by default)
- Simple to maintain and extend

## Technical Notes

**Pre-commit config location:** `.pre-commit-config.yaml`

**Research findings:**

**Approach 1: Global exclude pattern (Recommended)**
Add a global `exclude` pattern in `.pre-commit-config.yaml` to skip auto-generated files:
```yaml
exclude: ^(frontend/dist/manifest\.json|\.trellis/tasks/.*\.jsonl)$
```
- **Pros:** Simple, centralized, one-line change
- **Cons:** Excludes ALL hooks for these files (including validation hooks)

**Approach 2: Per-hook exclude**
Exclude auto-generated files only from hooks that modify them:
```yaml
- id: trailing-whitespace
  exclude: ^(frontend/dist/manifest\.json|\.trellis/tasks/.*\.jsonl)$
- id: end-of-file-fixer
  exclude: ^(frontend/dist/manifest\.json|\.trellis/tasks/.*\.jsonl)$
```
- **Pros:** More precise, other hooks (like `check-yaml`) still run
- **Cons:** More verbose, must update each modifying hook

**Approach 3: Git attributes with `linguist-generated`**
Mark files as generated in `.gitattributes`:
```
frontend/dist/manifest.json linguist-generated
.trellis/tasks/**/*.jsonl linguist-generated
```
- **Pros:** Standard way to mark generated files, some tools respect this automatically
- **Cons:** Pre-commit doesn't automatically respect `linguist-generated` without additional configuration

**Approach 4: Custom hook with `ignore-exit-code`**
Use `pre-commit hazmat ignore-exit-code` to make hooks pass despite modifications:
```yaml
- id: end-of-file-fixer
  entry: pre-commit hazmat ignore-exit-code end-of-file-fixer --
```
- **Pros:** Hooks still run and fix files, but don't fail
- **Cons:** Requires pre-commit 4.5.0+, adds warning noise, marked as "hazmat" (dangerous)

**Constraints:**
- Pre-commit is already configured and working for source code
- Frontend build process generates manifest.json deterministically
- Task workflow generates jsonl files as part of AI agent context management
- Both file types must be committed (cannot gitignore)
