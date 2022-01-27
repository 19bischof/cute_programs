import pygame  # import after userinput so window is in front
from time import sleep
from piano_logic import pipino
from settings import settings as st
st.config()

pygame.init()
screen = pygame.display.set_mode(st.size)
pygame.display.set_caption("Pipino")
next_note = True
clock = pygame.time.Clock()
max_frames = st.fps*st.sec
i = 0
correct_note = -1
note_press = 0
while i < max_frames:
    i += 1
    clock.tick(st.fps)  # controls fps
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            try:
                print("pressed:", chr(event.key), "\tnote:", pipino.cur_note)
                if chr(event.key) in ('c', 'd', 'e', 'f', 'g', 'a', 'h'):
                    note_press += 1
            except ValueError:
                print("unknown character")
                pass

            if event.key == ord(pipino.cur_note):
                next_note = True
    if next_note:
        correct_note += 1
        next_note = False
        pipino.next_note()
        screen.blit(pipino.cur_surface, (0, 0))
        pygame.display.flip()
pygame.quit()
if note_press != 0:
    acc = correct_note/note_press
else:
    acc = 0
print("You hit %d notes in %d seconds.\nSpeed: %.2f n/s Accuracy: %.0f%%" %
      (correct_note, st.sec, correct_note/st.sec, acc*100))
sleep(2)
