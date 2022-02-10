import os
from colored import fg, attr
import random
import time

# import logging # TODO: implement logger for bots in a ?smart? way
y_names = ("top", "center", "bottom")
x_names = ("left", "middle", "right")

grid = [[0] * 3 for x in range(3)]  # 0:empty, 1:player1, 2:player2
p_index = random.randrange(2)  # 0 is player1, 1 is player2
pre = (fg("chartreuse_3a") + "Player1, ", fg("red_3b") + "Player2, ")


def input_place_sign():
    global p_index
    stopping = False
    while not stopping:
        os.system("cls" if os.name == "nt" else "clear")
        try:
            inp = input(pre[p_index] + "Where do you want to set it?\n").lower().strip()
        except KeyboardInterrupt:
            print_grid()
            quit()
        if inp in ("?", "help"):
            print_help()
            input("Press Enter to continue!")
        for x_pos in x_names:
            if inp.find(x_pos) != -1:
                for y_pos in y_names:
                    if inp.find(y_pos) != -1:
                        if grid[y_names.index(y_pos)][x_names.index(x_pos)]:
                            continue
                        grid[y_names.index(y_pos)][x_names.index(x_pos)] = p_index + 1
                        stopping = True
    p_index += 1
    p_index %= 2


def finished():
    print(attr("reset"), end="", flush=True)
    # check for winner
    for i in range(3):
        if grid[i][0] == grid[i][1] == grid[i][2] and grid[i][0]:
            print(pre[grid[i][0] - 1] + "won the game!" + attr("reset"))
            return True
        if grid[0][i] == grid[1][i] == grid[2][i] and grid[0][i]:
            print(pre[grid[0][i] - 1] + "won the game!" + attr("reset"))
            return True
    if grid[0][0] == grid[1][1] == grid[2][2] and grid[0][0]:
        print(pre[grid[0][0] - 1] + "won the game!" + attr("reset"))
        return True
    if grid[2][0] == grid[1][1] == grid[0][2] and grid[2][0]:
        print(pre[grid[2][0] - 1] + "won the game!" + attr("reset"))
        return True
    # check if there can be a winner
    # example: if row not full and row has not one of each -> someone can win
    trans = list(map(list, zip(*grid)))
    for i in range(3):
        if grid[i].count(0) != 0:
            if (grid[i].count(1), grid[i].count(2)) != (1, 1):
                return False
        if trans[i].count(0) != 0:
            if (trans[i].count(1), trans[i].count(2)) != (1, 1):
                return False
    diags = ((grid[0][0], grid[1][1], grid[2][2]), (grid[2][0], grid[1][1], grid[0][2]))
    for i in range(2):
        if diags[i].count(0) != 0:
            if (diags[i].count(1), diags[i].count(2)) != (1, 1):
                return False
    print("No one wins!")
    return True


def api_place_sign(c: tuple[int]):  # c[0] is y; c[1] is x
    global p_index
    if grid[c[0]][c[1]]:
        print("Coordinates already taken!")
        raise ValueError
    grid[c[0]][c[1]] = p_index + 1
    print(pre[p_index] + "sets it at {} {}".format(y_names[c[0]], x_names[c[1]]))
    time.sleep(1)
    p_index += 1
    p_index %= 2


def bot1_angela():
    import random

    while True:
        c = (random.randrange(3), random.randrange(3))
        if not grid[c[0]][c[1]]:
            break
    api_place_sign(c)


def print_grid():
    row_one = attr("underlined") + " {} | {} | {} ".format(*grid[0]) + attr("reset")
    row_two = attr("underlined") + " {} | {} | {} ".format(*grid[1]) + attr("reset")
    row_thr = " {} | {} | {} ".format(*grid[2])
    print(attr("reset") + "\t" + row_one, row_two, row_thr, sep="\n\t")


def print_help():
    h = """You choose the position by using the following matrix:
    top     
    center  
    bottom
            left middle right"""
    print(attr("reset") + h)


if __name__ == "__main__":
    player_methods = {0: input_place_sign, 1: bot1_angela}
    while 1:
        player_methods[p_index]()
        if finished():
            break
    print_grid()
