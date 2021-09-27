import io
import os


class FileCheck:
    def __init__(self, path):
        self.path = path
        self.buffer = io.StringIO()

    def __enter__(self):
        return self.buffer

    def __exit__(self, exc_type, exc_val, exc_tb):
        if os.path.isfile(self.path):
            with open(self.path, 'r') as hr:
                actual = hr.read()
                if self.buffer.getvalue() == actual:
                    print("File '{}' has not changed".format(self.path))
                    return
        with open(self.path, 'w') as hr:
            hr.write(self.buffer.getvalue())
