class settings:
    size = width, height = 600, 600 #min width: 120,min height:100
    fps = 60
    sec = 30
    font_size = 30
    easy_mode = True
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

    what_clefs = ("g","f")
    interactive_config = True

    def config():
        if not settings.interactive_config:
            return
        while True:
            ans = input("Which clef do you want to train? (g,f,both)").lower().strip()
            if ans in ("g","f","both"):
                break
            print("wrong input!")
        if ans == "both":
            settings.what_clefs = ("f","g")
        else:
            settings.what_clefs = ans
        while True:
            ans = input("Easy mode? (y,n)").lower().strip()
            if ans in ("yes","y","n","no"):
                break
            print("wrong input!")
        if ans in ("yes","y"):
            settings.easy_mode = True
        else:
            settings.easy_mode = False