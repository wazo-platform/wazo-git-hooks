#!/usr/bin/env python3
# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import re
import subprocess
import sys


def main():
    if not should_run():
        return

    files = list_files_to_commit()

    if 'debian/changelog' not in files:
        print("Please update the changelog before committing.")
        sys.exit(1)


def should_run():
    cmd = ['dpkg-parsechangelog', '--show-field', 'Version']
    result = subprocess.run(cmd, stdout=subprocess.PIPE)
    command_exists = result.returncode != 127
    if not command_exists:
        result.check_returncode()
    changelog_exists = result.returncode != 255
    if not changelog_exists:
        return False
    changelog_version = result.stdout.strip().decode('utf-8')
    is_repackaged_by_wazo = re.match(r'^.*~(xivo|wazo)[0-9]', changelog_version)
    cmd = ['dpkg-parsechangelog', '--show-field', 'Source']
    changelog_package = subprocess.check_output(cmd).strip().decode('utf-8')
    is_packaging = changelog_package.endswith('-packaging')
    return is_packaging or is_repackaged_by_wazo


def list_files_to_commit():
    cmd = ['git', 'diff', '--cached', '--name-only', '--diff-filter=MA']
    output = subprocess.check_output(cmd).strip().decode('utf-8')
    if not output:
        return []
    return [l.strip() for l in output.split("\n") if not os.path.islink(l.strip())]


if __name__ == "__main__":
    main()
