
class Change(object):

    def __init__(self):
        self.changes = {};
        pass

    def add_change(self, file, lineNumber, lineContents):
        if not file in self.changes:
            self.changes[file] = []
        self.changes[file].append((lineNumber, lineContents))