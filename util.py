import subprocess


def run(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output = proc.communicate()[0]
    return output.split("\n")


def get_contents(file_path):
    with open(file_path, "r") as f:
        return f.read()


def get_lines(file_path):
    with open(file_path, "r") as f:
        return f.readlines()



