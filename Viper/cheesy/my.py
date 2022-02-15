import pygame
from settings import settings as st

pygame.init()

pygame.display.set_caption('Cheese 🧀')
window_surface = pygame.display.set_mode((st.width, st.height))

background = pygame.Surface((st.width, st.height))
background.fill(pygame.Color(st.b_color))

is_running = True

while is_running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    window_surface.blit(background, (0, 0))

    pygame.display.update()