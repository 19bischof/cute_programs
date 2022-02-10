import os
from colored import fg, attr
import random
import time
import logging

logging.basicConfig(
    filename="c.log",
    encoding="utf-8",
    format="%(asctime)s:%(levelname)s\t%(message)s",
    filemode="a",
    level=logging.DEBUG,
)
y_names = ("top", "center", "bottom")
x_names = ("left", "middle", "right")

grid = [[0] * 3 for x in range(3)]  # 0:empty, 1:player1, 2:player2
history = []
p_index = random.randrange(2)  # 0 is player1, 1 is player2
p_colors = (fg("chartreuse_3a"),fg("red_3b"))
pre = (p_colors[0] + "Player1", p_colors[1] + "Player2")


def input_place_sign():
    global p_index
    stopping = False
    logging.info("Player{} is choosing with input".format(p_index + 1))
    while not stopping:
        os.system("cls" if os.name == "nt" else "clear")
        try:
            logging.info("getting input from user")
            inp = (
                input(pre[p_index] + ", Where do you want to set it?\n").lower().strip()
            )
        except KeyboardInterrupt:
            logging.warning("stopped with KeyboardInterrupt")
            print_grid()
            quit()
        if inp in ("?", "help"):
            logging.debug("calling help function")
            print_help()
            input("Press Enter to continue!")
            continue
        logging.debug("raw input is " + inp)
        for x_pos in x_names:
            if inp.find(x_pos) != -1:
                logging.debug("found x position in input: " + x_pos)
                for y_pos in y_names:
                    if inp.find(y_pos) != -1:
                        logging.debug("found y position in input: " + y_pos)
                        if grid[y_names.index(y_pos)][x_names.index(x_pos)]:
                            logging.debug(
                                "chosen position already taken "
                                + repr((y_names.index(y_pos), x_names.index(x_pos)))
                            )
                            continue
                        grid[y_names.index(y_pos)][x_names.index(x_pos)] = p_index + 1
                        history.append((y_names.index(y_pos), x_names.index(x_pos)))
                        logging.info(
                            "input set sign at ->{}<-".format(
                                repr((y_names.index(y_pos), x_names.index(x_pos)))
                            )
                        )
                        stopping = True
    p_index = (p_index + 1) % 2


def finished():
    logging.debug("check for winner")
    print(attr("reset"), end="", flush=True)
    # check for winner
    for i in range(3):
        if grid[i][0] == grid[i][1] == grid[i][2] and grid[i][0]:
            print(pre[grid[i][0] - 1] + " won the game!" + attr("reset"))
            logging.info("Player{} won".format(grid[i][0]))
            return True
        if grid[0][i] == grid[1][i] == grid[2][i] and grid[0][i]:
            print(pre[grid[0][i] - 1] + " won the game!" + attr("reset"))
            logging.info("Player{} won".format(grid[0][i]))
            return True
    if grid[0][0] == grid[1][1] == grid[2][2] and grid[0][0]:
        print(pre[grid[0][0] - 1] + " won the game!" + attr("reset"))
        logging.info("Player{} won".format(grid[0][0]))
        return True
    if grid[2][0] == grid[1][1] == grid[0][2] and grid[2][0]:
        print(pre[grid[2][0] - 1] + " won the game!" + attr("reset"))
        logging.info("Player{} won".format(grid[2][0]))
        return True
    logging.debug("check for possibility to win")
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
    logging.info("no possibility to win")
    return True

def clear_screen():
    up = '\033[A'
    for i in range(5):
        print(up+" "*50,end="\r",flush=True)

def func_place_sign(c: tuple[int]):  # c[0] is y; c[1] is x
    global p_index
    clear_screen()
    if grid[c[0]][c[1]]:
        logging.error("Coordinates {} already taken".format(c))
        raise ValueError
    grid[c[0]][c[1]] = p_index + 1
    history.append((c[0], c[1]))
    print(pre[p_index] + " sets it at {} {}".format(y_names[c[0]], x_names[c[1]]))
    logging.info("function set sign at ->{}<-".format(repr(c)))
    p_index = (p_index + 1) % 2


def bot1_angela():
    # function: make random move
    logging.info("Player{} is choosing with bot1_angela".format(p_index + 1))
    while True:
        c = (random.randrange(3), random.randrange(3))
        if not grid[c[0]][c[1]]:
            break
    func_place_sign(c)


def bot2_amelie():
    # function: make mirrored move if possible
    logging.info("Player{} is choosing with bot2_amelie".format(p_index + 1))
    calc = {0: 2, 1: 0, 2: -2}
    try:
        y, x = history[-1]
        if grid[y][x]:
            mir_y, mir_x = y + calc[y], x + calc[x]
            if not grid[mir_y][mir_x]:
                func_place_sign((mir_y, mir_x))
                return
            logging.debug("spot already taken " + repr((mir_y, mir_x)))
    except IndexError:
        pass
    logging.debug("unable to find a move")
    bot1_angela()


def bot3_aurora():
    # function: make move in corners and middle to form multiple lines at once
    logging.info("Player{} is choosing with bot3_aurora".format(p_index + 1))
    corners = ((0, 0), (2, 0), (2, 2), (0, 2))
    if not grid[1][1]:
        func_place_sign((1, 1))
        return
    best_corner_score = 0
    best_corner = None
    for c in corners:
        if grid[c[0]][c[1]]:
            continue
        h_line = [(c[0], x) for x in range(3)]
        v_line = [(y, c[1]) for y in range(3)]
        d_line = [((0, 0), (1, 1), (2, 2)), ((2, 0), (1, 1), (0, 2))]
        if c in d_line[0]:
            d_line = d_line[0]
        else:
            d_line = d_line[1]
        corner_score = 0
        for line in (h_line, v_line, d_line):
            line_score = 0
            impossible = False
            for l in line:
                val = grid[l[0]][l[1]]
                if val == p_index + 1:
                    line_score += 1
                elif val == int(not p_index) + 1:
                    impossible = True
            if impossible: line_score = -1
            corner_score += line_score
        if corner_score > best_corner_score:
            logging.debug("corner_score updated to {}".format(corner_score))
            best_corner = c
            best_corner_score = corner_score
    if best_corner:
        func_place_sign(best_corner)
        return
    shuffled = list(corners)
    random.shuffle(shuffled)
    for y,x in shuffled:
        if not grid[y][x]:
            func_place_sign((y,x))
            return
    logging.debug("unable to find a move")
    bot2_amelie()


def bot4_anasthasia():
    # function: when one move from winning or losing make that one move
    logging.info("Player{} is choosing with bot4_anasthasia".format(p_index + 1))
    transp_grid = list(map(list, zip(*grid)))
    diags_index = (((0, 0), (1, 1), (2, 2)), ((2, 0), (1, 1), (0, 2)))
    # see if you are one away from winning
    for g in (grid, transp_grid):
        for y in range(3):
            if g[y].count(p_index + 1) == 2 and g[y].count(0) == 1:
                logging.debug("found winning move!")
                for x in range(3):
                    if not g[y][x]:
                        if g == transp_grid:
                            func_place_sign((x, y))
                        else:
                            func_place_sign((y, x))
                        return
    for d in diags_index:
        line = [grid[y][x] for y, x in d]
        if line.count(p_index + 1) == 2 and line.count(0) == 1:
            logging.debug("found winning move!")
            for y, x in d:
                if not grid[y][x]:
                    func_place_sign((y, x))
                    return

    # see if enemy is one from winning:
    next_p_index = int(not p_index)
    for g in (grid, transp_grid):
        for y in range(3):
            if g[y].count(next_p_index + 1) == 2 and g[y].count(0) == 1:
                logging.debug("found enemy's winning move!")
                for x in range(3):
                    if not g[y][x]:
                        if g == transp_grid:
                            func_place_sign((x, y))
                        else:
                            func_place_sign((y, x))
                        return
    for d in diags_index:
        line = [grid[y][x] for y, x in d]
        if line.count(next_p_index + 1) == 2 and line.count(0) == 1:
            logging.debug("found enemy's winning move!")
            for y, x in d:
                if not grid[y][x]:
                    func_place_sign((y, x))
                    return
    logging.debug("unable to find a move")
    bot3_aurora()


def bot5_ashley():
    # function: move on pattern
    logging.info("Player{} is choosing with bot5_ashley".format(p_index + 1))
    corners = ((0, 0), (2, 0), (2, 2), (0, 2))
    edges = ((0, 1), (1, 0), (2, 1), (1, 2))
    for c in corners:
        if history == [c]:
            func_place_sign((1, 1))
            return

    for i, c in enumerate(corners):
        if history == [c, (1, 1), corners[i - 2]]:
            func_place_sign(random.choice(edges))
            return
    logging.debug("unable to find a move")
    bot4_anasthasia()


def print_grid():
    gar = grid[0].copy() + grid[1].copy() + grid[2].copy()
    clrs = [p_colors[x-1] if x != 0 else "" for x in gar]
    re_u = attr('reset') + attr('underlined')
    # input(repr(clrs))
    row_one = attr("underlined") + " {p1}{}{r} | {p2}{}{r} | {p3}{}{r} ".format(*grid[0],p1=clrs[0],p2=clrs[1],p3=clrs[2],r=re_u) + attr("reset")
    row_two = attr("underlined") + " {p1}{}{r} | {p2}{}{r} | {p3}{}{r} ".format(*grid[1],p1=clrs[3],p2=clrs[4],p3=clrs[5],r=re_u) + attr("reset")
    row_thr = " {p1}{}{r} | {p2}{}{r} | {p3}{}{r} ".format(*grid[2],p1=clrs[6],p2=clrs[7],p3=clrs[8],r=attr('reset'))
    print(attr("reset") + "\t" + row_one, row_two, row_thr, sep="\n\t")


def print_help():
    h = """You choose the position by using the following matrix:
    top     
    center  
    bottom
            left middle right"""
    print(attr("reset") + h)


if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    logging.info("Running in __main__")
    player_methods = {0: input_place_sign, 1: bot5_ashley, 2:bot3_aurora,3:bot1_angela}  # even is player1, odd is player2
    logging.debug("player methods are " + repr(player_methods))
    logging.debug("starting Game Loop")
    i = p_index
    while 1:
        player_methods[i]()
        if finished():
            logging.debug("Break out of Game Loop")
            break
        if input_place_sign not in player_methods.values():
            print_grid()
        if player_methods[i] != input_place_sign:
            time.sleep(1)
        i = (i+1) % len(player_methods)
    print_grid()

# ideas for writing a tic bot:
# -instead of choosing cells, choosing lines seems better
# -when opponent one away from winning stop it
# -start from either corner or middle
# -make program react by mirroring
# -program patterns like: if opponent starts from corner choose opposing corner
