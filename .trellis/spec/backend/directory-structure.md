# Directory Structure

> How backend code is organized in this project.

---

## Overview

This is a Django 5+ project with a custom app structure. The main application code lives in `dream_blog/`, while Django configuration is in `config/`.

**Key principle**: Each Django app is self-contained with its own models, views, urls, admin, tests, and templatetags.

---

## Directory Layout

```
django-dream-blog/
├── config/                      # Django project settings & entry points
│   ├── settings/
│   │   ├── base.py             # Base settings for all environments
│   │   ├── local.py            # Local development (DEBUG=True)
│   │   ├── test.py             # Test settings (pytest uses this)
│   │   └── production.py       # Production settings
│   ├── urls.py                 # Root URL configuration
│   ├── asgi.py                 # ASGI application
│   └── wsgi.py                 # WSGI application
│
├── dream_blog/                  # Main application directory (added to Python path)
│   ├── core/                   # Core abstract models & generic capabilities
│   │   ├── models.py           # Abstract base models (TimeStampedModel, etc.)
│   │   ├── admin.py            # Shared admin actions (hide, show)
│   │   ├── entries.py          # EntryQuerySet with published(), visible()
│   │   ├── tasks.py            # Huey async tasks
│   │   └── templatetags/       # Shared template tags
│   │
│   ├── posts/                  # Blog posts app
│   ├── tutorials/              # Tutorials app
│   ├── columns/                # Columns app
│   ├── comments/               # Comments app (custom, extends tree_comments)
│   ├── users/                  # Custom user model & authentication
│   │
│   ├── templates/              # Project-wide Django templates
│   │   ├── base.html
│   │   ├── posts/
│   │   ├── tutorials/
│   │   └── ...
│   │
│   ├── static/                 # Static files (not auto-generated)
│   └── media/                  # User-uploaded media files
│
├── frontend/                    # Vite + Tailwind frontend
│   ├── src/                    # TypeScript/JavaScript source
│   ├── dist/                   # Build output (served as static)
│   └── package.json
│
├── devops/                      # Deployment files
│   ├── ansible/
│   ├── supervisor/
│   └── caddy/
│
└── staticfiles/                 # Collected static files (auto-generated, DO NOT EDIT)
```

---

## Module Organization

### Django App Structure

Each Django app follows this structure:

```
{app_name}/
├── __init__.py
├── models.py           # Django models
├── views.py            # Class-based views
├── urls.py             # App-level URL patterns
├── admin.py            # Django admin configuration
├── forms.py            # Django forms (optional, only if needed)
├── apps.py             # App configuration
├── moderation.py       # Comment moderation (if applicable)
├── templatetags/       # Template tags specific to this app
│   ├── __init__.py
│   └── {app_name}_extra.py
├── tests/              # Tests in separate directory
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_views.py
│   ├── test_admin.py
│   └── factories.py    # Factory Boy factories
├── migrations/         # Database migrations
│   └── __init__.py
└── management/         # Management commands (optional)
    └── commands/
```

### Adding a New App

1. Create app in `dream_blog/` directory
2. Add to `LOCAL_APPS` in `config/settings/base.py`
3. Follow the standard app structure above

---

## Naming Conventions

### Files and Directories

- **Apps**: lowercase with underscores (e.g., `tree_comments`, not `treeComments`)
- **Modules**: lowercase (e.g., `models.py`, `views.py`)
- **Tests**: `test_{what}.py` pattern (e.g., `test_views.py`)
- **Template tags**: `{app_name}_extra.py` (e.g., `posts_extra.py`)

### Python Classes

- **Models**: PascalCase singular (e.g., `Post`, `Comment`)
- **Views**: PascalCase with suffix (e.g., `PostDetailView`)
- **Managers**: PascalCase with suffix (e.g., `PostManager`)
- **Factories**: PascalCase with suffix (e.g., `PostFactory`)

### URL Patterns

- Use namespaced URLs: `app_name:name` pattern
- Example: `posts:detail`, `comments:post`

---

## Examples

### Well-organized app: `posts/`

```
dream_blog/posts/
├── __init__.py
├── admin.py          # PostAdmin with hide/show actions
├── apps.py
├── models.py         # Post model inheriting from core abstract models
├── urls.py           # Namespaced URL patterns
├── views.py          # PostDetailView class-based view
├── templatetags/
│   ├── __init__.py
│   └── posts_extra.py
├── tests/
│   ├── __init__.py
│   ├── factories.py  # PostFactory using factory_boy
│   ├── test_models.py
│   ├── test_views.py
│   └── test_admin.py
└── migrations/
```

### Core abstract models: `dream_blog/core/models.py`

Contains reusable abstract base classes:
- `TimeStampedModel` - adds `created_at`, `modified_at`
- `RichContentModel` - adds markdown content with TOC
- `CommentsModel` - adds generic comment relation
- `HitCountModel` - adds hit count functionality
