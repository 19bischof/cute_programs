class settings:
    win_x_off = 10
    win_y_off = 10
    win_width = 500
    win_height = win_width
    blocks_no = 20
    l_length = int(win_width/blocks_no) if win_width > win_height else int(win_height/blocks_no)
    # l_length = 100
    back_color = '#008212'
    l_colors = ('#AAAAAA','#5F007F') 
    block_colors = ('#DFDF00','#DF0000') #p1,p2
    l_width = 3
    b_color = '#000000'
    player_count = 2
    hitbox = 4
    running = True