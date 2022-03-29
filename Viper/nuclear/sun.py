import random
import pygame
import time
import pathlib
width, height = 400, 300
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("REACTOR 🍌")
icon = pygame.image.load(pathlib.Path(
    __file__).parent.as_posix() + "/banana.jpg")
pygame.display.set_icon(icon)
done = False


def create_new_timing() -> float:
    formula = 0.5 + (random.random() * 6) ** 1.5 / 2 + random.random() * 2
    return time.perf_counter() + formula


timing = 0
clock = pygame.time.Clock()
state = "recover"
screen.fill("red")
font = pygame.font.SysFont("serif", 40)
img = font.render('Press Space', True, "black")
screen.blit(img, (width/2 - 90, height/2 - 30))
while not done:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if state == "recover":
                    timing = create_new_timing()
                    screen.fill("black")
                    state = "idle"
                if state == "armed":
                    delay = str(int((time.perf_counter() - timing)*1000)) + " ms"
                    print(delay)
                    state = "recover"
                    screen.fill("red")
                    result = font.render(delay, True, "black")
                    screen.blit(result, (width/2 - 50, height/2 - 30))
    if time.perf_counter() > timing and state == "idle":
        state = "armed"
        screen.fill("green")
        screen.blit(img, (width/2 - 90, height/2 - 30))



    pygame.display.flip()
