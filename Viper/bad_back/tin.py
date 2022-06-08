import tkinter as tk
import random
from sys import getsizeof


class lolipop(tk.Toplevel):
    """Popup that populates itself if left unchecked"""
    count = 0
    root = tk.Tk()
    root.withdraw()
    photo = tk.PhotoImage(file="./one_bad_day.png")
    root.iconphoto(True, photo)

    def __init__(self):
        lolipop.count += 1
        super().__init__(lolipop.root)
        self.title("Pop me 🎈 OR ELSE ...")
        self.decide_position()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.attributes('-topmost', True) # so it can't be hidden
        self.after(2000, self.new_window)

    def new_window(self):
        lolipop()
        self.after(3000, self.new_window)

    def on_close(self):
        lolipop.count -= 1
        if lolipop.count == 0:
            lolipop.root.quit()
        self.destroy()

    def decide_position(self):
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        width, height = 300, 0
        x, y = random.randrange(ws-width), random.randrange(hs-height)
        self.geometry(f'{width}x{height}+{x}+{y}')


def main():
    lolipop()
    lolipop.root.mainloop()


if __name__ == "__main__":
    main()
