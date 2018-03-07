import subprocess
import locale
from typing import List

UNICODE_ESCAPING = "surrogateescape"
ASCII_ENCODING = "ascii"


def run(cmd: List[str], encoding: str = None) -> List[str]:
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output = proc.communicate()[0]
    if encoding is None:
        encoding = locale.getpreferredencoding()
    output_str = output.decode(encoding)
    if len(output_str) > 0 and output_str[-1] == '\n':
        output_str = output_str[:-1]
    return output_str.split("\n")


def get_contents(file_path: str, use_ascii: bool = False) -> str:
    if use_ascii:
        with open(file_path, "rb") as fb:
            return fb.read().decode(ASCII_ENCODING, errors=UNICODE_ESCAPING)
    else:
        with open(file_path, "rt") as ft:
            return ft.read()


def get_lines(file_path: str, use_ascii: bool = False) -> List[str]:
    if use_ascii:
        with open(file_path, "rt", encoding=ASCII_ENCODING,
                  errors=UNICODE_ESCAPING) as f:
            return f.readlines()
    else:
        with open(file_path, "rt") as f:
            return f.readlines()


def hide_unicode(s: str) -> bytes:
    return s.encode(ASCII_ENCODING, errors=UNICODE_ESCAPING)


def unhide_unicode(b: bytes) -> str:
    return b.decode(ASCII_ENCODING, errors=UNICODE_ESCAPING)