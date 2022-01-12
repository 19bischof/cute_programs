factor = 1
class settings:
    ball_radius = 8*factor
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
    duration = 180   #in seconds
    raw_file_name = str(width)+"x"+str(height)+"_of_" + str(max_number_of_balls)+"_with_"+str(ball_radius)+"_in_" + str(duration)+".var"
    comp_file_name = raw_file_name + ".zip"
    comp_protocol = "zip"    #gztar
    dir_of_animations = "animations"
    raw_file_path =  dir_of_animations+'/'+ raw_file_name
    comp_file_path = dir_of_animations + '/'+comp_file_name
    video_file_name = raw_file_name[:-4] + ".mp4"
    video_directory = "compiled_videos"
    video_file_path = video_directory+'/'+video_file_name