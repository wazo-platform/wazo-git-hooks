#!/usr/bin/env python3
# Copyright 2016-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import re
import subprocess
import sys

from datetime import datetime

COPYRIGHT_TPL = "{}Copyright {}-{} The Wazo Authors  (see the AUTHORS file)"


def main():
    abort = False
    for filepath in find_files_to_check():
        copyright = find_copyright(filepath)
        if copyright is None:
            print(f"WARNING: {filepath} has no copyright")
        elif copyright and not copyright_ok(copyright):
            fix_copyright(filepath, copyright)
            abort = True

    if abort:
        print("Files have been changed. Please add and commit again.")
        sys.exit(1)


def find_files_to_check():
    cmd = ['git', 'diff', '--cached', '--name-only', '--diff-filter=MA']
    output = subprocess.check_output(cmd).strip().decode('utf-8')
    if not output:
        return []
    return [
        line.strip() for line in output.split("\n") if not os.path.islink(line.strip())
    ]


def find_copyright(filepath):
    with open(filepath) as f:
        for line in f:
            match = re.search(r"(.*)copyright.*?(\d+).*", line, re.IGNORECASE)
            if match:
                return match
    return None


def copyright_ok(match):
    current_year = str(datetime.now().year)
    return current_year in match.group(0)


def fix_copyright(filepath, match):
    prefix = match.group(1)
    first_year = match.group(2)
    current_year = datetime.now().year
    new_copyright = COPYRIGHT_TPL.format(prefix, first_year, current_year)
    change_copyright(filepath, match.group(0), new_copyright)


def change_copyright(filepath, old, new):
    print(f'{filepath}: "{old}" -> "{new}"')
    with open(filepath) as f:
        text = f.read()
    with open(filepath, 'w') as f:
        text = text.replace(old, new)
        f.write(text)


if __name__ == "__main__":
    main()
