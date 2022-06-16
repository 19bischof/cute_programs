from ast import Index
import os
from colored import fg, bg, attr
import time
from getch import Getch
# import cursor
import textwrap
up = '\033[A'
green = fg('green')
yellow = fg('yellow')
blue = fg('cyan')
red = bg('red_3a')
# the options and descriptions can be dynamically adjusted by starting the menu in a new thread and manipulating the given parameters


class i_menu:

    def __init__(self, first_page, callback_page):
        # cursor.hide()
        os.system('cls' if os.name == 'nt' else "clear")
        self.options, self.descriptions, self.urls = [], [], []
        self.options.append(first_page["options"])
        self.descriptions.append(first_page["descriptions"])
        self.urls.append(first_page["urls"])
        self.cb_page = callback_page
        self.entered = False
        self.cur_hover = 0
        self.cur_page = 0
        self.selected = [None for _ in range(len(self.options))]
        self.getch = Getch()  # init getch
        self.result = ""
        self.last_height = 0
        # cursor.show()

    def loop(self):
        self.show_menu()
        start_selected = self.selected.copy()
        while not self.entered:
            # time.sleep(0.01)
            ch = self.getch()
            if ch == b'\x03':
                # cursor.show()
                quit()
            elif ch == b'\x1b':
                if self.getch() == b'[':
                    match self.getch():
                        case b'A': self.up()
                        case b'B': self.down()
                        case b'C': self.right()
                        case b'D': self.left()
            elif ch == b'\x00' or ch == b'\xe0':
                match self.getch():
                    case b'H': self.up()
                    case b'P': self.down()
                    case b'M': self.right()
                    case b'K': self.left()
            elif ch == b'\r':
                self.enter()
        self.show_menu()
        return self.urls[self.cur_page][self.cur_hover]

    def enter(self):
        if self.selected[self.cur_page] == self.options[self.cur_page][self.cur_hover]:
            self.selected[self.cur_page] = None
            return
        self.selected[self.cur_page] = self.options[self.cur_page][self.cur_hover]
        self.entered = True

    def up(self):
        if self.cur_hover > 0:
            self.cur_hover -= 1
            self.show_menu()

    def down(self):
        if self.cur_hover < len(self.options[self.cur_page]) - 1:
            self.cur_hover += 1
            self.show_menu()

    def left(self):
        if self.cur_page > 0:
            self.cur_page -= 1
            if self.cur_hover >= len(self.options[self.cur_page]):
                self.cur_hover = len(self.options[self.cur_page]) - 1
            self.show_menu()

    def right(self):
        self.cur_page += 1
        try:
            if self.cur_hover >= len(self.options[self.cur_page]):
                self.cur_hover = len(self.options[self.cur_page]) - 1
        except IndexError: 
            self.options.append([])
            self.descriptions.append([])
            self.urls.append([])
            self.selected.append(None)
        self.show_menu()

    def update_page(self):
        res = self.cb_page()
        for key in ("options", "descriptions", "urls"):
            getattr(self, key)[self.cur_page] = res[key]

    def show_menu(self):
        width, height = os.get_terminal_size()
        for i in range(self.last_height):  # clear last screen
            print(up + " "*(width)+'\r', end="", flush=False)
        self.last_height = 1
        if not self.options[self.cur_page]:
            self.update_page()
            os.system('cls' if os.name == 'nt' else "clear")
        # incrementing by height of print output
        for i,opt in enumerate(self.options[self.cur_page]):
            highlight = red
            active = blue+attr('underlined')
            pre = highlight if i == self.cur_hover else ""
            pre += active if opt == self.selected[self.cur_page] else ""
            pre += bg(
                'dark_red_2') if opt == self.selected[self.cur_page] and i == self.cur_hover else ""
            out = "- {0}{1} {2}".format(pre, opt, green) + attr('reset')
            if i == self.cur_hover:
                out += "\n"+blue+str(self.descriptions[self.cur_page][i])+attr('reset')
            self.last_height += len(textwrap.wrap(out,width))
            print(out)
