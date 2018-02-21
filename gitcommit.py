import re
from util import run


class GitCommitInfo(object):
    def __init__(self, commit, author, date, message):
        self.commit = commit
        self.author = author
        self.date = date
        self.message = message

    @classmethod
    def from_commit(cls, commit):
        lines = run(['git', 'log', '-1', commit])
        commit_log = "\n".join(lines)
        commit, author, date, message = match_parts(commit_log)
        return GitCommitInfo(commit, author, date, message)

    def impersonate_and_write_commit(self, files):
        print("Overwriting " + self.commit + " (Impersonating " + self.author + ")")
        message = self.message + "\n\nFrom-Commit: " + self.commit
        args = ['git', 'commit', '--date', self.date, '--author', self.author, '--message', message]
        output = run(args + files)


def match_commit(commit_log):
    return re.search(r'^commit (\S+)', commit_log, re.M).group(1)


def match_author(commit_log):
    return re.search(r'^Author: (.+)', commit_log, re.M).group(1)


def match_date(commit_log):
    return re.search(r"^Date: \s*(.*)$", commit_log, re.M).group(1)


def match_message(commit_log):
    commit_log = re.sub(r"^(.*)\n\n", '', commit_log, 0, re.M|re.S)
    commit_log = re.sub(r"^\s{4}", '', commit_log, 0, re.M)
    return commit_log


def match_parts(commit_log):
    commit = match_commit(commit_log)
    author = match_author(commit_log)
    date = match_date(commit_log)
    message = match_message(commit_log)
    return commit, author, date, message