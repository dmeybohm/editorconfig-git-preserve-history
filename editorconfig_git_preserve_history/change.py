from typing import List, Dict


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