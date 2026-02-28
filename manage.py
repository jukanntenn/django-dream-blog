#!/usr/bin/env python
import os
import sys
from pathlib import Path

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django  # noqa
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )

        raise

    # This allows easy placement of apps within the interior
    # my_awesome_project directory.
    current_path = Path(__file__).parent.resolve()
    sys.path.append(str(current_path / "dream_blog"))

    # Support PORT environment variable for runserver (for dev-manager-mcp integration)
    if "runserver" in sys.argv:
        # Check if port is already specified in command arguments
        has_port_arg = any(":" in arg or arg.isdigit() for arg in sys.argv[1:])
        if not has_port_arg:
            port = os.environ.get("PORT", "8000")
            sys.argv.append(f"127.0.0.1:{port}")

    execute_from_command_line(sys.argv)
