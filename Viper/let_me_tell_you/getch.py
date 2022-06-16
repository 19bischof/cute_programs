# original: https://code.activestate.com/recipes/134892/
class Getch:
    """Gets a single character from terminal.  Does not echo to the
screen. Flushes while creating instance. Call the instance to get character.
Example at bottom"""
    def __init__(self,flush=True):
        try:
            self.impl = _GetchWindows(flush)
        except ImportError:
            self.impl = _GetchUnix(flush)
            
    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self,flush):
        import tty, sys,termios
        termios.tcflush(sys.stdin, termios.TCIOFLUSH) #to flush previous

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
    def __init__(self,flush):
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

if __name__ == "__main__":
    _getch = Getch() #init + flush
    while(inp:=_getch()): #get character
        if inp == b"\x03": #Ctrl+c
            quit()
        print(inp)