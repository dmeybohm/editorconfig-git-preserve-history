#!/usr/bin/env python

import subprocess
import os
import re
import sys
import tempfile
from editorconfig import get_properties, EditorConfigError

changes_by_commit = {}


class RuntimeException(BaseException):
    pass


class Change(object):
    def __init__(self):
        self.changes = {}

    def add_change(self, file_path, line_number):
        if file_path not in self.changes:
            self.changes[file_path] = []
        self.changes[file_path].append(line_number)

    def files(self):
        return self.changes.keys()

    def line_numbers_for_file(self, file_path):
        return {line_number: True for line_number in self.changes[file_path]}


class GitInfo(object):
    def __init__(self, commit, author, date, message):
        self.commit = commit
        self.author = author
        self.date = date
        self.message = message

    @classmethod
    def from_commit(cls, commit):
        lines = run(['git', 'log', '-1', commit])
        info = "\n".join(lines)
        rawinfo = run(['./gitinfo.php', info])
        commit = rawinfo[0]
        author = rawinfo[1]
        date = rawinfo[2]
        message = "\n".join(rawinfo[3:])
        return GitInfo(commit, author, date, message)

    def impersonate_and_write_commit(self, files):
        print("Overwriting " + self.commit + " (Impersonating " + self.author + ")")
        message = self.message + "\n\nFrom-Commit: " + self.commit
        args = ['git', 'commit', '--date', self.date, '--author', self.author, '--message', message]
        output = run(args + files)


def run(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output = proc.communicate()[0]
    return output.split("\n")


def get_contents(filepath):
    with open(filepath, "r") as f:
        return f.read()


def get_lines(filepath):
    with open(filepath, "r") as f:
        return f.readlines()


def store_changes(change_file):
    blame = run(['git', 'blame', change_file])
    for line_number, line in enumerate(blame):
        if line == "":
            continue
        match = re.match(r'^(\S+)', line)
        if not match:
            print("Bad match:" + str(len(line)))
            raise RuntimeException("Bad match in git blame")
        commit = match.group()
        if commit not in changes_by_commit:
            changes_by_commit[commit] = Change()
        changes_by_commit[commit].add_change(change_file, line_number)


def generate_changes(editorconfig_config, abspath, relpath):
    contents, newcontents = run_editorconfig_changes(editorconfig_config, abspath)
    if newcontents == contents:
        # no changes:
        return
    print("Changing " + relpath)
    store_changes(abspath)


def run_editorconfig_changes(editorconfig_config, file, lines_to_change={}):
    end_of_line = editorconfig_config['end_of_line']
    trim_trailing_whitespace = editorconfig_config['trim_trailing_whitespace']
    insert_final_newline = editorconfig_config['insert_final_newline']
    if end_of_line == "lf":
        eol = '\n'
    elif end_of_line == "crlf":
        eol = '\r\n'
    else:
        raise RuntimeException("Unhandled line ending")
    old_contents = get_contents(file)
    lines = get_lines(file)
    with tempfile.TemporaryFile() as tmp:
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
        gitinfo = GitInfo.from_commit(commit)
        for change_file in change.files():
            line_numbers = change.line_numbers_for_file(change_file)
            editorconfig_options = get_properties(change_file)
            old_contents, new_contents = run_editorconfig_changes(editorconfig_options, change_file, line_numbers)
            with open(change_file, 'w') as f:
                f.write(new_contents)
        gitinfo.impersonate_and_write_commit(change.files())


if __name__ == "__main__":
    find_and_write_commits()
