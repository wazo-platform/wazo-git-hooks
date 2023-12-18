#!/usr/bin/env python3
# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import re
import subprocess
import sys

from wazo_hook_utils import get_files_to_check


def main() -> None:
    if not should_run():
        return

    files = get_files_to_check()

    if 'debian/changelog' not in files:
        print("Please update the changelog before committing.")
        sys.exit(1)


def should_run() -> bool:
    cmd = ['dpkg-parsechangelog', '--show-field', 'Version']
    result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
    command_exists = result.returncode != 127
    if not command_exists:
        result.check_returncode()
    changelog_exists = result.returncode != 255
    if not changelog_exists:
        return False
    changelog_version = result.stdout.strip()
    is_repackaged_by_wazo = re.match(r'^.*~(xivo|wazo)[0-9]', changelog_version)
    cmd = ['dpkg-parsechangelog', '--show-field', 'Source']
    changelog_package = subprocess.check_output(cmd, text=True).strip()
    is_packaging = changelog_package.endswith('-packaging')
    return bool(is_packaging or is_repackaged_by_wazo)


if __name__ == "__main__":
    main()
