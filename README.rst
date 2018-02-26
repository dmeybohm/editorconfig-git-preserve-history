editorconfig-git-preserve-history
=================================

This will read `editorconfig` files and preserve history by writing new commits with the original authorship and date but with the 
whitespace updated.

Installation
------------

Python 3.5 or later is required. On macOS, you can install `homebrew` first and then:

.. code:: sh

    brew install python3

With pip
--------

After installing Python 3

.. code:: sh

    pip install EditorConfigGitPreserveHistory



Running
-------

.. code:: sh

    editorconfig-git-preserve-history


Developing
----------

Create a virtual environment with the venv module:

.. code:: sh

    python3 -m venv venv

Then activate the environment and install the requirements from the `dev-requirements.txt` file:

.. code:: sh

    . venv/bin/activate
    pip install -r requirements.txt

Be sure to run the tests with nosetests before issuing a PR:

.. code:: sh

    nosetests

You can also run `mypy`, the Python static analyzer, to check for typing errors:

.. code:: sh

    mypy --ignore-missing-imports -p editorconfig_git_preserve_history
