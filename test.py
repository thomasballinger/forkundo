import code
import os
import sys

# read about copy-on-write for Python processes - I feel like I've heard
# this doesn't work well

DEBUG = False

print 'running with pid %r' % (os.getpid(),)


def print_to_terminal(msg):
    if DEBUG:
        sys.stderr.write(str(os.getpid())+': ' + str(msg) + '\n')
        sys.stderr.flush()


def readline(prompt):
    """Get input from user, fork or exit

    readline needs function attributes:
    .on_close() should notify parent process we're undoing
    .on_exit() should notify parent that we're exiting"""

    print_to_terminal('pid %r initial call to readline' % (os.getpid()))
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
        print_to_terminal('created read/write fd pair: %r %r' % (read_fd, write_fd))

        if is_child:

            def on_undo():
                print_to_terminal('undoing command')
                print_to_terminal('writing line to say done on fd %r' % (write_fd,))
                os.write(write_fd, 'done\n')
                print_to_terminal('wrote, exiting')
                sys.exit()

            def on_exit():
                print_to_terminal('exiting!')
                os.write(write_fd, 'exit\n')
                sys.exit()

            readline.on_undo = on_undo
            readline.on_exit = on_exit

            print_to_terminal('child returning to loop')
            return s
        else:
            print_to_terminal('Waiting for child %r by reading on fd %r' % (pid, read_fd))
            from_child = os.read(read_fd, 1)
            if from_child == 'e':
                readline.on_exit()
            print_to_terminal('parent %r received response from child %r: %r' % (os.getpid(), pid, from_child))
            continue

readline.on_undo = sys.exit
readline.on_exit = sys.exit

class ForkUndoConsole(code.InteractiveConsole):
    def raw_input(self, prompt=""):
        """Write a prompt and read a line.

        The returned line does not include the trailing newline.
        When the user enters the EOF key sequence, EOFError is raised.

        The base implementation uses the built-in function
        raw_input(); a subclass may replace this with a different
        implementation.

        """
        return readline(prompt)


console = ForkUndoConsole()
console.interact()
