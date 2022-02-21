import pygame
import numpy
def fade_me(size:tuple[int,int],start_color,end_color) -> pygame.Surface:
    """fills a Surface with a color_fade (top-bottom) from start_color to end_color
    :param start_color,end_color: an rgb tuple or color name or hash value
    :param size: x,y"""
    start_c = pygame.Color(start_color)
    end_c = pygame.Color(end_color)
    r_s,g_s,b_s = start_c.r,start_c.g,start_c.b
    r_e,g_e,b_e = end_c.r,end_c.g,end_c.b
    step_count = size[1]
    r_diff = (r_s - r_e) / step_count
    g_diff = (g_s - g_e) / step_count
    b_diff = (b_s - b_e) / step_count
    step = 0
    arr = numpy.ndarray(size[::-1]+(3,),dtype=numpy.uint8)
    for y in range(size[1]):
        col_v = (int(r_s-r_diff*step),int(g_s-g_diff*step),int(b_s-b_diff*step))
        row = numpy.full((size[0],3),col_v,dtype=numpy.uint8)
        arr[y] = row
        
        step += 1
    arr = arr.transpose((1,0,2))
    return pygame.surfarray.make_surface(arr)

if __name__ == '__main__':
    size = (200,600)
    c_start = '#00FFFF'
    c_end = '#000000'
    s = fade_me(size,c_start,c_end)
    pygame.init()
    window_screen = pygame.display.set_mode(size)
    is_running = True
    while is_running:
        for event in pygame.event.get():
             if event.type == pygame.QUIT:
               is_running = False
        window_screen.blit(s,(0,0))
        pygame.display.update()