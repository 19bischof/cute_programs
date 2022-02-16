import time
import pygame
import pygame_gui
from settings import settings as st
from colorfade import fade_me
import thai

player_methods = {0: thai.bot4_ashley, 1: thai.bot4_ashley}


def draw_map():
    s = pygame.Surface((st.block_length * 3 + st.edge_offset * 2,) * 2)
    s.fill("#FFFFFF")
    for c in range(0, st.block_length * 4, st.block_length):
        pygame.draw.line(s, "#000000", (c, 0), (c, st.block_length * 3), 4)
        pygame.draw.line(s, "#000000", (0, c), (st.block_length * 3, c), 4)
    g = thai.grid.copy()
    for col in range(3):
        for row in range(3):
            if g[col][row] == 1:
                pygame.draw.circle(
                    s,
                    "#000000",
                    (
                        row * st.block_length
                        + st.block_length / 2
                        + st.edge_offset / 2,
                        col * st.block_length
                        + st.block_length / 2
                        + st.edge_offset / 2,
                    ),
                    st.block_length / 2 - st.edge_offset - 2,
                    5,
                )
            elif g[col][row] == 2:
                pygame.draw.line(
                    s,
                    "#000000",
                    (
                        row * st.block_length + st.edge_offset,
                        col * st.block_length + st.edge_offset,
                    ),
                    (
                        (row + 1) * st.block_length - st.edge_offset,
                        (col + 1) * st.block_length - st.edge_offset,
                    ),
                    5,
                )
                pygame.draw.line(
                    s,
                    "#000000",
                    (
                        row * st.block_length + st.edge_offset,
                        (col + 1) * st.block_length - st.edge_offset,
                    ),
                    (
                        (row + 1) * st.block_length - st.edge_offset,
                        col * st.block_length + st.edge_offset,
                    ),
                    5,
                )

    return s


def get_mouse_index():
    x, y = pygame.mouse.get_pos()
    x_div, y_div = int(x / st.block_length), int(y / st.block_length)
    if 0 <= x_div <= 2:
        if 0 <= y_div <= 2:
            return x_div, y_div


pygame.init()

pygame.display.set_caption("❤👌")
window_surface = pygame.display.set_mode((st.total_width, st.total_height))

background = pygame.Surface((st.total_width, st.total_height))
background.fill(pygame.Color("#000000"))

manager = pygame_gui.UIManager((800, 600), "./theme.json")

against_cpu_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(
        (
            (st.total_width - st.menu_button_size[0]) / 2,
            (st.total_height - st.menu_button_size[1]) / 2,
        ),
        st.menu_button_size,
    ),
    text="Play against CPU",
    manager=manager,
)

clock = pygame.time.Clock()


def game_logic():
    start = 0
    i = thai.p_index
    pygame.time.Clock().tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            st.running = False
        if i == st.my_index:
            if event.type == pygame.MOUSEBUTTONUP:
                ret = get_mouse_index()
                if ret:
                    x, y = ret
                    if not thai.grid[y][x]:
                        thai.func_place_sign((y, x))
                        

    background.fill("#FFFFFF")
    background.blit(draw_map(), (5, 5))
    window_surface.blit(background, (0, 0))

    pygame.display.update()
    if i != st.my_index:
        if st.my_index == -1:
            if time.perf_counter() - start > 1:
                start = time.perf_counter()
                player_methods[i]()
        else:
            player_methods[i]()
    if thai.finished():
        st.menu_time = True


def finish_menu():
    st.menu_time = False
    thai.reset_game()


def menu_logic(delay):

    time_delta = delay / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            st.running = False
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == against_cpu_button:
                finish_menu()
        manager.process_events(event)
    window_surface.blit(
        fade_me((st.total_width, st.total_height), "#00FFFF", "#000000"), (0, 0)
    )
    manager.update(time_delta)
    manager.draw_ui(window_surface)
    pygame.display.update()


clock = pygame.time.Clock()
while st.running:
    delay = clock.tick(60)
    if st.menu_time:
        menu_logic(delay)
    else:
        game_logic()
