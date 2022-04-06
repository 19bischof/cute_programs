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
#the options and descriptions can be dynamically adjusted by starting the menu in a new thread and manipulating the given parameters
class i_menu:

    def __init__(self, options: list[list[str]] ,header: list[str]):
        assert len(options) == len(header)
        # cursor.hide()
        os.system('cls' if os.name == 'nt' else "clear")
        self.options = options
        self.desc = header
        self.cur_hover = 0
        self.cur_page = 0
        self.selected = [ None for _ in range(len(self.options))]
        self.getch = Getch()
        self.result = ""
        # cursor.show()

    def loop(self):
        self.show_menu()
        start_selected = self.selected.copy()
        while self.selected == start_selected:
            # time.sleep(0.01)
            ch = self.getch()
            if ch == b'\x03':
                # cursor.show()
                quit() 
            if ch == b'\x1b':
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
            if ch == b'\r':
                self.enter()
        self.show_menu()
        return self.selected                


    def enter(self):
        if self.selected[self.cur_page] == self.options[self.cur_page][self.cur_hover]:
            self.selected[self.cur_page] = None
            return
        self.selected[self.cur_page] = self.options[self.cur_page][self.cur_hover]

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
                self.cur_hover = len(self.options[self.cur_page]) -1
            self.show_menu()
    def right(self):
        if self.cur_page < len(self.options) - 1:
            self.cur_page += 1
            if self.cur_hover >= len(self.options[self.cur_page]):
                self.cur_hover = len(self.options[self.cur_page]) -1
            self.show_menu()

    def show_menu(self):
        width,height = os.get_terminal_size()
        for i in range(len(self.options[self.cur_page])+4):    
            print(up + " "*(width)+'\r', end="",flush=False)
        print(textwrap.shorten(self.desc[self.cur_page],width)) #print question
        for i in range(len(self.options[self.cur_page])):
            cur_text = self.options[self.cur_page][i]
            percent = self.distros[self.cur_page][cur_text]
            if not cur_text:
                cur_text = "<<No Value !>>"
            highlight = red
            active =  blue+attr('underlined') 
            pre = highlight if i == self.cur_hover else ""
            pre += active if cur_text == self.selected[self.cur_page] else ""
            pre += bg('dark_red_2') if cur_text == self.selected[self.cur_page] and i == self.cur_hover else ""
            print("- {0}{1} {2}{3}".format(pre, cur_text,green,percent) + attr('reset'))
        print(yellow,self.result,attr('reset'))



