from typing import List
from .util import run


def list_git_files() -> List[str]:
    return run(['git', 'grep', '-I', '-l', '.'])