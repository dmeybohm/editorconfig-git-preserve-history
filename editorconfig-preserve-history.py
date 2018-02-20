#!/usr/bin/env python

import subprocess
import os
import Change
import re
import sys
from editorconfig import get_properties, EditorConfigError

commits = {}


def run(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output = proc.communicate()[0]
    return output.split("\n")


def generate_changes(editorconfigConfig, file):
    end_of_line = editorconfigConfig['end_of_line']
    blame = run(['git', 'blame', file])
    if end_of_line == "lf":
        repl = '\n'
    elif end_of_line == "crlf":
        repl = '\r\n'
    else:
        raise "Unhandled line ending"
    with open(file, "r") as f:
        contents = f.read()
    print("contents: "+contents)
    with open(file, "r") as f:
        lines = f.readlines()
        for line in lines:
            new_line = re.sub(r"\r?\n$", repl, line)
            sys.stdout.write(new_line)


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