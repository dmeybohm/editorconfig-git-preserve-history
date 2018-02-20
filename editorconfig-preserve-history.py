#!/usr/bin/env python

import subprocess
import os
from editorconfig import get_properties, EditorConfigError

def run(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output = proc.communicate()[0]
    return output.split("\n")


for file in run(['git', 'ls-files']):
    if file == "":
        continue
    print("file: "+file)
    try:
        options = get_properties(os.path.abspath(file))
    except EditorConfigError:
        print "Error occurred while getting EditorConfig properties"
    else:
        for key, value in options.items():
            print "%s=%s" % (key, value)
