import code
import os
import sys


class ForkUndoConsole(code.InteractiveConsole):
    def __init__(self):
        code.InteractiveConsole.__init__(self)
        self.write_to_parent_fd = None
        self.read_from_child_fd = None
        self.has_parent = False

    def on_undo(self):
        # kill process, let parent continue in raw_input loop
        if self.has_parent:
            os.write(self.write_to_parent_fd, 'done\n')
        sys.exit()

    def on_exit(self):
        # kill process, tell parent die took
        if self.has_parent:
            os.write(self.write_to_parent_fd, 'exit\n')
        else:
            print  # print a newline when exiting top level
        sys.exit()

    def raw_input(self, prompt=""):
        while True:  # each time through this loop is another
            try:
                s = raw_input(prompt)
            except EOFError:
                self.on_exit()
            if s == 'undo':
                self.on_undo()
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

                # e is the first letter of 'exit\n'
                if from_child == 'e':
                    self.on_exit()

if __name__ == '__main__':
    console = ForkUndoConsole()
    # self.interact() does something like
    # while True:
    #     source = self.raw_input('>>> ')
    #     self.run_source(source)
    # but works with multiline input
    console.interact()
