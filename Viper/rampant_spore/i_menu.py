import os
from colored import fg, bg, attr
import time
from getch import Getch
import cursor
import textwrap
textwrap.shorten
up = '\033[A'

#the options and descriptions can be dynamically adjusted by starting the menu in a new thread and manipulating the given parameters
class i_menu:
    selected = 0
    choices = []

    def __init__(self, options: list[str] ,desc: list[str]=None,get_index=False):
        if desc is not None:
            if len(options) != len(desc):
                print("descr has to be the same length as options!")
                raise ValueError
        cursor.hide()
        os.system('cls' if os.name == 'nt' else 'clear')
        self.options = options
        self.desc = desc
        self.choice = None
        self.selected = 0
        self.getch = Getch()

        self.get_index = get_index
        self.show_menu()
        self.loop()
        cursor.show()

    def __call__(self):
        if self.get_index:
            return self.choice
        return self.options[self.choice]
    
    def __str__(self):
        if self.get_index:
            return self.choice
        return self.options[self.choice]

    # # def add_option(self, option, ind=None):
    #     if ind is None:
    #         self.option.append(option)
    #     else:
    #         self.option.insert(ind, option)
    #     self.show_menu()
    def loop(self):
        while self.choice is None:
            
            # time.sleep(0.01)
            ch = self.getch()
            if ch == b'\x03':
                cursor.show()
                quit() 
            if ch == b'\x00' or ch == b'\xe0':
                ch = self.getch()
                if ch == b'P':
                    self.down()
                if ch == b'H':
                    self.up()
            if ch == b'\r':
                self.enter()
                print(self.choice)


    def enter(self):
        self.choice = self.selected

    def up(self):
        if self.selected != 0:
            self.selected -= 1
        self.show_menu()

    def down(self):
        if self.selected != len(self.options) - 1:
            self.selected += 1
        self.show_menu()

    def show_menu(self):
        width,height = os.get_terminal_size()
        for i in range(len(self.options)+1):    #+1 for the description
            print(up+" "*(width-1)+'\r', end="")
        for i in range(len(self.options)):
            highlight = fg('white') + bg('deep_pink_4c')+ attr('underlined')
            pre = highlight if i == self.selected else ""
            print("{0}{1}".format(pre, self.options[i]) + attr('reset'))
            if i == self.selected and self.desc[i]:
                print(fg('green')+textwrap.shorten(self.desc[i],width)+attr('reset'))


if __name__ == "__main__":
    opts = ("first", "second", "third", "fourth")
    desc = ("erste "*100,"zweite "*20,"dritte "*5,"vierte "*60)
    choice = i_menu(opts,desc=desc,get_index=True)()
    print(choice)
    


