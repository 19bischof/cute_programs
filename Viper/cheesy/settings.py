class settings:
    win_x_off = 10
    win_y_off = 10
    win_width = 500
    win_height = win_width
    blocks_no = 2
    l_length = int(win_width/blocks_no) if win_width > win_height else int(win_height/blocks_no)
    l_length = 100
    l_colors = ('#AAAAAA','#FF00FF') 
    block_colors = ('#FFFF00','#FF0000','#000000') #p1,p2,normal
    l_width = 3
    b_color = '#000000'
    player_count = 2
    hitbox = 10
    running = True