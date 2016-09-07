import code, os, sys

def read_line(prompt=""):
    while True:
        s = input(prompt)
        if s == 'undo':
            sys.exit()  # die to resume parent
        pid = os.fork()
        if pid == 0:  # if this is the child
            return s
        else:  # if this is the parent
            os.wait()

console = code.InteractiveConsole()
while True:
    src = read_line('>>> ')
    console.runsource(src)
