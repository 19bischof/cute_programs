import pygame
from cheese import cheese
from settings import settings as st

pygame.init()

pygame.display.set_caption('Cheese 🧀')
window_surface = pygame.display.set_mode((st.win_width, st.win_height))

background = pygame.Surface((st.win_width, st.win_height))
background.fill(pygame.Color(st.b_color))

is_running = True


ch = cheese()
def draw_map():
    s = pygame.Surface((st.win_width,)*2)
    #vertical
    for c in range(0,st.l_length*st.blocks_no,st.l_length):
        for r in range(0,st.l_length*st.blocks_no,st.l_length):
            pygame.draw.line(s,st.l_color,(c,r),(c+st.l_length,r),st.l_width)

    #horizontal
    for c in range(0,st.l_length*st.blocks_no,st.l_length):
        for r in range(0,st.l_length*st.blocks_no,st.l_length):
            pygame.draw.line(s,st.l_color,(c,r),(c,r+st.l_length),st.l_width)
    return s

while is_running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.MOUSEBUTTONUP:
            x,y = pygame.mouse.get_pos()
            x_in,y_in = x%st.l_length,y%st.l_length
            #check if click on vertical:
            if abs(x_in*st.l_length - x ) <= 10:
                if abs((x_in+1)*st.l_length - x ) <= 10:
                    ch.set_line(y_in,x_in,) #left off here!!!
            #check if click on horizontal
            if abs(y_in*st.l_length - y ) > 10:
                if abs((y_in+1)*st.l_length - y ) > 10:
    window_surface.blit(background, (0, 0))
    background.blit(draw_map(),(0,0))
    pygame.display.update()