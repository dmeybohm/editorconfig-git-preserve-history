import subprocess
import locale
from typing import List, AnyStr


def run(cmd: List[str], encoding: str = None) -> List[str]:
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output = proc.communicate()[0]
    if encoding is None:
        encoding = locale.getpreferredencoding()
    output_str = output.decode(encoding)
    if len(output_str) > 0 and output_str[-1] == '\n':
        output_str = output_str[:-1]
    return output_str.split("\n")


def get_contents(file_path: str, encoding: str = None, mode: str = None) -> AnyStr:
    if mode is None:
        mode = 't'
    if encoding is None:
        with open(file_path, "r" + mode) as ft:
            return ft.read()
    else:
        with open(file_path, "r" + mode, encoding=encoding) as ft:
            return ft.read()


def get_lines(file_path: str, encoding: str = None) -> List[str]:
    if encoding is None:
        with open(file_path, "rt") as f:
            return f.readlines()
    else:
        with open(file_path, "rt", encoding=encoding) as f:
            return f.readlines()
