#!/usr/bin/env python

import subprocess
import os
import Change
import re
import sys
import tempfile
from editorconfig import get_properties, EditorConfigError

commits = {}


class RuntimeException(BaseException):
    pass


def run(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output = proc.communicate()[0]
    return output.split("\n")


def get_contents(filepath):
    with open(file, "r") as f:
        return f.read()

def get_lines(filepath):
    with open(file, "r") as f:
        return f.readlines()


def store_changes(file, contents, newcontents):
    blame = run(['git', 'blame', file])
    for line_number, line in enumerate(blame):
        if line == "":
            continue
        print("Line: "+line)
        match = re.match(r'^(\S+) ', line)
        if not match:
            print("Bad match:" +str(len(line)))

            raise RuntimeException("Bad match in git blame")
        group = match.lastgroup
        print(group)


def generate_changes(editorconfigConfig, file):
    contents, newcontents = run_editorconfig_changes(editorconfigConfig, file)
    print("file: "+file+": "+str(len(newcontents)))
    if newcontents == contents:
        # no changes:
        return
    store_changes(file, contents, newcontents)


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
        # Do whitespace first to not strip carriage returns:
        if trim_trailing_whitespace:
            line = re.sub(r'\s*\n', '\n', line)
        line = re.sub(r'\r?\n', eol, line)
        if line_number == lastline and insert_final_newline and '\n' not in line:
            line += eol
        if not lines_to_change or lines_to_change[line_number]:
            tmp.write(line)
    tmp.seek(0, 0)
    newcontents = tmp.read()
    return contents, newcontents


files = run(['git', 'ls-files'])
for file in files:
    if file == "":
        continue
    try:
        abspath = os.path.abspath(file)
        options = get_properties(abspath)
        generate_changes(options, abspath)
    except EditorConfigError:
        print "Error occurred while getting EditorConfig properties"
    else:
        for key, value in options.items():
            print "%s=%s" % (key, value)

# Generate the commits:
for file in files:
    pass