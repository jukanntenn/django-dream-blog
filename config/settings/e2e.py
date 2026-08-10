"""
E2E test settings: production-grade frontend assets and an isolated database.

django-vite runs in manifest mode (dev_mode=False) and DEBUG is off, so the
Playwright suite exercises the exact CSS/JS the production site serves.
Run `pnpm build` in frontend/ before starting the suite.
"""

from pathlib import Path

from .local import *  # noqa: F403

DEBUG = False
DJANGO_VITE = {"default": {"dev_mode": False}}

# Dedicated e2e database: never touch the development database.
E2E_DB_PATH = Path(__file__).resolve().parent.parent.parent / "e2e" / "e2e.sqlite3"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": str(E2E_DB_PATH),
    }
}
