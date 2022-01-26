from multiprocessing.sharedctypes import Value
import pygame
from settings import settings as st
from piano_logic import pipino
pygame.init()


screen = pygame.display.set_mode(st.size)
next_note = True
while 1:
    pygame.time.Clock().tick(60)
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            # if event.key i
            # 1
            try:
                print("pressed:",chr(event.key),"\tnote:",pipino.cur_note)
            except ValueError:
                print("unknown character")
                pass
            if event.key == ord(pipino.cur_note):
                next_note = True
    if next_note:
        next_note = False
        pipino.next_note()
        screen.blit(pipino.cur_surface, (0, 0))
        pygame.display.flip()
