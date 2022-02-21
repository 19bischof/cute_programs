import time
import snak
import pygame
import colorfade

width, height = 600, 600
pygame.init()

pygame.display.set_caption("Snak")
window_surface = pygame.display.set_mode((width, height))


is_running = True
snack = snak.snack()


def draw():
    background = pygame.Surface((width, height))
    background.fill(pygame.Color("#000000"))
    block_size = (int(height / snak.height), int(width / snak.width))
    for b in snack.body:
        pygame.draw.rect(
            background,
            "green",
            (b[1] * block_size[1], b[0] * block_size[0], block_size[1], block_size[0]),
            width=2,
        )
    pygame.draw.rect(
        background,
        "red",
        (
            snack.apple[1] * block_size[1],
            snack.apple[0] * block_size[0],
            block_size[1],
            block_size[0],
        ),
    )
    # pygame.draw.rect(
    #     background,
    #     "blue",
    #     (
    #         snack.head[1] * block_size[1],
    #         snack.head[0] * block_size[0],
    #         block_size[1],
    #         block_size[0],

    #     ),
    #     width=0

    # )
    ind = -1 if snack.direction % 2 == 0 else 1
    s = pygame.transform.rotate(
        colorfade.fade_me(block_size[::ind], "black", "blue"), snack.direction * -90
    )
    background.blit(
        s,
        (snack.head[1] * block_size[1], snack.head[0] * block_size[0]),
    )
    return background


clock = pygame.time.Clock()
start_t = time.perf_counter()
while snack.state == 1 and is_running:
    clock.tick(5)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.KEYDOWN:

            if event.key in (pygame.K_UP, ord("w")):
                snack.change_dir(0)
            elif event.key in (pygame.K_RIGHT, ord("d")):
                snack.change_dir(1)
            elif event.key in (pygame.K_DOWN, ord("s")):
                snack.change_dir(2)
            elif event.key in (pygame.K_LEFT, ord("a")):
                snack.change_dir(3)
    snack.move()
    background = draw()
    window_surface.blit(background, (0, 0))

    pygame.display.update()

print("You have a score of {}".format(snack.score))
if snack.state == 2:
    print("You have won the game")
