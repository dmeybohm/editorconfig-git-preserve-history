#!/bin/sh

# Hidden in a .travis dir to avoid running it outside travis

# Test installing the package with pip-install and then
# running it on a previous version of its own repository
pip install -e .
git clone . clonetest 
cd clonetest 
git checkout -b clone-test 153c40eae86411b674e95235b4a66c8b4ee16024 
editorconfig-git-preserve-history
