import code
import os
import sys


if sys.version_info[0] == 2:
    input = raw_input


class ForkUndoConsole(code.InteractiveConsole):
    def __init__(self):
        code.InteractiveConsole.__init__(self)
        self.write_to_parent_fd = None
        self.read_from_child_fd = None
        self.has_parent = False

    def die_and_tell_parent(self, msg):
        if self.has_parent:
            os.write(self.write_to_parent_fd, msg+b'\n')
        elif msg == 'exit':
            print  # write a newline on top level exit
        sys.exit()

    def raw_input(self, prompt=""):
        while True:  # each time through this loop is another
            try:
                s = input(prompt)
            except EOFError:
                self.die_and_tell_parent(b'exit')
            if s == 'undo':
                self.die_and_tell_parent(b'done')
            read_fd, write_fd = os.pipe()
            pid = os.fork()
            is_child = pid == 0

            if is_child:
                self.has_parent = True
                self.write_to_parent_fd = write_fd
                return s
            else:
                self.read_from_child_fd = read_fd

                # blocking read to wait for child to die
                from_child = os.read(self.read_from_child_fd, 1)

                # e is the first letter of 'exit'
                if from_child == 'e':
                    # propogate that message up
                    self.die_and_tell_parent(b'exit')


if __name__ == '__main__':
    print('parent pid:', os.getpid())
    console = ForkUndoConsole()
    # console.interact() does something like
    # while True:
    #     source = self.raw_input('>>> ')
    #     self.run_source(source)
    # but works with multiline input
    console.interact()
