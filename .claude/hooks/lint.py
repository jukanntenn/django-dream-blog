#!/usr/bin/env python3
"""
PostToolUse hook for linting Python files after editing.
This hook runs after Edit, Write, or MultiEdit operations and applies ruff checking.
"""

import json
import subprocess
import sys


def main():
    """Main function to run ruff check hook."""
    try:
        hook_data = json.load(sys.stdin)
        tool_input = hook_data.get("tool_input", {})

        file_path = tool_input.get("file_path", "")

        if not file_path or not file_path.endswith((".py", ".pyi")):
            print("Ruff check: Not a python file, skipping.")
            sys.exit(0)

        try:
            check_result = subprocess.run(
                [
                    "ruff",
                    "check",
                    "--fix",
                    "--select",
                    "F,E,W,I",
                    "--line-length",
                    "120",
                    file_path,
                ],
                capture_output=True,
                text=True,
            )
        except FileNotFoundError:
            print("Ruff not found. Please install ruff.", file=sys.stderr)
            sys.exit(0)

        if check_result.returncode == 0:
            if check_result.stdout:
                print(check_result.stdout, end="")
            if check_result.stderr:
                print(check_result.stderr, file=sys.stderr, end="")
            sys.exit(0)
        elif check_result.returncode == 1:
            if check_result.stdout:
                print(check_result.stdout, file=sys.stderr, end="")
            if check_result.stderr:
                print(check_result.stderr, file=sys.stderr, end="")
            sys.exit(2)
        else:
            if check_result.stdout:
                print(check_result.stdout, end="")
            if check_result.stderr:
                print(check_result.stderr, file=sys.stderr, end="")
            sys.exit(0)

    except Exception as e:
        print(f"Hook error: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
