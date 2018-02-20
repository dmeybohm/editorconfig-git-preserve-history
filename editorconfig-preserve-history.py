#!/usr/bin/env python

import subprocess
import os
import re
import sys
import tempfile
from editorconfig import get_properties, EditorConfigError

changes_by_commit = {}
changes_by_file = {}


class RuntimeException(BaseException):
    pass


class Change(object):

    def __init__(self):
        self.changes = {};
        pass

    def add_change(self, file, line_number, line_contents):
        print("adding change to file: "+file)
        if file not in self.changes:
            self.changes[file] = []
        self.changes[file].append((line_number, line_contents))

    def files(self):
        return self.changes.keys()

    def line_numbers_for_file(self, file):
        numbers = {};
        for line_number, line_contents in self.changes[file]:
            numbers[line_number] = True
        return numbers


class GitInfo(object):
    def __init__(self, commit, author, date, message):
        self.commit = commit
        self.author = author
        self.date = date
        self.message = message

    def impersonate(self, files):
        message = self.message + "\nFrom-Commit: " + self.commit
        args = ['git', 'commit', '--date', self.date, '--author', self.author, '--message', message]
        output = run(args + files)

def run(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output = proc.communicate()[0]
    return output.split("\n")


def get_contents(filepath):
    with open(changefile, "r") as f:
        return f.read()


def extract_git_info(commit):
    lines = run(['git', 'log', '-1', commit])
    info = "\n".join(lines)
    rawinfo = run(['./gitinfo.php', info])
    commit = rawinfo[0]
    author = rawinfo[1]
    date = rawinfo[2]
    message = "\n".join(rawinfo[3:])
    return GitInfo(commit, author, date, message)


def get_lines(filepath):
    with open(changefile, "r") as f:
        return f.readlines()


def store_changes(changefile, contents, newcontents):
    blame = run(['git', 'blame', changefile])
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

        changes_by_commit[commit].add_change(changefile, line_number, newcontents[line_number])
        if changefile not in changes_by_file:
            changes_by_file[changefile] = []
        if commit not in changes_by_file[changefile]:
            changes_by_file[changefile].append(commit)


def generate_changes(editorconfigConfig, abspath):
    contents, newcontents = run_editorconfig_changes(editorconfigConfig, abspath)
    if newcontents == contents:
        # no changes:
        return
    store_changes(abspath, contents, newcontents)


def run_editorconfig_changes(editorconfigConfig, file, lines_to_change={}):
    end_of_line = editorconfigConfig['end_of_line']
    trim_trailing_whitespace = editorconfigConfig['trim_trailing_whitespace']
    insert_final_newline = editorconfigConfig['insert_final_newline']
    if end_of_line == "lf":
        eol = '\n'
    elif end_of_line == "crlf":
        eol = '\r\n'
    else:
        raise RuntimeException("Unhandled line ending")
    contents = get_contents(file)
    lines = get_lines(file)
    tmp = tempfile.TemporaryFile()
    lastline = len(lines) - 1
    for line_number, line in enumerate(lines):
        orig_line = line
        # Do whitespace first to not strip carriage returns:
        if trim_trailing_whitespace:
            line = re.sub(r'\s*\n', '\n', line)
        line = re.sub(r'\r?\n', eol, line)
        if line_number == lastline and insert_final_newline and '\n' not in line:
            line += eol
        if not lines_to_change or line_number in lines_to_change:
            tmp.write(line)
        else:
            tmp.write(orig_line)
    tmp.seek(0, 0)
    newcontents = tmp.read()
    return contents, newcontents


files = run(['git', 'ls-files'])
for changefile in files:
    if changefile == "":
        continue
    try:
        abspath = os.path.abspath(changefile)
        options = get_properties(abspath)
        generate_changes(options, abspath)
    except EditorConfigError:
        print("Error occurred while getting EditorConfig properties")
    # else:
    #     for key, value in options.items():
    #         print "%s=%s" % (key, value)

# Generate the commits:
for commit, change in changes_by_commit.items():
    # get info for the commit:
    gitinfo = extract_git_info(commit)
    for changefile in change.files():
        line_numbers = change.line_numbers_for_file(changefile)
        options = get_properties(changefile)
        contents, newcontents = run_editorconfig_changes(options, changefile, line_numbers)
        with open(changefile, 'w') as f:
            f.write(newcontents)
    gitinfo.impersonate(change.files())



