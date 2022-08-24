import random
import os
W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purple
C  = '\033[36m' # cyan


length = 20
height = 20
grid = list()
points_grid = list()
clicked_grid = list()
percentage_of_bombs = 0.1
bombs = int(height*length*percentage_of_bombs)
pot = bombs*[1]+int((height*length)-bombs)*[0]
def set_bombs():    
    global length, height,pot
    for i in range(height):
        line = list()
        for j in range(length):
            choice = random.choice(pot)
            line.append(choice)
            pot.remove(choice)
        grid.append(line)

def initialize_grid(this_grid):
    for i in range (height):
            line = list()
            for j in range (length):
                line.append(0)
            this_grid.append(line)

def print_open_grid(the_grid):
    for i in range (height):
        for j in range (length):
            if(j is length-1):                
                print(the_grid[i][j])
                break
            print(the_grid[i][j],'| ',end="")
    print()
          
def print_exploding_grid():            
    for i in range (height):
            for j in range (length):
                if(j is length-1):
                    if grid[i][j] == 0:                
                        print(B+str(points_grid[i][j])+W)
                    else:
                        print(R+"X"+W)
                    break
                if grid[i][j] == 0:                
                    print(B+str(points_grid[i][j]),'| '+W,end="")

                else:
                    print(R+"X",B+'| '+W,end="")

    print()


def print_game_grid():
    global row

    for i in range (height):
        for j in range (length):
            if(j is length-1):
                if clicked_grid[i][j] == 1:
                    print(C+str(points_grid[i][j])+W)
                else:
                    
                    if clicked_grid[i][j]==0 :
                        if i == row:
                            print(O+'X'+W)
                        else:
                            print(R+'X'+W)
                
                    if clicked_grid[i][j]==2:
                        print(G+'?'+W)
                break
            if clicked_grid[i][j] == 1:
                print(C+str(points_grid[i][j]),'| '+W,end="")
            else:
                if clicked_grid[i][j]==0:

                    if i == row:
                        print(O+'X | '+W,end="")
                    else:
                        print(R+'X | '+W,end="")
                
                if clicked_grid[i][j]==2:
                        print(G+'?',R+'| '+W,end="")
    print()
               



def get_coord():
    global row
    mode = input("mark a bomb or test a cell ?(0/1)\n")
    if mode == "quit":
        quit()
    mode = int(mode)
    row = input("which row ?\n")
    if row == "quit":
        quit()
    row = int(row)
    print_game_grid()    
    column  = input("which column ?\n")
    if column== "quit":
        quit()
    column = int(column)
    return mode,row,column


def reveal_neighbours(row,column):
    if row<height-1:
            if clicked_grid[row+1][column] ==0:
                clicked_grid[row+1][column] =1
                if points_grid[row+1][column] == 0:
                    reveal_neighbours(row+1,column)
    if row>0:            
            if clicked_grid[row-1][column] ==0:
                clicked_grid[row-1][column] =1
                if points_grid[row-1][column] == 0:
                    reveal_neighbours(row-1,column)
    if column >0:
        if clicked_grid[row][column-1] ==0:
            clicked_grid[row][column -1] =1
            if points_grid[row][column-1] == 0:
                    reveal_neighbours(row,column-1)
        if row>0:
            if clicked_grid[row-1][column-1] ==0:
                clicked_grid[row-1][column-1] =1
                if points_grid[row-1][column-1] == 0:
                    reveal_neighbours(row-1,column-1)
        if row<height-1:
            if clicked_grid[row+1][column-1] ==0:
                clicked_grid[row+1][column-1] =1
                if points_grid[row+1][column-1] == 0:
                    reveal_neighbours(row+1,column-1)
    if column <length-1:
        if clicked_grid[row][column+1] ==0:
            clicked_grid[row][column +1] =1
            if points_grid[row][column+1] == 0:
                    reveal_neighbours(row,column+1)
        if row>0:
            if clicked_grid[row-1][column+1] ==0:
                clicked_grid[row-1][column+1] =1
                if points_grid[row-1][column+1] == 0:
                    reveal_neighbours(row-1,column+1)
        if row<height-1:
            if clicked_grid[row+1][column+1] ==0:
                clicked_grid[row+1][column+1] =1
                if points_grid[row+1][column+1] == 0:
                    reveal_neighbours(row+1,column+1)



def start_game():
    global mode,row,column
    real_bombs = bombs              #for winning condition
    number_of_tiles_open = 0
    number_of_marks = 0
    os.system("")
    print("Game is starting...\nIf you want to exit the game enter quit")
    while(True):
        mode=row=column = -1
        print_game_grid()
        print("bombs:",bombs-number_of_marks)
        mode,row,column = get_coord()
        if mode == 1:
            if grid[row][column]==1:
                print("explosion!")
                print_exploding_grid()
                print("GAME OVER")
                exit()
            if clicked_grid[row][column] == 0:
                clicked_grid[row][column] = 1
                number_of_tiles_open += 1
                if points_grid[row][column] == 0:
                    reveal_neighbours(row,column)
            else:
                if clicked_grid[row][column] == 2:
                    print("This cell is marked!")
                if clicked_grid[row][column] == 1:
                    print("This cell is already open!")   
            
         
        if mode == 0:
            if clicked_grid[row][column] == 0:
                clicked_grid[row][column] = 2
                number_of_marks+=1
                if grid[row][column] == 1:
                    real_bombs-=1
            else:
                if clicked_grid[row][column] == 2:
                    clicked_grid[row][column] = 0
                    number_of_marks-=1
                    if grid[row][column] == 1:
                        real_bombs+=1

                else:
                    if clicked_grid[row][column] == 1:
                        print("This cell is already open!")
        if number_of_tiles_open == height*length-bombs or real_bombs == 0:
            print("\nCONGRATULATIONS\nYou've won the game!")
            quit()
            

def calc_points_of_cell():
    global points_grid
    
    for index,line in enumerate(grid):
        for iindex,cell in enumerate(line):
            if cell  == 1:
                if index<height-1:
                        points_grid[index+1][iindex] +=1
                if index>0:
                        points_grid[index-1][iindex] +=1
                if iindex >0:
                    points_grid[index][iindex -1] +=1
                    if index>0:
                        points_grid[index-1][iindex-1] +=1
                    if index<height-1:
                        points_grid[index+1][iindex-1] +=1
                if iindex <length-1:
                    points_grid[index][iindex +1] +=1
                    if index>0:
                        points_grid[index-1][iindex+1] +=1
                    if index<height-1:
                        points_grid[index+1][iindex+1] +=1        

set_bombs()
initialize_grid(points_grid)
initialize_grid(clicked_grid)
# print_open_grid(grid)
# print_grid(grid,True)
calc_points_of_cell()
# print_open_grid(points_grid)
start_game()