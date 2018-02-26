from .util import run


def haschanges() -> bool:
    lines = run(['git', 'status', '--porcelain'])
    for line in lines:
        if line == '':
            continue
        if line.startswith(' '):
            line = line[1:]
        if line[0] == 'M' or line[0] == 'A' or line[0] == 'D':
            return True
    return False
