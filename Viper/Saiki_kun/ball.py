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
    speed = st.ball_speed
    directions = {"left": -1, "right": 1}

    def __init__(self, x_pos, y_pos):
        ball.all_balls.append(self)
        self.direction = random.choice((1,-1))
        self.position = [x_pos, y_pos]
        self.balls_in_same_lane = []

    def move(self):
        self.position[0] += self.direction * ball.speed
        if self.collides_with_other_ball_in_same_lane_or_OOB():
            self.direction *= -1

    def collides_with_other_ball_or_OOB(self):
        #if OOB:
        if self.position[0] < ball.radius or self.position[0]> st.width - ball.radius:
            return True
        #collision:
        for b in self.all_balls:
            if b == self:
                continue
            x_diff = abs(self.position[0] - b.position[0])
            y_diff = abs(self.position[1] - b.position[1])
            if math.sqrt(x_diff**2 + y_diff**2) < ball.radius*2:
                return True
        
        return False

    def collides_with_other_ball_in_same_lane_or_OOB(self):
        #if OOB:
        if self.position[0] < ball.radius or self.position[0]> st.width - ball.radius:
            return True
        #collision:
        for b in self.balls_in_same_lane:
            if b == self:
                continue
            x_diff = abs(self.position[0] - b.position[0])
            y_diff = abs(self.position[1] - b.position[1])
            if math.sqrt(x_diff**2 + y_diff**2) < ball.radius*2:
                return True
        
        return False
    def collides_witih_neighbours_or_OOB(self):
        #doesnt work as of yet -> even the theory isn't thought out properly : there are a max of two possible neighbours on each side (maybe)
        #how to calculate that and even is that worth it considering the rendering of collisions is extremely fast
        #if OOB:
        if self.position[0] < ball.radius or self.position[0]> st.width - ball.radius:
            return True
        #collision:
        for b in self.balls_in_same_lane:
            x_diff = abs(self.position[0] - b.position[0])
            y_diff = abs(self.position[1] - b.position[1])
            if math.sqrt(x_diff**2 + y_diff**2) < ball.radius*2:
                return True
    def remove_ball(b):
        ball.all_balls.remove(b)

    def move_balls():
        for b in ball.all_balls:
            b.move()

    def draw_balls_on_Surface(S: Surface):
        for b in ball.all_balls:
            draw.circle(S, ball.color, b.position, ball.radius)

    def spawn_balls(x_space, y_space, max_count):
        print("spawning...")
        for i in range(max_count):
            tries = 0
            while_condition = 100
            while tries < while_condition:
                x_pos = random.randint(ball.radius, x_space-ball.radius)
                y_pos = random.randint(ball.radius, y_space-ball.radius)
                cur_ball = ball(x_pos, y_pos)
                if ball.collides_with_other_ball_or_OOB(cur_ball):
                    ball.remove_ball(cur_ball)
                    tries += 1
                else:
                    break
            if tries == while_condition:
                break
        # ball.calc_ball_neighbours_for_all_balls() neighbours dont work reason is below
        ball.calc_balls_in_same_lane()
        print("spawned",len(ball.all_balls),"balls")

    def calc_balls_in_same_lane():
        for b in ball.all_balls:
            for ob in ball.all_balls:
                if b == ob:
                    continue
                if abs(ob.position[1]-b.position[1]) < ball.radius * 2:
                    b.balls_in_same_lane.append(ob)
    # def calc_ball_neighbours_for_all_balls():
        #commented out because i realized that two balls can hit 
        #the same ball from the right for example
        #and not touch each other if they are close enough vertically
        # smallest_left = -1 
        # left_ball = None
        # smallest_right = -1
        # right_ball = None
        # for h in b.balls_in_same_lane:
        #     diff = h.position[0]-b.position[0]
        #     if diff<smallest_right and diff >0:
        #         right_ball = h
        #     diff = b.position[0]-h.position[0]
        #     if diff<smallest_left and diff >0:
        #         left_ball = h
        # b.ball_neighbours = [left_ball,right_ball]
if __name__ == "__main__":
    ball.spawn_balls(100, 100, 100)
    for b in ball.all_balls:
        print(b.position)
    print(len(ball.all_balls))
