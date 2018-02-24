import subprocess
import locale


def run(cmd, encoding=None):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output = proc.communicate()[0]
    if encoding is None:
        encoding = locale.getpreferredencoding()
    return output.decode(encoding).split("\n")


def get_contents(file_path):
    with open(file_path, "r") as f:
        return f.read()


def get_lines(file_path):
    with open(file_path, "r") as f:
        return f.readlines()



