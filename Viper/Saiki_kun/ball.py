import math
import random
from pygame import Surface, draw
from settings import settings as st

class ball:
    screen_width = st.width
    screen_height = st.height
    color = st.ball_color
    all_balls: list['ball'] = []
    radius = st.ball_radius
    speed = 1
    directions = {"left": -1, "right": 1}

    def __init__(self, x_pos, y_pos):
        ball.all_balls.append(self)
        self.direction = random.choice((1,-1))
        self.position = [x_pos, y_pos]

    def move(self):
        self.position[0] += self.direction * ball.speed
        if self.collides_with_other_ball_or_OOB():
            self.direction *= -1

    def collides_with_other_ball_or_OOB(self):
        if self.position[0] < ball.radius or self.position[0]> st.width - ball.radius:
            return True
        for b in ball.all_balls:
            if b is self:
                continue
            x_diff = abs(self.position[0] - b.position[0])
            y_diff = abs(self.position[1] - b.position[1])
            if math.sqrt(x_diff**2 + y_diff**2) < ball.radius*2:
                return True
        
        return False

    def remove_ball(b):
        ball.all_balls.remove(b)

    def move_balls():
        for b in ball.all_balls:
            b.move()

    def draw_balls_on_Surface(S: Surface):
        for b in ball.all_balls:
            draw.circle(S, ball.color, b.position, ball.radius)

    def spawn_balls(x_space, y_space, max_count):
        for i in range(max_count):
            tries = 0
            while tries < 1000:
                x_pos = random.randint(ball.radius, x_space-ball.radius)
                y_pos = random.randint(ball.radius, y_space-ball.radius)
                cur_ball = ball(x_pos, y_pos)
                if ball.collides_with_other_ball_or_OOB(cur_ball):
                    ball.remove_ball(cur_ball)
                    tries += 1
                else:
                    break
            if tries == 1000:
                break
        print("spawned",len(ball.all_balls),"balls")


if __name__ == "__main__":
    ball: ball = 0
    ball.spawn_balls(100, 100, 100)
    for b in ball.all_balls:
        print(b.position)
    print(len(ball.all_balls))
