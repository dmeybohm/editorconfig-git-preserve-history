import unittest
import os
import json
from editorconfig_git_preserve_history.util import get_contents
from editorconfig_git_preserve_history.replace import (
    replace_editorconfig,
    replace_leading_spaces_with_tabs,
    replace_leading_tabs_with_spaces,
    FILE_ENCODING
)


class UtilTest(unittest.TestCase):

    def test_replace_leading_spaces_with_tabs_with_no_leading_space(self):
        result = replace_leading_spaces_with_tabs('if test:', 4, 4)
        self.assertEqual('if test:', result);

    def test_replace_leading_spaces_with_tabs(self):
        result = replace_leading_spaces_with_tabs('    if test:', 2, 4)
        self.assertEqual('\t\tif test:', result)

    def test_replace_leading_spaces_with_tab_in_middle(self):
        result = replace_leading_spaces_with_tabs('  \t  if test:', 4, 4)
        self.assertEqual('\t\tif test:', result)

    def test_replace_leading_spaces_with_tab_at_end(self):
        result = replace_leading_spaces_with_tabs('  \tif test:', 4, 4)
        self.assertEqual('\t  if test:', result)

    def test_replace_leading_tabs_with_spaces(self):
        result = replace_leading_tabs_with_spaces('\t  \tif test:', 4)
        self.assertEquals((' ' * 8) + '  if test:', result)

    def test_replace_editorconfig_test_cases_in_data_dir(self):
        datadir = os.path.dirname(__file__) + '/data/'
        for dir in os.listdir(datadir):
            top_dir = datadir + dir + '/'
            with self.subTest(datadir=top_dir):
                editorconfig = json.loads(get_contents(top_dir + 'editorconfig.json'))
                input = top_dir + 'input.txt'
                expected = get_contents(top_dir + 'output.txt', mode='b')
                old_contents, new_contents = replace_editorconfig(editorconfig, input)
                self.assertEqual(expected, new_contents, "Failed in " + top_dir)


if __name__ == "__main__":
    unittest.main()
