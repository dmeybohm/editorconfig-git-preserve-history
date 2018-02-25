#!/bin/sh

# Hidden in a .travis dir to avoid running it outside travis

cat > .editorconfig << EOF
# editorconfig.org
root = true

[*]
indent_style = tab
indent_size = 4
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true
EOF

# Test installing the package with pip-install and then
# running it on a previous version of its own repository
pip install -e .
git clone . clonetest 
cd clonetest 
git checkout -b clone-test 153c40eae86411b674e95235b4a66c8b4ee16024 
for i in $(git ls-files)
do
    git blame "$i"
done
editorconfig-git-preserve-history
