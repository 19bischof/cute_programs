import pygame
import sys
from settings import Settings as st


class Window:
    in_focus = False
    instance = None

    def __init__(self, Title):
        pygame.init()
        self.screen = pygame.display.set_mode([st.screen_width, st.screen_height])
        pygame.display.set_caption(Title)
        Window.instance = self

    def check_events():
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        Window.in_focus = True
                        pause = True
                        while pause:
                            for _event in pygame.event.get():
                                if _event.type == pygame.QUIT:
                                    sys.exit()
                                if _event.type == pygame.KEYUP:
                                    if _event.key == pygame.K_SPACE:
                                        pause = False
            if Window.in_focus:
                break

    def update():
        pygame.display.flip()
