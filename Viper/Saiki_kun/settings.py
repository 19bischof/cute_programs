factor = 1
class settings:
    ball_radius = 10*factor
    ball_speed = 1 * factor
    background_color = '#052732'
    ball_color = '#e6da95'
    max_number_of_balls = 1000000  #might not be accurate since max sometimes cant fit in to a window so filename would also be not accurate
    width = 1920*factor  #30 is min for both
    height = 1080*factor
    #window-title-bar 31 pixel height
    #window-right-shifted is 8 pixel width
    #-31 and -8 to get perfect fullscreen
    x_shift = -8
    y_shift = -31
    fps = 60
    duration = 120   #in seconds
    #--------------------
    number_of_frames = fps * duration
    all_bytes = width * height * fps * duration * 3 #3 because 24 bit color for each pixel
    billion = 1000000000    
    number_of_steps = int(all_bytes / billion * 100) + 1    #times 100 for fun so to get more files
    step = int(number_of_frames / number_of_steps)
    #----------------------
    raw_file_name = "in"+str(step)+"and"+str(width)+"x"+str(height)+"_of_" + str(max_number_of_balls)+"_with_"+str(ball_radius)+"_in_" + str(duration)+".var"
    comp_file_name = raw_file_name + ".zip"
    comp_protocol = "zip"    #gztar
    dir_of_animations = "animations"
    raw_file_path =  dir_of_animations+'/'+ raw_file_name
    comp_file_path = dir_of_animations + '/'+comp_file_name
    video_file_name = raw_file_name[:-4] + ".mp4"
    video_directory = "compiled_videos"
    video_file_path = video_directory+'/'+video_file_name