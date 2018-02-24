#!/usr/bin/env python

import os
import re
import sys
import tempfile

from editorconfig import get_properties, EditorConfigError

from util import run, get_contents, get_lines
from gitcommit import GitCommitInfo

changes_by_commit = {}


class Change:
    def __init__(self):
        self.changes = {}

    def add_change(self, file_path: str, line_number: int):
        if file_path not in self.changes:
            self.changes[file_path] = []
        self.changes[file_path].append(line_number)

    def files(self) -> list:
        return list(self.changes.keys())

    def line_numbers_for_file(self, file_path: str) -> dict:
        return {line_number: True for line_number in self.changes[file_path]}


def store_changes(change_file: str):
    blame = run(['git', 'blame', change_file])
    for line_number, line in enumerate(blame):
        if line == "":
            continue
        match = re.match(r'^(\S+)', line)
        if not match:
            print("Bad match:" + str(len(line)))
            raise RuntimeError("Bad match in git blame")
        commit = match.group()
        if commit not in changes_by_commit:
            changes_by_commit[commit] = Change()
        changes_by_commit[commit].add_change(change_file, line_number)


def generate_changes(editorconfig_config: dict, abspath: str, relpath: str):
    old_contents, new_contents = run_editorconfig_changes(editorconfig_config, abspath)
    if new_contents == old_contents:
        # no changes:
        return
    print("Changing " + relpath)
    store_changes(abspath)


def run_editorconfig_changes(editorconfig_config, file_path, lines_to_change={}):
    end_of_line = editorconfig_config['end_of_line']
    trim_trailing_whitespace = editorconfig_config['trim_trailing_whitespace']
    insert_final_newline = editorconfig_config['insert_final_newline']
    if end_of_line == "lf":
        eol = '\n'
    elif end_of_line == "crlf":
        eol = '\r\n'
    else:
        raise RuntimeError("Unhandled line ending")
    old_contents = get_contents(file_path)
    lines = get_lines(file_path)
    with tempfile.TemporaryFile(mode='w+t', encoding='utf-8') as tmp:
        last_line = len(lines) - 1
        for line_number, orig_line in enumerate(lines):
            modified_line = orig_line
            # Do whitespace first to not strip carriage returns:
            if trim_trailing_whitespace:
                modified_line = re.sub(r'\s*\n', '\n', modified_line)
            modified_line = re.sub(r'\r?\n', eol, modified_line)
            if line_number == last_line and insert_final_newline and '\n' not in modified_line:
                modified_line += eol
            if not lines_to_change or line_number in lines_to_change:
                tmp.write(modified_line)
            else:
                tmp.write(orig_line)
        tmp.seek(0, 0)
        new_contents = tmp.read()
        return old_contents, new_contents


def find_and_write_commits():
    modified_files = run(['git', 'ls-files', '-m'])
    if modified_files[0] != '' or len(modified_files) > 1:
        print("You have modified files!\n\nOnly run this script on a pristine tree.")
        print(modified_files)
        sys.exit(1)
    files = run(['git', 'ls-files'])
    for change_file in files:
        if change_file == "":
            continue
        try:
            abspath = os.path.abspath(change_file)
            editorconfig_options = get_properties(abspath)
            generate_changes(editorconfig_options, abspath, change_file)
        except EditorConfigError:
            print("Error occurred while getting EditorConfig properties")
    # Generate the commits:
    for commit, change in changes_by_commit.items():
        # get info for the commit:
        gitinfo = GitCommitInfo.from_commit(commit)
        for change_file in change.files():
            line_numbers = change.line_numbers_for_file(change_file)
            editorconfig_options = get_properties(change_file)
            old_contents, new_contents = run_editorconfig_changes(editorconfig_options, change_file, line_numbers)
            with open(change_file, 'w') as f:
                f.write(new_contents)
        gitinfo.impersonate_and_write_commit(change.files())


if __name__ == "__main__":
    find_and_write_commits()
