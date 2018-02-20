#!/usr/bin/env python

import os
import subprocess

def run(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output = proc.communicate()[0]
    return output

files = run("git ls-files")
print(files)