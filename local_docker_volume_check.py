#!/usr/bin/env python3
# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import subprocess
import sys


def main():
    files = list_files_changed_with_local_git_repos()

    if files:
        print("ERROR: Modification with LOCAL_GIT_REPOS detected. Refusing to commit.")
        sys.exit(1)


def list_files_changed_with_local_git_repos():
    """
    We do not want commits containing uncommented lines using LOCAL_GIT_REPOS.
    Those lines should stay commented when committed
    """

    cmd = ['git', 'diff', '--staged', '--name-only', '-G^\s+-\s+"?\$\{LOCAL_GIT_REPOS\}']
    output = subprocess.check_output(cmd).strip().decode('utf-8')
    if not output:
        return []
    return [l.strip() for l in output.split("\n") if not os.path.islink(l.strip())]


if __name__ == "__main__":
    main()
