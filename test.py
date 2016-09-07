import code
import os
import sys

write_to_parent_fd = None

def read_line(prompt=""):
    global write_to_parent_fd
    while True:
        s = input(prompt)
        if s == 'undo':
            os.write(write_to_parent_fd, b'\n')
            sys.exit()  # die to resume parent
        read_from_child_fd, write_fd = os.pipe()
        if os.fork():  # if this is the parent
            # blocking read to wait for child
            os.read(read_from_child_fd, 1)
        else:  # this is the child
            # store how to talk to parent
            write_to_parent_fd = write_fd
            return s


if __name__ == '__main__':
    console = code.InteractiveConsole()
    while True:
        src = read_line('>>> ')
        console.runsource(src)
