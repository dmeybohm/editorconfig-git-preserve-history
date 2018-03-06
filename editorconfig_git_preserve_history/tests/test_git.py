import unittest

import editorconfig_git_preserve_history.git as git

test_commit = """commit 9471e20cebc84f5931c77eb2bf6c8eb004ed2305
Author: A User <user@example.org>
Date:   Tue Feb 20 00:52:25 2018 -0500

    Move back to CRLF
    
    And test big message..
    Fix gitinfo.php
"""

commit_message = """Move back to CRLF

And test big message..
Fix gitinfo.php
"""


class GitTest(unittest.TestCase):
    def test_match_commit(self):
        commit = git.match_commit(test_commit)
        self.assertEqual("9471e20cebc84f5931c77eb2bf6c8eb004ed2305", commit)

    def test_match_author_at_beginning(self):
        author = git.match_author("Author: Cheese")
        self.assertEqual("Cheese", author)

    def test_match_author_after_something(self):
        author = git.match_author("SOmething\nAuthor: Cheese")
        self.assertEqual("Cheese", author)

    def test_match_author_in_middle(self):
        author = git.match_author(test_commit)
        self.assertEqual("A User <user@example.org>", author)

    def test_match_date(self):
        date = git.match_date(test_commit)
        self.assertEqual('Tue Feb 20 00:52:25 2018 -0500', date)

    def test_match_message(self):
        message = git.match_message(test_commit)
        self.assertEqual(commit_message, message)


if __name__ == "__main__":
    unittest.main()
