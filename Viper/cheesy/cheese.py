from settings import settings as st


import random
class cheese:
    def __init__(self):
        one_block = [False] * 4  # top right down left
        self.all_blocks_lines = [
            [one_block.copy() for y in range(st.blocks_no)]
            for x in range(st.blocks_no)
        ]
        self.all_blocks_player = [[-1] * st.blocks_no] * st.blocks_no
        self.last_move = None  # ((c,r),line_index)
        self.cur_player = random.randrange(st.player_count)

    def update_block(self):
        c, r, line_i = self.last_move
        if self.all_blocks_lines[c][r].count(True) == 4:
            self.all_blocks_player[c][r] = self.cur_player
        calc_table = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}
        c_off, r_off = calc_table[line_i]
        if self.all_blocks_lines[c + c_off][r + r_off].count(True) == 4:
            self.all_blocks_player[c + c_off][r + r_off] = self.cur_player

    def set_line(self,c,r,line_i):
        if self.all_blocks_lines[c][r][line_i]:
            return "already taken"
        self.all_blocks_lines[c][r][line_i] = True
        self.cur_player = (self.curplayer+1)%st.player_count

    def evaluate_winner(self) :
        #can be tuple when draw 
        blocks_one_row = []
        winner = -1
        win_count = 0
        for i in range(st.blocks_no):
            blocks_one_row += self.all_blocks_player[i]
        for p in range(st.player_count):
            c = blocks_one_row.count(p)
            
            if c == win_count:
                winner = (winner,p)
            if c > win_count:
                winner = p
                win_count = c
            
        return winner
            