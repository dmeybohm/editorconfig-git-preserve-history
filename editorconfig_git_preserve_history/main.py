#!/usr/bin/env python3
import os
import re
import sys

from typing import Dict
from editorconfig import get_properties, EditorConfigError

from . import git
from .change import Change, ChangesByCommit, ChangeList
from .util import run
from .git import GitCommitInfo
from .replace import replace_editorconfig, FILE_ENCODING

changes_by_commit = {}  # type: ChangesByCommit


def store_changes(change_file: str, old_contents: bytes, new_contents: bytes):
    # TODO: handle \r line separator here:
    old_str = old_contents.decode(FILE_ENCODING).split("\n")
    new_str = new_contents.decode(FILE_ENCODING).split("\n")

    blame = run(['git', 'blame', change_file])
    for line_number, line in enumerate(blame):
        if len(line) == 0:
            continue
        if old_str[line_number] == new_str[line_number]:
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
    store_changes(abspath, old_contents, new_contents)


def find_and_write_commits():
    if git.has_changes():
        print("You have modified files!\n\n")
        print("Only run this script on a pristine tree.")
        sys.exit(1)
    for change_file in git.list_text_files():
        if len(change_file) == 0:
            continue
        try:
            abspath = os.path.abspath(change_file)
            editorconfig = get_properties(abspath)
            generate_changes(editorconfig, abspath, change_file)
        except EditorConfigError:
            print("Error occurred while getting EditorConfig properties")
    # Generate the commits:
    changes_sorted = Change.sort_by_date(changes_by_commit)
    for commit, gitinfo, change in changes_sorted:
        for change_file in change.files():
            line_numbers = change.line_numbers_for_file(change_file)
            editorconfig = get_properties(change_file)
            old_contents, new_contents = replace_editorconfig(editorconfig,
                                                              change_file,
                                                              line_numbers)
            with open(change_file, 'wb') as f:
                f.write(new_contents)
        gitinfo.impersonate_and_write_commit(change.files())


if __name__ == "__main__":
    find_and_write_commits()
