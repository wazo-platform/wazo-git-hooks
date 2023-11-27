from __future__ import annotations

import subprocess
import sys
from os import path


def list_files_to_commit() -> list[str]:
    """
    Return a list of all staged files.
    """
    cmd = ['git', 'diff', '--cached', '--name-only', '--diff-filter=MA']
    output = subprocess.check_output(cmd, text=True).strip()
    if not output:
        return []
    return [
        line.strip() for line in output.split("\n") if not path.islink(line.strip())
    ]


def get_files_to_check() -> list[str]:
    """
    Pre-commit will pass files as arguments to script or not call it at all.
    If no arguments are received, we will assume we are running as standalone
    And find the files ourselves.
    """
    if files := sys.argv[1:]:
        return files
    return list_files_to_commit()
