#!/usr/bin/env python3
"""
PostToolUse hook for formatting Python files after editing.
This hook runs ruff format in the background after Edit or Write operations.
"""

import json
import subprocess
import sys


def main():
    """Main function to run ruff format hook."""
    try:
        hook_data = json.load(sys.stdin)
        tool_input = hook_data.get("tool_input", {})

        file_path = tool_input.get("file_path", "")

        if not file_path or not file_path.endswith((".py", ".pyi")):
            sys.exit(0)

        try:
            subprocess.run(
                ["ruff", "format", file_path],
                capture_output=True,
                text=True,
            )
        except FileNotFoundError:
            pass

        sys.exit(0)

    except Exception:
        sys.exit(0)


if __name__ == "__main__":
    main()
