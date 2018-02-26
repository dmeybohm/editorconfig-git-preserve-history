import subprocess
import locale
from typing import List


def run(cmd: List[str], encoding: str = None) -> List[str]:
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output = proc.communicate()[0]
    if encoding is None:
        encoding = locale.getpreferredencoding()
    return output.decode(encoding).split("\n")


def get_contents(file_path: str) -> str:
    with open(file_path, "rt") as f:
        return f.read()


def get_lines(file_path: str) -> List[str]:
    with open(file_path, "rt") as f:
        return f.readlines()
