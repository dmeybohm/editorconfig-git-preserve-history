import unittest
import gitcommit

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


class GitCommitTest(unittest.TestCase):
    def test_match_commit(self):
        commit = gitcommit.match_commit(test_commit)
        self.assertEquals("9471e20cebc84f5931c77eb2bf6c8eb004ed2305", commit)

    def test_match_author_at_beginning(self):
        author = gitcommit.match_author("Author: Cheese")
        self.assertEquals("Cheese", author)

    def test_match_author_after_something(self):
        author = gitcommit.match_author("SOmething\nAuthor: Cheese")
        self.assertEquals("Cheese", author)

    def test_match_author_in_middle(self):
        author = gitcommit.match_author(test_commit)
        self.assertEquals("A User <user@example.org>", author)

    def test_match_date(self):
        date = gitcommit.match_date(test_commit)
        self.assertEquals('Tue Feb 20 00:52:25 2018 -0500', date)

    def test_match_message(self):
        message = gitcommit.match_message(test_commit)
        self.assertEquals(commit_message, message)

    def test_match_parts(self):
        commit, author, date, message = gitcommit.match_parts(test_commit)
        self.assertIsNotNone(commit)
        self.assertIsNotNone(author)
        self.assertIsNotNone(date)
        self.assertIsNotNone(message)


if __name__ == "__main__":
    unittest.main()