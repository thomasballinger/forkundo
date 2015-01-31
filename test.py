import code
import os
import sys

# read about copy-on-write for Python processes - I feel like I've heard
# this doesn't work well

# read this about named pipes
# http://www.python-course.eu/pipes.php
#
#
# when things fork off, 
#


def print_to_terminal(msg):
    sys.stderr.write(str(os.getpid())+': ' + str(msg) + '\n')
    sys.stderr.flush()


def readline():
    """Get input from user, fork or exit

    on_close should notify parent process we're undoing"""

    print_to_terminal('pid %r initial call to readline' % (os.getpid()))
    while True:
        s = raw_input('>>> ')
        if s == 'undo':
            readline.on_undo()
        read_fd, write_fd = os.pipe()
        pid = os.fork()
        is_child = pid == 0
        print_to_terminal('created read/write fd pair: %r %r' % (read_fd, write_fd))


        if is_child:

            def on_undo():

                print_to_terminal('writing line to say done on fd %r' % (on_undo.write_fd,))
                os.write(on_undo.write_fd, 'done\n')
                print_to_terminal('wrote, exiting')
                sys.exit()

            readline.on_undo = on_undo
            readline.on_undo.write_fd = write_fd

            print_to_terminal('child returning to loop')
            return s
        else:
            print_to_terminal('Waiting for child %r by reading on fd %r' % (pid, read_fd))
            from_child = os.read(read_fd, 1)
            print_to_terminal('parent %r received response from child %r: %r' % (os.getpid(), pid, from_child))
            continue

interp = code.InteractiveInterpreter()
while True:
    source = readline()
    interp.runsource(source)
