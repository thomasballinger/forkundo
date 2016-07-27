import code
import os
import sys


def readline(prompt):
    """Get input from user then fork or exit

    readline needs function attributes:
    .on_close() which should notify parent process we're undoing
    .on_exit() which should notify parent that we're exiting"""

    while True:
        try:
            s = raw_input(prompt)
        except EOFError:
            readline.on_exit()
        if s == 'undo':
            readline.on_undo()
        read_fd, write_fd = os.pipe()
        pid = os.fork()
        is_child = pid == 0

        if is_child:

            def on_undo():
                os.write(write_fd, 'done\n')
                sys.exit()

            def on_exit():
                os.write(write_fd, 'exit\n')
                sys.exit()

            readline.on_undo = on_undo
            readline.on_exit = on_exit

            return s
        else:
            from_child = os.read(read_fd, 1)
            if from_child == 'e':
                readline.on_exit()
            continue

readline.on_undo = sys.exit
readline.on_exit = sys.exit


class ForkUndoConsole(code.InteractiveConsole):
    def raw_input(self, prompt=""):
        return readline(prompt)


console = ForkUndoConsole()
console.interact()
