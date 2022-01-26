class settings:
    size = width, height = 600, 600 #min width: 120,min height:100
    black = '#000000'
    white = '#FFFFFF'
    grey = '#838780'
    red = '#FF0000'
    ratio = 20
    # if width< height:
    #     note_radius = width/2 -15
    # else:
    note_radius = height/ratio
    line_width = 4
    line_diff = note_radius*2 + line_width
    #there are currently 13 positions
    number_of_pos = 13
    y_offset = (height - ((number_of_pos-1)*line_diff/2))/2
