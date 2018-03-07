import re
import tempfile
from typing import Dict, Tuple

from .util import get_contents, get_lines


def replace_editorconfig(editorconfig: dict, file_path: str,
                         lines_to_change: Dict[int, bool] = {}) -> Tuple[str, str]:
    end_of_line = None
    if 'end_of_line' in editorconfig:
        end_of_line = editorconfig['end_of_line']
    trim_trailing_whitespace = False
    if 'trim_trailing_whitespace' in editorconfig:
        trim_trailing_whitespace = editorconfig['trim_trailing_whitespace']
    insert_final_newline = False
    if 'insert_final_newline' in editorconfig:
        insert_final_newline = editorconfig['insert_final_newline']

    indent_style = None
    if 'indent_style' in editorconfig:
        indent_style = editorconfig['indent_style']
    if end_of_line == "lf":
        eol = '\n'
    elif end_of_line == "crlf":
        eol = '\r\n'
    elif end_of_line == "cr":
        raise RuntimeError("Unhandled line ending")

    old_contents = get_contents(file_path)
    lines = get_lines(file_path)
    with tempfile.TemporaryFile(mode='w+t') as tmp:
        last_line = len(lines) - 1
        for line_number, orig_line in enumerate(lines):
            modified_line = orig_line

            # Do whitespace first to not strip carriage returns:
            if trim_trailing_whitespace:
                modified_line = re.sub(r'\s*\n', '\n', modified_line)
            if end_of_line is not None:
                modified_line = re.sub(r'\r?\n', eol, modified_line)

            # Handle spaces vs tabs:
            if indent_style == 'tab':
                modified_line = expand_to_tabs(editorconfig, modified_line)
            elif indent_style == 'space':
                modified_line = expand_to_spaces(editorconfig, modified_line)

            # Insert final newline
            if line_number == last_line and \
                    insert_final_newline and '\n' not in modified_line:
                modified_line += eol

            # Write either the modified line or the original line:
            if not lines_to_change or line_number in lines_to_change:
                tmp.write(modified_line)
            else:
                tmp.write(orig_line)

        tmp.seek(0, 0)
        new_contents = tmp.read()
        return old_contents, new_contents


def expand_to_spaces(editorconfig: dict, modified_line: str) -> str:
    indent_size, tab_size = get_indent_sizes(editorconfig)
    return replace_leading_tabs_with_spaces(modified_line, indent_size)


def expand_to_tabs(editorconfig: dict, modified_line: str) -> str:
    indent_size, tab_size = get_indent_sizes(editorconfig)
    return replace_leading_spaces_with_tabs(modified_line, indent_size, tab_size)


def get_indent_sizes(editorconfig: dict) -> Tuple[int, int]:
    indent_size = get_indent_size(editorconfig)
    tab_size = get_tab_size(editorconfig)
    return indent_size, tab_size


def get_tab_size(editorconfig: dict, no_recurse: bool = False) -> int:
    if 'tab_width' in editorconfig:
        tab_size = int(editorconfig['tab_width'])
    else:
        if no_recurse:
            tab_size = 4
        else:
            tab_size = get_indent_size(editorconfig)
    return tab_size


def get_indent_size(editorconfig: dict) -> int:
    indent_size = 4
    if 'indent_size' in editorconfig:
        indent_size = editorconfig['indent_size']
        if indent_size == 'tab':
            indent_size = get_tab_size(editorconfig, True)
        else:
            indent_size = int(indent_size)
    return indent_size


def replace_leading_tabs_with_spaces(line: str, indent_size: int) -> str:
    # Count leading whitespace and convert it all to spaces:
    match = re.match(r'^([ \t]+)', line)
    if match is None:
        return line
    leading_whitespace = match.group(1)
    line = line[len(leading_whitespace):]
    leading_whitespace = leading_whitespace.replace('\t', ' ' * indent_size)
    return leading_whitespace + line


def replace_leading_spaces_with_tabs(line: str, indent_size: int,
                                     tab_size: int) -> str:
    # Count leading whitespace and convert it all to spaces:
    match = re.match(r'^([ \t]+)', line)
    if match is None:
        return line
    leading_whitespace = match.group(1)
    line = line[len(leading_whitespace):]
    # Convert all leading spaces that will match into tabs:
    leading_whitespace = replace_leading_tabs_with_spaces(leading_whitespace,
                                                          tab_size)
    total_len = len(leading_whitespace)
    num_tabs = int(total_len / indent_size)
    num_spaces = int(total_len % indent_size)
    tabs_str = '\t' * num_tabs
    return tabs_str + (' ' * num_spaces) + line
