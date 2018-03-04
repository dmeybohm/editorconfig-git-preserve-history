#!/usr/bin/env python3
import os
import re
import sys
from typing import Dict
from editorconfig import get_properties, EditorConfigError

from . import gitstatus
from .change import Change
from .util import run
from .gitcommit import GitCommitInfo
from .replace import replace_editorconfig

changes_by_commit = {}  # type: Dict[str, 'Change']


def store_changes(change_file: str):
    blame = run(['git', 'blame', change_file])
    for line_number, line in enumerate(blame):
        if len(line) == 0:
            continue
        match = re.match(r'^(\S+)', line)
        if not match:
            print("Bad match:" + str(len(line)))
            raise RuntimeError("Bad match in git blame")
        commit = match.group()
        if commit not in changes_by_commit:
            changes_by_commit[commit] = Change()
        changes_by_commit[commit].add_change(change_file, line_number)


def generate_changes(editorconfig: dict, abspath: str, relpath: str):
    old_contents, new_contents = replace_editorconfig(editorconfig, abspath)
    if new_contents == old_contents:
        # no changes:
        return
    print("Changing " + relpath)
    store_changes(abspath)


def find_and_write_commits():
    if gitstatus.haschanges():
        print("You have modified files!\n\n")
        print("Only run this script on a pristine tree.")
        sys.exit(1)
    files = run(['git', 'ls-files'])
    for change_file in files:
        if len(change_file) == 0:
            continue
        try:
            abspath = os.path.abspath(change_file)
            editorconfig = get_properties(abspath)
            generate_changes(editorconfig, abspath, change_file)
        except EditorConfigError:
            print("Error occurred while getting EditorConfig properties")
    # Generate the commits:
    for commit, change in changes_by_commit.items():
        # get info for the commit:
        gitinfo = GitCommitInfo.from_commit(commit)
        for change_file in change.files():
            line_numbers = change.line_numbers_for_file(change_file)
            editorconfig = get_properties(change_file)
            old_contents, new_contents = replace_editorconfig(editorconfig,
                                                     change_file,
                                                     line_numbers)
            with open(change_file, 'w') as f:
                f.write(new_contents)
        gitinfo.impersonate_and_write_commit(change.files())


if __name__ == "__main__":
    find_and_write_commits()
