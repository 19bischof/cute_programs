import guy
import snak

skip = 0
def snake_logic():
    global skip
    if skip == 0:
        skip += 1
        if snake.head[1] == snak.width-1:
            snake.change_dir("south")
            snake.change_dir("west")
            skip += 1
        elif snake.head[1] == 0:
            snake.change_dir("south")
            snake.change_dir("east")
            skip += 1
    skip -= 1


snake = snak.snack()
guy.new_snack(snake,snake_logic)
guy.loopy(fps=60)