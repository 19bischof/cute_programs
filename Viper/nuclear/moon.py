import random 
import pygame
import time
import pathlib

red = "\033[31m"
reset = "\033[0m"
width, height = 1600, 800
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("REACTOR 🍌")
icon = pygame.image.load(pathlib.Path(
    __file__).parent.as_posix() + "/banana.jpg")
pygame.display.set_icon(icon)
done = False
error_ring_duration = 0.5


class drop:
    """class for the popups"""
    colors = ["#F49804", "#FACD10", "#0CB535", "#2C67F6","#5B23D5","#ff039a"]
    last_color = None

    def __init__(self):
        self.radius = random.randint(25, 50)
        self.color = self.gen_color()
        self.duration = 2
        self.position = self.gen_position()
        self.time_of_inception = time.perf_counter()
        self.expiry_date = 0

    @classmethod
    def gen_color(cls):
        pool = cls.colors.copy()
        if cls.last_color:
            pool.remove(cls.last_color)
        cls.last_color = random.choice(pool)
        return cls.last_color

    def gen_position(self):
        x = random.randrange(self.radius, width - self.radius)
        y = random.randrange(self.radius, height - self.radius)
        return x, y

    def get_cur_radius(self):
        return self.radius * (1 - (time.perf_counter() - self.time_of_inception) / self.duration)

    def to_surface(self):
        circle_width = 0
        clr = self.color
        rad = self.get_cur_radius()
        if time.perf_counter() - self.time_of_inception > self.duration:
            # time_it expired and now displays for 1 second error ring
            if not self.expiry_date:
                self.expiry_date = time.perf_counter()
            clr = '#800000'
            circle_width = 5
            rad = (time.perf_counter() - self.expiry_date)**2 / error_ring_duration**2 * 200 #the exponent for fast acceleration of error ring 
        pygame.draw.circle(
            new_surface := pygame.Surface((width, height)),
            clr,
            self.position,
            rad,
            circle_width
        )
        return new_surface

    def hit(self, position):
        x1, y1 = position
        x2, y2 = self.position
        delta_x = abs(x1 - x2)
        delta_y = abs(y1 - y2)
        pyth = (delta_x**2 + delta_y**2)**0.5
        if self.get_cur_radius() >= pyth:  # hit the drop
            self.expiry_date = True
            return True


def update_click_rate(avg=False):
    global last_hits, last_t
    cur_t = time.perf_counter()
    pre = ""
    if avg:
        last_hits = 0
        last_t = start_t
        pre = red + "avg: "
    rate = (hits - last_hits) / (cur_t - last_t)
    print(f"\r{pre}{rate:.2f} hit/s".ljust(15) + reset, end="", flush=True)
    last_t = cur_t
    last_hits = hits

class splash:
    """class for splash animation"""
    color = "#87CEEB"
    duration = 3
    width = 3
    def __init__(self,pos):
        self.pos = pos
        self.time_of_inception = time.perf_counter()
        self.expired = False
    
    def to_surface(self):
        if (t_diff := (time.perf_counter() - self.time_of_inception)) > self.duration:
            self.expired = True
            return False
        new_surface = pygame.Surface((width,height))
        for i in range(5):
            pygame.draw.circle(
            new_surface,
            self.color,
            self.pos,
            (1 + t_diff*3)**4*i,
            self.width
        )
        return new_surface


clock = pygame.time.Clock()
cur_pop = drop()
hits = 0
last_hits = 0
start_t = time.perf_counter()
last_t = start_t
delta_t = 0
splashes: list[splash] = []
while not done:
    delta_t += clock.tick(60)
    if delta_t > 2000:  # after 2 seconds
        update_click_rate()
        delta_t = 0
    if cur_pop.expiry_date and (time.perf_counter() - cur_pop.expiry_date) > error_ring_duration:   #after showing of error ring
        cur_pop = drop() #new_instance
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if cur_pop.hit(event.pos):
                hits += 1
            else:
                splashes.append(splash(event.pos))
    screen.blit(cur_pop.to_surface(), (0, 0))
    for s in splashes.copy():
        sur = s.to_surface()
        if not sur:
            splashes.remove(s)
            continue
        screen.blit(sur,(0,0),special_flags=pygame.BLEND_ADD)
    pygame.display.flip()

update_click_rate(avg=True)
