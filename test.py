import code, os, sys

def read_line(prompt=""):
    while True:
        s = input(prompt)
        if s == 'undo':
            sys.exit()  # restore prev. state in parent
        if os.fork() == 0:  # this is the child
            return s
        else:  # this is the parent
            os.wait()  # wait for child process

console = code.InteractiveConsole()
while True:
    src = read_line('>>> ')
    console.runsource(src)
