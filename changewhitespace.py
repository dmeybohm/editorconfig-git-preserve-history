

def apply_changes(editorconfigConfig, file):
    end_of_line = editorconfigConfig['end_of_line']
    with open(file, "r") as f:
        contents = f.read()
    print("contents: "+contents)
    with open(file, "r") as f:
        lines = f.readlines()
        for line in lines:
            pass
