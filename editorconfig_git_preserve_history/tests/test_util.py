import unittest
import os
from editorconfig_git_preserve_history.util import run, get_contents, get_lines


test_path = os.path.dirname(os.path.abspath(__file__)) + '/test_util.py'


class UtilTest(unittest.TestCase):
    def test_get_contents(self):
        contents = get_contents(test_path)
        self.assertIsNotNone(contents)
        self.assertTrue(contents.startswith('import unittest'))

    def test_get_lines(self):
        lines = get_lines(test_path)
        self.assertIsNotNone(lines)
        self.assertGreater(len(lines), 0)
        self.assertEqual('import unittest\n', lines[0])

    def test_run(self):
        files = run(['ls'])
        self.assertIsNotNone(files)
        self.assertGreater(len(files), 0)


if __name__ == "__main__":
    unittest.main()
