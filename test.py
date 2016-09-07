import code
import os
import sys

write_to_parent_fd = None
read_from_child_fd = None

def read_line(prompt=""):
    global write_to_parent_fd
    global read_from_child_fd
    while True:  # each time through this loop is another
        s = input(prompt)
        if s == 'undo':
            os.write(write_to_parent_fd, b'done\n')
            sys.exit()
        read_fd, write_fd = os.pipe()
        if os.fork():  # this is the parent
            read_from_child_fd = read_fd
            os.read(read_from_child_fd, 1)
        else:  # this is the parent
            write_to_parent_fd = write_fd
            return s


if __name__ == '__main__':
    console = code.InteractiveConsole()
    while True:
        src = read_line('>>> ')
        console.runsource(src)
