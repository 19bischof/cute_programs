from _words import words
from pprint import pprint
import os
import random
import time
import colored
yellow = colored.fg("yellow")
green = colored.fg("green")
blue = colored.fg("blue")
red = colored.fg("red")
reset = colored.attr("reset")
width, height = 3,4
abc = "abcdefghijklmnopqrstuvwxyz"
dig = "123456789"
if width > 26 or height > 9 or (width*height) % 2:
    print(red+"These are inappropriate Values for this game"+reset)
    raise ValueError(width, height)
grid = [[None for _ in range(width)] for _ in range(height)]


def populate():
    global grid
    pool_of_pos = []
    pool_of_words = [words.pop(random.randrange(len(words)))
                     for i in range(width*height//2)]
    for row in range(height):
        for col in range(width):
            pool_of_pos.append((row, col))
    for word in pool_of_words:
        for _ in range(2):
            p = pool_of_pos.pop(random.randrange(len(pool_of_pos)))
            grid[p[0]][p[1]] = word


def game_loop():
    first_pick = ()
    words_already_found = []
    while True:
        if not first_pick:
            os.system('cls' if os.name == "nt" else "clear")
        inp = input(f"From (A-{chr(64+width)}) and (1-{height}): " + yellow).lower().strip()
        # doesnt contain at least one digit and character
        if not (any((first_c := c) in inp for c in abc) and any((first_d := d) in inp for d in dig)):
            print(red+"need digit and character"+reset)
            time.sleep(1)
            continue
        d_ind, c_ind = int(first_d)-1, abc.find(first_c)
        if not (0 <= d_ind <= height-1):
            print(red+"Bad digit"+reset)
            time.sleep(1)
            continue
        if not (0 <= c_ind <= width-1):
            print(red+"Bad letter"+reset)
            time.sleep(1)
            continue
        if (d_ind, c_ind) in words_already_found:
            print(red+"Already picked this point"+reset)
            time.sleep(1)
            continue
        if first_pick == (d_ind, c_ind):
            print(red+"Choose different points!"+reset)
            time.sleep(1)
            continue
        print(blue+grid[d_ind][c_ind]+reset)
        if not first_pick:
            first_pick = d_ind, c_ind
            continue
        if grid[first_pick[0]][first_pick[1]] == grid[d_ind][c_ind]:
            print(green+"Correct!"+reset)
            words_already_found.append(first_pick)
            words_already_found.append((d_ind, c_ind))
        first_pick = ()
        time.sleep(1)
        if len(words_already_found) == width * height:
            break
    print(green+"You made it!")


if __name__ == "__main__":
    populate()
    # pprint(grid)
    # input(yellow+"Press Enter to continue!"+reset)
    try:
        game_loop()
    except KeyboardInterrupt:
        print(reset)
