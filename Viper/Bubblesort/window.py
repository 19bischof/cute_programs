import pygame
from settings import Settings as st
pygame.init()
class Window:
    screen = pygame.display.set_mode([st.screen_width,st.screen_height])
    pygame.display.set_caption("Bubblesort")
    def check_events():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause = True
                    while pause:
                        for _event in pygame.event.get():
                            if _event.type == pygame.QUIT:
                                pygame.quit()
                            if _event.type == pygame.KEYUP:
                                if _event.key == pygame.K_SPACE:
                                    pause = False
    def update():
        pygame.display.flip()
    

