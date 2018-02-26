import subprocess
import locale
from typing import List


def run(cmd: List[str], encoding: str = None) -> List[str]:
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output = proc.communicate()[0]
    if encoding is None:
        encoding = locale.getpreferredencoding()
    output_str = output.decode(encoding)
    if len(output_str) > 0 and output_str[-1] == '\n':
        output_str = output_str[:-1]
    return output_str.split("\n")


def get_contents(file_path: str) -> str:
    with open(file_path, "rt") as f:
        return f.read()


def get_lines(file_path: str) -> List[str]:
    with open(file_path, "rt") as f:
        return f.readlines()
