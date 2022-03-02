import snak


class deeper:
    snake = snak.snack()

    @classmethod
    def environment(cls):
        apple_y, apple_x = cls.snake.apple
        head_y, head_x = cls.snake.head
        if head_y > apple_y:
            apple_above = True
        else:
            apple_above = False
        if abs(head_y - apple_y) > int(snak.height / 2):
            apple_above = not apple_above  # because snake can walk through wall

        if head_x > apple_x:
            apple_left = True
        else:
            apple_left = False
        if abs(head_x - apple_x) > int(snak.width / 2):
            apple_left = not apple_left  # because snake can walk through wall
        body_length = len(cls.snake.body)
        direction = cls.snake.direction
        snake_bod = cls.snake.body

        return apple_above,apple_left,body_length,direction,snake_bod

    @classmethod
    def rewarding(cls):
        if cls.snake.state == 0:
            return -40
        if cls.snake.state == 2:
            return 100
        if cls.snake.digestion != 0:
            return 10
        