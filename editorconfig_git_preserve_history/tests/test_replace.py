import unittest
from editorconfig_git_preserve_history.replace import (
    replace_leading_spaces_with_tabs,
    replace_leading_tabs_with_spaces
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


if __name__ == "__main__":
    unittest.main()
