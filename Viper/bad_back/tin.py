import time
import tkinter as tk
from infi.systray import SysTrayIcon
import random
import os
import signal


class lolipop_Base(tk.Toplevel):
    """Popup Base Class"""
    inited = False  # tk root is bound to class and needs init

    def __init__(self):
        self.root_init()
        self.register_loli(self)
        super().__init__(master=self.root)
        self.attributes('-topmost', True) # on top and true for default children
        self.title("Pop me 🎈 OR ELSE ...")
        self.decide_position()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    @classmethod
    def register_loli(cls, loli):
        cls.lolis += [loli]

    @classmethod
    def root_init(cls):
        if cls.root_init:
            return None
        cls.root_init = True
        cls.root = tk.Tk()
        cls.root.withdraw()
        cls.root.protocol("WM_DELETE_WINDOW", lambda: None)
        cls.photo = tk.PhotoImage(file="./one_bad_day.png")
        cls.root.iconphoto(True, cls.photo)
        cls.lolis = []

    def on_close(self):
        self.lolis.remove(self)
        self.destroy()

    def decide_position(self):
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        width, height = 300, 0
        x, y = random.randrange(ws-width), random.randrange(hs-height)
        self.geometry(f'{width}x{height}+{x}+{y}')

    @staticmethod
    def full_break(*args):
        pid = os.getpid()
        if os.name == 'nt':
            os.system(f'taskkill -f /pid {pid}')
        else:
            os.kill(pid, signal.Signal.SIGKILL)

    menu_options = (("IT'S SAFE HERE, QUICK!!", None, full_break),)
    systray = SysTrayIcon("./ALARM.ico", "COME HERE!!", menu_options)

    @classmethod
    def start_gen(cls,count: int):
        for _ in range(count):
            cls()

    


class lolipop_v1(lolipop_Base):
    """Popup that populates itself if left unchecked"""
    maturation_time = 3000

    def __init__(self):
        super().__init__()
        self.after_id = self.after(self.maturation_time, self.new_window)

    def new_window(self):
        self._new_window()
        self.after_id = self.after(self.maturation_time, self.new_window)

    @classmethod
    def _new_window(cls):
        cls()

    def on_close(self):
        super().on_close()
        self.after_cancel(self.after_id)
        if not self.lolis:  # if closed the last one
            self.root.quit()
    
    @classmethod
    def main(cls):
        cls.start_gen(4)
        cls.root.mainloop()

class lolipop_v2(lolipop_Base):
    """Popup that is populated in generations"""

    @classmethod
    def root_init(cls):
        if cls.root_init:
            return None
        super().root_init()
        cls.root_text = tk.Text(cls.root, height=2, width=50)
        cls.root_text.pack()
        cls.root.eval('tk::PlaceWindow . center')
        cls.root.withdraw()

    @classmethod
    def main(cls):
        count = 2
        gen = 0
        while 1:
            gen += 1
            cls.start_gen(count*2)
            cls.root.after(
                3000, lambda: cls.root.quit())
            cls.root.mainloop()

            count = len(cls.lolis)
            for ind, l in enumerate(cls.lolis.copy()):
                l.on_close()
            cls.root.wm_deiconify()
            s = f"Generation {gen} survived with {count} lolis.\nNow they will multiply."
            cls.root_text.delete('1.0', tk.END)
            for c in s:
                cls.root_text.insert(tk.END, c)
                cls.root.update()
                time.sleep(0.035 + random.random()/50)
                if c == '\n':
                    time.sleep(1)
            time.sleep(2)
            cls.root.withdraw()



if __name__ == "__main__":
    # lolipop_v2.main()
    lolipop_v1.main()
