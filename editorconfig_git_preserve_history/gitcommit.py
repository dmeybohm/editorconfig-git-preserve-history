import re
from typing import List

from util import run


class GitCommitInfo:
    def __init__(self, commit: str, author: str, date: str,
                 message: str) -> None:
        self.commit = commit
        self.author = author
        self.date = date
        self.message = message

    @classmethod
    def from_commit(cls, commit: str) -> 'GitCommitInfo':
        lines = run(['git', 'log', '-1', commit])
        commit_log = "\n".join(lines)
        commit = match_commit(commit_log)
        author = match_author(commit_log)
        date = match_date(commit_log)
        message = match_message(commit_log)
        return GitCommitInfo(commit, author, date, message)

    def impersonate_and_write_commit(self, files: List[str]) -> None:
        print("Overwriting " + self.commit + " (Impersonating " +
              self.author + ")")
        message = self.message + "\n\nFrom-Commit: " + self.commit
        args = ['git', 'commit', '--date', self.date, '--author', self.author,
                '--message', message]
        output = run(args + files)


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
