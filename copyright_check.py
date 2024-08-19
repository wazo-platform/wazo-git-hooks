#!/usr/bin/env python3
# Copyright 2016-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import re
import sys

from datetime import datetime

from wazo_hook_utils import list_files_to_commit

COPYRIGHT_TPL = "{}Copyright {}-{} The Wazo Authors  (see the AUTHORS file)"
COPYRIGHT_REGEX = re.compile(
    r"(?P<prefix>.*)copyright.*?(?P<first_year>\d+).*", re.IGNORECASE
)
EXCLUDE_FILES = [
    "LICENSE",
    "debian/copyright",
    "attribution.md",  # Used by wazo-platform.org
]


def main() -> None:
    abort = False

    files_to_check = list_files_to_commit()
    if specified_files := sys.argv[1:]:
        files_to_check = [f for f in specified_files if f in files_to_check]
    files_to_check = [f for f in files_to_check if not is_excluded(f)]

    for file_path in files_to_check:
        copyright_text = find_copyright(file_path)
        if copyright_text is None:
            print(f"WARNING: {file_path} has no copyright")
        elif copyright_text and not copyright_ok(copyright_text):
            fix_copyright(file_path, copyright_text)
            abort = True

    if abort:
        print("Files have been changed. Please add and commit again.")
        sys.exit(1)


def is_excluded(file_path: str) -> bool:
    return any(exclude_file in file_path for exclude_file in EXCLUDE_FILES)


def find_copyright(file_path: str) -> re.Match[str] | None:
    with open(file_path) as f:
        for line in f:
            if match := COPYRIGHT_REGEX.search(line):
                return match
    return None


def copyright_ok(match: re.Match[str]) -> bool:
    current_year = str(datetime.now().year)
    return current_year in match.group(0)


def fix_copyright(filepath: str, match: re.Match[str]) -> None:
    prefix, first_year = match.groups()
    current_year = datetime.now().year
    new_copyright = COPYRIGHT_TPL.format(prefix, first_year, current_year)
    change_copyright(filepath, match.group(0), new_copyright)


def change_copyright(filepath: str, old: str, new: str) -> None:
    print(f'{filepath}: "{old}" -> "{new}"')
    with open(filepath) as f:
        text = f.read()
    with open(filepath, 'w') as f:
        text = text.replace(old, new)
        f.write(text)


if __name__ == "__main__":
    main()
