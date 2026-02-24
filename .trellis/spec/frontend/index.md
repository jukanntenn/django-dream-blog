# Frontend Development Guidelines

> Best practices for frontend development in this project.

---

## Overview

This directory contains guidelines for frontend development in the django-dream-blog project.

**Tech Stack**: Vite 5 + Tailwind CSS 4 + TypeScript, integrated with Django via django-vite.

**Note**: This project uses vanilla TypeScript classes (not React/Vue).

---

## Guidelines Index

| Guide | Description | Status |
|-------|-------------|--------|
| [Directory Structure](./directory-structure.md) | Module organization and file layout | Filled |
| [Component Guidelines](./component-guidelines.md) | Component patterns, props, composition | Filled |
| [Hook Guidelines](./hook-guidelines.md) | Module patterns, data fetching | Filled |
| [State Management](./state-management.md) | Component state, DOM state | Filled |
| [Quality Guidelines](./quality-guidelines.md) | Code standards, forbidden patterns | Filled |
| [Type Safety](./type-safety.md) | Type patterns, validation | Filled |

---

## Quick Reference

### Project Structure

```
frontend/
├── src/           # TypeScript source files
│   ├── main.ts    # Entry point
│   ├── comment.ts # Comment system component
│   ├── toast.ts   # Toast notifications
│   └── ...
├── dist/          # Build output
└── package.json   # Dependencies (pnpm)
```

### Key Patterns

- **Components**: Class-based with `init()` method
- **Styling**: Tailwind CSS utilities preferred
- **State**: Private class properties, DOM for persistence
- **Events**: Event delegation for dynamic content

### Commands

```bash
cd frontend
pnpm dev      # Development server
pnpm build    # Production build
```

---

## How to Use These Guidelines

1. Read the relevant guideline before starting development
2. Follow the patterns documented with code examples
3. Check forbidden patterns to avoid common mistakes
4. Use `/trellis:before-frontend-dev` to inject these guidelines into AI context

---

**Language**: All documentation should be written in **English**.
