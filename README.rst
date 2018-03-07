editorconfig-git-preserve-history
=================================

This tool is a script that runs on a git repository that contains`editorconfig`_ files.
This rewrites all the text files in the repository to update the whitespace in accordance with
the editorconfig, but preserves history by writing new commits with the original authorship and
commit date.

The purpose of this is twofold: to maintain the original authorship of changes (as reported
by git blame) due only to editorconfig, thus making the original authorship information more accessible even
when using editorconfig, and also to avoid the hassle of having to handle large
numbers of changes due to files that are drastically different from what's
configured in an .editorconfig.

By rewriting all the whitespace at once with this tool, you can keep your
editorconfig plugin in your editor enabled, and avoid unnecessary whitespace changes
in other, more important code changes.

Installation
------------

Python 3.5 or later is required. On macOS, you can install `homebrew` first and then:

.. code:: sh

    brew install python3

With pip
--------

After installing Python 3

.. code:: sh

    pip3 install EditorConfigGitPreserveHistory



Running
-------

.. code:: sh

    editorconfig-git-preserve-history

The script will write commits into your current branch that reformat according
to the `.editorconfig` that applies to each file in your repository. It will
also add "Impersonator:" and "Original-Commit:" lines to the commit message of each
commit to reference back to the previous commit and inform whoever looks at the
log who created this whitespace commit. It looks like this:

.. code::

    commit 0e5f0feb7f9453b2fc8595f3db7835dbfe57db0e
    Author: Original Author <originalauthor@example.com>
    Date:   Mon Feb 19 20:33:06 2018 -0500

    Add editorconfig module to requirements.txt
    
    Original-Commit: 0e9d1d4bd3fe4cb278ed785bdb229e519eccc857
    Impersonator: New Author <newauthor@example.com>

You can then put those commits up on github and issue a pull request to change all the whitespace in
your project, but preserve the original authorship.

This way, if you do `git blame` you will still see the original author
of each line, but the whitespace will also be updated.

Developing
----------

Create a virtual environment with the venv module:

.. code:: sh

    python3 -m venv venv

Then activate the environment and install the requirements from the `requirements.txt` file:

.. code:: sh

    . venv/bin/activate
    pip install -r requirements.txt

Be sure to run the tests with nosetests before issuing a PR:

.. code:: sh

    nosetests

You can also run `mypy`, the Python static analyzer, to check for typing errors:

.. code:: sh

    mypy --ignore-missing-imports -p editorconfig_git_preserve_history

.. _editorconfig: http://editorconfig.org