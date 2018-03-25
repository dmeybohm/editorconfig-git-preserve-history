import dateutil.parser
from datetime import datetime
from typing import List, Dict, Tuple

from editorconfig_git_preserve_history.git import GitCommitInfo

ChangeList = List[Tuple[str, GitCommitInfo, 'Change']]
ChangesByCommit = Dict[str, 'Change']


class Change:
    def __init__(self):
        self.changes = {}  # type: Dict[str, List[int]]

    def add_change(self, file_path: str, line_number: int):
        if file_path not in self.changes:
            self.changes[file_path] = []
        self.changes[file_path].append(line_number)

    def files(self) -> List[str]:
        return list(self.changes.keys())

    def line_numbers_for_file(self, file_path: str) -> Dict[int, bool]:
        return {line_number: True for line_number in self.changes[file_path]}

    @classmethod
    def sort_by_date(cls, changes_by_commit: ChangesByCommit) -> ChangeList:
        result = []  # type: ChangeList
        for commit, change in changes_by_commit.items():
            # get info for the commit:
            gitinfo = GitCommitInfo.from_commit(commit)
            result.append((commit, gitinfo, change))
        result.sort(key=_sort_func)
        return result


def _sort_func(info) -> datetime:
    return dateutil.parser.parse(info[1].date)
