import win32gui
import time
class win_focus:
    def __init__(self,name):
        self.name = name
        
    def focus(self,delay=0):
        time.sleep(delay)
        toplist = []
        winlist = []
        def enum_callback(hwnd, results):
            winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

        win32gui.EnumWindows(enum_callback, toplist)
        windows = [hwnd for hwnd, title in winlist if self.name.lower() in title.lower()]
        if not windows:
            raise Exception("Window couldn't be found")
            
        win32gui.SetForegroundWindow(windows[0])

if __name__ == "__main__":
    import time
    w = win_focus("Visual Studio Code")
    time.sleep(3)
    w.focus()