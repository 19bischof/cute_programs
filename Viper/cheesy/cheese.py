from cv2 import line
from numpy import block
from settings import settings as st

import random


class cheese:
    def __init__(self):
        one_block = [False] * 4  # top right down left
        self.all_blocks_lines = [
            [one_block.copy() for y in range(st.blocks_no)]
            for x in range(st.blocks_no)
        ]
        self.all_blocks_player = [[-1 for x in range(st.blocks_no)] for y in range(st.blocks_no)]
        self.last_move = None  # (c,r,line_index)
        self.cur_player = random.randrange(st.player_count)

    def _get_line(self, c, r, line_type):
        # returns c,r,line_index
        if line_type == "horizontal":
            if c < st.blocks_no:
                return c, r, 0
            if c > 0:
                return c-1, r, 2
        elif line_type == "vertical":
            if r < st.blocks_no:
                return c, r, 3
            if r > 0:
                return c, r-1, 1

    def _get_other_line(self, c, r, line_index):
        new_index = (line_index+2) % 4
        calc_table = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}
        c_off, r_off = calc_table[new_index]
        if line_index%2: #vertical
            if r-r_off >= 0 and r-r_off < st.blocks_no:
                self.all_blocks_lines[c-c_off][r-r_off][new_index]
                return c-c_off, r-r_off, new_index
        
        else: #horizontal
            if c-c_off >= 0 and c-c_off < st.blocks_no:
                self.all_blocks_lines[c-c_off][r-r_off][new_index]
                return c-c_off, r-r_off, new_index

    def block_completed(self):
        completed = False
        c, r, line_index = self.last_move
        if self.all_blocks_lines[c][r].count(True) == 4:
            self.all_blocks_player[c][r] = self.cur_player
            completed = True
        ret = self._get_other_line(c,r,line_index)
        if ret:
            c, r, line_index = ret
            if self.all_blocks_lines[c][r].count(True) == 4:
                self.all_blocks_player[c][r] = self.cur_player
                completed = True
        if completed:
            self.cur_player = (self.cur_player+1) % st.player_count


    def set_line(self, c, r, line_type):
        c, r, line_index = self._get_line(c, r, line_type)
        if self.all_blocks_lines[c][r][line_index]:
            return "already set!"
        self.all_blocks_lines[c][r][line_index] = True
        ret = self._get_other_line(c,r,line_index)
        if ret:
            new_c,new_r,new_line_index = ret
            self.all_blocks_lines[new_c][new_r][new_line_index] = True
        self.last_move = (c, r, line_index)
        self.block_completed()
        self.evaluate_winner()
        self.cur_player = (self.cur_player+1) % st.player_count

    def is_line_set(self, c, r, line_type):
        ret = self._get_line(c, r, line_type)
        if ret is not None:
            c,r,line_index = ret
            return self.all_blocks_lines[c][r][line_index]
        return -1

    def evaluate_winner(self):
        # can be tuple when draw
        blocks_one_row = []
        winner = -1
        win_count = 0
        for i in range(st.blocks_no):
            blocks_one_row += self.all_blocks_player[i]
        if blocks_one_row.count(-1) != 0:
            return None
        for p in range(st.player_count):
            c = blocks_one_row.count(p)

            if c == win_count:
                winner = (winner, p)
            if c > win_count:
                winner = p
                win_count = c
        st.running = False
        print("The player{} won the game!".format(winner))


if __name__ == "__main__":
    ch = cheese()
    c,r,line_index = ch._get_line(1,4,"horizontal")
    print(c,r,line_index)
    print(ch._get_other_line(c,r,line_index))