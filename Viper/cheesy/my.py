import pygame
from cheese import cheese
from settings import settings as st

pygame.init()

pygame.display.set_caption('Cheese 🧀')
window_surface = pygame.display.set_mode(
    (st.win_width + st.win_x_off*2, st.win_height + st.win_y_off*2))

background = pygame.Surface(
    (st.win_width + st.win_x_off*2, st.win_height + st.win_y_off*2))
background.fill(pygame.Color(st.b_color))


ch = cheese()


def check_mouse():
    x, y = pygame.mouse.get_pos()
    x, y = x-st.win_x_off, y-st.win_y_off
    x_div, y_div = int(x/st.l_length), int(y/st.l_length)
    if x - x_div*st.l_length >= st.l_length - st.hitbox:
        x_div += 1
    if y - y_div*st.l_length >= st.l_length - st.hitbox:
        y_div += 1
    # check if click on vertical:
    if x - (x_div*st.l_length) <= st.hitbox:
        ch.set_line(y_div, x_div, "vertical")
    # check if click on horizontal
    if y - (y_div*st.l_length) <= st.hitbox:
        ch.set_line(y_div, x_div, "horizontal")


def draw_map():
    s = pygame.Surface((st.win_width+st.win_x_off*2,
                       st.win_height+st.win_y_off*2))
    # vertical
    for c_i, c in enumerate(range(0, st.l_length*st.blocks_no, st.l_length)):
        for r_i, r in enumerate(range(0, st.l_length*(st.blocks_no+1), st.l_length)):
            ret = ch.is_line_set(c_i, r_i, "vertical")
            pygame.draw.line(
                s, st.l_colors[ret], (r, c), (r, c+st.l_length), st.l_width)

    # horizontal
    for c_i, c in enumerate(range(0, st.l_length*(st.blocks_no+1), st.l_length)):
        for r_i, r in enumerate(range(0, st.l_length*st.blocks_no, st.l_length)):
            ret = ch.is_line_set(c_i, r_i, "horizontal")
            pygame.draw.line(
                s, st.l_colors[ret], (r, c), (r+st.l_length, c), st.l_width)

    for c_i in range(st.blocks_no):
        for r_i in range(st.blocks_no):
            if ch.all_blocks_player[c_i][r_i] != -1:
                # print(c_i,r_i)
                pygame.draw.rect(s, st.block_colors[ch.all_blocks_player[c_i][r_i]],
                                 (r_i*st.l_length, c_i*st.l_length, st.l_length, st.l_length))

    return s


clock = pygame.time.Clock()
cur_player = None
while st.running:
    clock.tick(60)
    if cur_player != ch.cur_player:
        cur_player = ch.cur_player
        pygame.display.set_caption('Player{} 🧀'.format(cur_player))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            st.running = False
        if event.type == pygame.MOUSEBUTTONUP:
            check_mouse()

    window_surface.blit(background, (0, 0))
    background.blit(draw_map(), (st.win_x_off, st.win_y_off))
    pygame.display.update()
