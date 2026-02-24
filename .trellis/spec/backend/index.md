# Backend Development Guidelines

> Best practices for backend development in this project.

---

## Overview

This directory contains guidelines for Django backend development in the django-dream-blog project.

**Tech Stack**: Django 5+ with SQLite, Huey for async tasks, ASGI/Daphne.

---

## Guidelines Index

| Guide | Description | Status |
|-------|-------------|--------|
| [Directory Structure](./directory-structure.md) | Module organization and file layout | Filled |
| [Database Guidelines](./database-guidelines.md) | ORM patterns, queries, migrations | Filled |
| [Error Handling](./error-handling.md) | Error types, handling strategies | Filled |
| [Quality Guidelines](./quality-guidelines.md) | Code standards, forbidden patterns | Filled |
| [Logging Guidelines](./logging-guidelines.md) | Structured logging, log levels | Filled |

---

## Quick Reference

### Project Structure

```
config/           # Django settings (base, local, test, production)
dream_blog/       # Main application directory
├── core/         # Abstract models, shared utilities
├── posts/        # Blog posts app
├── comments/     # Comments system
├── users/        # Custom user model
└── templates/    # Django templates
```

### Key Patterns

- **Models**: Inherit from abstract base classes in `core.models`
- **Views**: Use class-based views
- **QuerySets**: Custom QuerySets with `published()`, `visible()` methods
- **Testing**: pytest with Factory Boy and test-plus

---

## How to Use These Guidelines

1. Read the relevant guideline before starting development
2. Follow the patterns documented with code examples
3. Check forbidden patterns to avoid common mistakes
4. Use `/trellis:before-backend-dev` to inject these guidelines into AI context

---

**Language**: All documentation should be written in **English**.
