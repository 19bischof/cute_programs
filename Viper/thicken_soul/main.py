import os
from colored import fg,attr
y_names = ("top","center","bottom")
x_names = ("left","middle","right")

grid = [[0]*3 for x in range(3)]
p1_turn = True
pre = (fg('green')+"Player2, ",fg('red_3b')+"Player1, ")

def place_sign():
    global p1_turn
    stopping = False
    while not stopping:
        os.system("cls" if os.name == 'nt' else 'clear')
        inp = input(pre[int(p1_turn)]+"Where do you want to set it?\n").lower()
        for x_pos in x_names:
            if inp.find(x_pos) != -1:
                for y_pos in y_names:
                    if inp.find(y_pos) != -1:
                        if grid[y_names.index(y_pos)][x_names.index(x_pos)]:
                            continue
                        grid[y_names.index(y_pos)][x_names.index(x_pos)] = int(not p1_turn)+1
                        stopping = True
    p1_turn = not p1_turn

def finished():
    print(attr('reset'),end="",flush=True)
    #check for winner
    for i in range(3):
        if grid[i][0] == grid[i][1] == grid[i][2] and grid[i][0]:
            print(pre[int(grid[i][0])-1]+"won the game!"+attr('reset'))
            return True
        if grid[0][i] == grid[1][i] == grid[2][i] and grid[0][i]:
            print(pre[int(grid[0][i])-1]+"won the game!"+attr('reset'))
            return True
    if grid[0][0] == grid[1][1] == grid[2][2] and grid[0][0]:
        print(pre[int(grid[0][0])-1]+"won the game!"+attr('reset'))
        return True
    if grid[2][0] == grid[1][1] == grid[0][2] and grid[2][0]:
        print(pre[int(grid[2][0])-1]+"won the game!"+attr('reset'))
        return True
    #check if there can be a winner
    #example: if row not full and row has not one of each -> someone can win
    trans =  list(map(list,zip(*grid)))
    for i in range(3):
        if grid[i].count(0) != 0:
            if (grid[i].count(1),grid[i].count(2)) != (1,1):
                return False
        if trans[i].count(0) != 0:
            if (trans[i].count(1),trans[i].count(2)) != (1,1):
                return False
    diags = ((grid[0][0], grid[1][1], grid[2][2]),(grid[2][0], grid[1][1], grid[0][2]))
    for i in range(2):
        if diags[i].count(0) != 0:
            if (diags[i].count(1),diags[i].count(2)) != (1,1):
                return False
    print("No one wins!")
    return True

def print_grid():
    row_one = attr('underlined')+" {} | {} | {} ".format(*grid[0])+attr('reset')
    row_two = attr('underlined')+" {} | {} | {} ".format(*grid[1])+attr('reset')
    row_thr = attr('underlined')+" {} | {} | {} ".format(*grid[2])+attr('reset')    
    print("\t"+row_one,row_two,row_thr,sep='\n\t')

if __name__ == "__main__":
    while 1:
        place_sign()
        if finished():
            break
    print_grid()