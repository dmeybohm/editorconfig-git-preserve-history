import re
from typing import List
from .util import run


class GitCommitInfo:
    def __init__(self, commit: str, author: str, date: str,
                 message: str) -> None:
        self.commit = commit
        self.author = author
        self.date = date
        self.message = message

    @classmethod
    def from_commit(cls, commit: str) -> 'GitCommitInfo':
        if commit.startswith('^'):
            commit = commit[1:]
        lines = run(['git', 'log', '-1', commit])
        commit_log = "\n".join(lines)
        return cls.from_commit_log(commit, commit_log)

    @classmethod
    def from_commit_log(cls, commit: str, commit_log: str):
        try:
            commit = match_commit(commit_log)
            author = match_author(commit_log)
            date = match_date(commit_log)
            message = match_message(commit_log)
        except AttributeError:
            print("Failed to parse commit {} for commit log: {}".format(commit, commit_log))
            raise
        return GitCommitInfo(commit, author, date, message)

    def impersonate_and_write_commit(self, files: List[str]) -> None:
        print("Overwriting " + self.commit + " (Impersonating " +
              self.author + ")")
        impersonator_email = run(['git', 'config', 'user.email'])[0]
        impersonator_name = run(['git', 'config', 'user.name'])[0]
        message = self.message + "\n\nFrom-Commit: " + self.commit + "\n" + \
            "Impersonator: {} <{}>".format(impersonator_name, impersonator_email)
        args = ['git', 'commit', '--date', self.date, '--author', self.author,
                '--message', message]
        run(args + files)


def match_commit(commit_log: str) -> str:
    return re.search(r'^commit (\S+)', commit_log, re.M).group(1)


def match_author(commit_log: str) -> str:
    return re.search(r'^Author: (.+)', commit_log, re.M).group(1)


def match_date(commit_log: str) -> str:
    return re.search(r"^Date: \s*(.*)$", commit_log, re.M).group(1)


def match_message(commit_log: str) -> str:
    commit_log = re.sub(r"^(.*)\n\n", '', commit_log, 0, re.M | re.S)
    commit_log = re.sub(r"^\s{4}", '', commit_log, 0, re.M)
    return commit_log


def has_changes() -> bool:
    lines = run(['git', 'status', '--porcelain'])
    for line in lines:
        if len(line) == 0:
            continue
        if line.startswith(' '):
            line = line[1:]
        if line[0] == 'M' or line[0] == 'A' or line[0] == 'D':
            return True
    return False


def list_text_files() -> List[str]:
    return run(['git', 'grep', '-I', '-l', '.'])
