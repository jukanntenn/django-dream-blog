---
name: nudging
description: Find 3-5 small, incremental code improvements to reduce codebase entropy and plan them as tasks. Use this skill whenever the user wants to nudge the codebase toward better shape, asks for a tiny refactor, says "nudge", or wants a low-risk cleanup pass — even if they don't describe a specific change.
---

## What this does

Find 3-5 small improvement opportunities in the codebase and plan each one as a task. Think of it as paying down technical debt a few coins at a time — each nudge makes the code slightly cleaner without any risk to behavior.

## Workflow

### Step 1 — Progressive discovery

Start small and expand only as needed. Follow this order:

1. **Single file** — pick one file, look for improvements.
2. **Module files** — if still short on improvements, look at other files in the same module.
3. **Whole module** — expand to the entire module if needed.
4. **Cross-module** — look at related modules.
5. **Project-wide** — last resort.

**Stop as soon as you have enough improvements.** Do not keep exploring once you have 3-5 solid ones. The goal is efficiency — find improvements quickly in the smallest scope possible and move on.

### Step 2 — Create tasks

For each improvement, create a task:

```bash
fa task create nudge-<descriptive-slug>
```

**MANDATORY**: you MUST create tasks using `fa task create` command. NEVER create tasks manually.

Then write `spec.md` and `plan.md` in each task directory. The plan must be detailed enough that someone unfamiliar with the codebase could execute it without making a single design decision.

All slugs must start with `nudge-`.

### Step 3 — Output result

Output JSON when done:

```json
{
  "tasks": [
    {"task_id": <task-id>, "task_path": "<absolute-path-to-task-directory>"},
    {"task_id": <task-id>, "task_path": "<absolute-path-to-task-directory>"}
  ]
}
```

If you genuinely cannot find anything worth improving, return an empty list:

```json
{
  "tasks": []
}
```

Do not force it. An empty list is a perfectly valid result — it means the codebase is in good shape.

## Target count

Aim for **3-5 improvements** per invocation. If you discover more high-quality ones during exploration, you may include up to **7**. If even after thorough searching you cannot find 3, return what you have — even 1 or 2 genuine improvements are better than padded ones.

## What counts as a nudge

- Extract a code fragment into a pure function, add type hints, write unit tests
- Fix naming inconsistencies that hurt readability
- Simplify equivalent code — remove redundancy or unnecessary complexity
- Any small, self-contained improvement that leaves the codebase cleaner

This list is not exhaustive — use your judgment.

## Rules

- Each function should do one thing. If you spot one that does two, that is a valid nudge.
- Never change business logic. The behavior before and after must be identical.
- Keep the scope of each individual nudge small. Resist the urge to chain improvements within a single task.
