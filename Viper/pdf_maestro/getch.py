# original: https://code.activestate.com/recipes/134892/
class Getch:
    """Gets a single character from terminal.  Does not echo to the
screen. Call the instance to get character.
Example at bottom"""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()
            
    def __call__(self): return self.impl()


class _GetchUnix:
    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch.encode("utf-8")


class _GetchWindows:
    def __init__(self):
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

def get_input(request):
    print(request)
    _getch = Getch() #init 
    inputs = []
    while(inp:=_getch()): #get character
        inp = inp.decode()
        print(inp,end="",flush=True)
        if inp == "\x03": #Ctrl+c
            raise KeyboardInterrupt
        if inp == '\r':
            break
        inputs.append(inp)
    return "".join(inputs)

if __name__ == "__main__":
    _getch = Getch() #init 
    while(inp:=_getch()): #get character
        if inp == b"\x03": #Ctrl+c
            raise KeyboardInterrupt
        print(inp)