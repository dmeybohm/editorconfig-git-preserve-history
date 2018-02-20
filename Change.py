
class Change(object):

    def __init__(self):
        self.changes = {};
        pass

    def add_change(self, file, line_number, line_contents):
        if not file in self.changes:
            self.changes[file] = []
        self.changes[file].append((line_number, line_contents))

    def files(self):
        return self.changes.keys()
