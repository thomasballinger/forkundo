import code
import os
import sys


class ForkUndoConsole(code.InteractiveConsole):
    def __init__(self):
        code.InteractiveConsole.__init__(self)
        self.write_to_parent_fd = None
        self.read_from_child_fd = None

    def read_line(self, prompt=""):
        while True:  # each time through this loop is another
            s = input(prompt)
            if s == 'undo':
                os.write(self.write_to_parent_fd, b'done\n')
                sys.exit()
            read_fd, write_fd = os.pipe()

            if os.fork():  # this is the parent
                self.read_from_child_fd = read_fd
                # blocking read to wait for child to die
                os.read(self.read_from_child_fd, 1)
            else:  # this is the parent
                self.write_to_parent_fd = write_fd
                return s


if __name__ == '__main__':
    console = ForkUndoConsole()
    while True:
        src = console.read_line('>>> ')
        console.runsource(src)
