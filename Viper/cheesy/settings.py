class settings:
    win_width = 600
    win_height = 600
    blocks_no = 5
    l_length = int(win_width/blocks_no) if win_width > win_height else int(win_height/blocks_no)
    l_color = '#20A0C0'
    l_width = 3
    b_color = '#000000'
    player_count = 2