import pygame
import random

class Conni:
    screen_height = 500
    screen_width = 1000
    running = True
    frames = 0
    max_number_of_empty_balls = 10
    number_of_empty_balls = max_number_of_empty_balls - 1
    space_pressed = False
    spawn_speed = 0

    pygame.init()
    screen = pygame.display.set_mode([screen_width, screen_height])
    pygame.display.set_caption("Alien Invasion")
    def game_start():
        Conni.my_ship = Ship()
        Conni.game_loop()
    
    def game_loop():
        while(Conni.running):
            Conni.check_events()            
            Conni.draw()
            Conni.motion()
            Conni.generate()
            Conni.grow()
            pygame.time.Clock().tick(60)
            pygame.display.flip()
            Conni.frames += 1
        pygame.quit()
        print("Score: ",int(Conni.frames/501))
    def check_events():
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Conni.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    Conni.my_ship.speed = -3
                if event.key == pygame.K_RIGHT:
                    Conni.my_ship.speed = 3
                if event.key == pygame.K_SPACE:
                    Conni.space_pressed = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    if Conni.my_ship.speed<0:
                        Conni.my_ship.speed = 0
                if event.key == pygame.K_RIGHT:
                    if Conni.my_ship.speed > 0:
                        Conni.my_ship.speed = 0
                if event.key == pygame.K_SPACE:
                    Conni.space_pressed = False
                    Conni.number_of_empty_balls = Conni.max_number_of_empty_balls - 1
    def draw():
        Conni.screen.fill((255,255,255))
        pygame.draw.rect(Conni.screen,(3, 127, 252),(0,Conni.screen_height*0.96,Conni.screen_width,Conni.screen_height*0.04))   #drawing the sea
        Conni.my_ship.draw()
        Ball.draw()
        Alien.draw()
    def generate():
        if Conni.space_pressed:
            Conni.number_of_empty_balls += 1
            if Conni.number_of_empty_balls % Conni.max_number_of_empty_balls == 0:
                Ball(Conni.my_ship.x+Conni.my_ship.width/2,Conni.my_ship.y)
        
        if Conni.frames % (100 - int(Conni.spawn_speed)) == 0:
            Alien()
            Conni.spawn_speed += 5 - 5*Conni.spawn_speed/99

    def grow():
        if Conni.frames % 100 == 0:
            Ball.radius += 1
            Ship.width += 1
            Ship.height += 1

        

    def motion():
        Conni.my_ship.motion()
        Ball.motion()
        Alien.motion()

class Alien:
    height = 18
    width = 32
    speed = 1
    image = pygame.image.load("./images/ufo.png").convert_alpha()
    image = pygame.transform.smoothscale(image,(width,height))
    instances = []
    def __init__(self):
        self.x = random.randint(0,Conni.screen_width-Alien.width)
        self.y = 0 - Alien.height
        self.direction = 1                                                  #right is 1, left is -1
        Alien.instances.append(self)
    def draw():
        for a in Alien.instances:
            Conni.screen.blit(Alien.image,(a.x,a.y))
    def motion():
        shift = 0
        for index,a in enumerate(Alien.instances[:]):
            a.y += Alien.speed
            a.x += Alien.speed * a.direction
            if a.x < 0 :
                a.x = 0
            if a.x > Conni.screen_width - Alien.width:
                a.x = Conni.screen_width - Alien.width
            if random.randint(-1,100)==a.direction:
                a.direction *= -1
            if a.y + Alien.height >= Conni.screen_height:
                Conni.running = False
            for b in Ball.instances: 
                # if b.y - Ball.radius< a.y + Alien.height and b.y + Ball.radius > a.y:
                #     if b.x - Ball.radius< a.x and b.x + Ball.radius > a.x or b.x - Ball.radius> a.x and b.x - Ball.radius < a.x + Alien.width:            #rectangle ball calc
                if (a.x + Alien.width - b.x)**2 + (a.y + Alien.height - b.y)**2 <= Ball.radius**2 or (a.x  - b.x)**2 + (a.y + Alien.height - b.y)**2 <= Ball.radius**2 or a.x < b.x < a.x + Alien.width and b.y-a.y <= Ball.radius:
                        del Alien.instances[index - shift]
                        shift += 1
        Alien.speed + 0.001
class Ball:
    radius = 20
    speed = 5
    list_of_colors = [(239,7,73),(224,93,244),(93,216,244),(93,244,133),(222,244,93),(242,114,29)]
    color_index = 0
    pre_image = pygame.image.load("./images/medicine-ball.png").convert_alpha()
    instances = []
    def __init__(self,x,y):
        self.x = x                                                                                          #x and y are the middle of the ball
        self.y = y
        self.color = Ball.list_of_colors[Ball.color_index]
        Ball.color_index = (Ball.color_index +1) % len(Ball.list_of_colors)
        Ball.instances.append(self)
    def draw():
        Ball.image = pygame.transform.smoothscale(Ball.pre_image,(Ball.radius*2,Ball.radius*2))
        for b in Ball.instances:
            pygame.draw.circle(Conni.screen,b.color,(b.x,b.y),Ball.radius)
            Conni.screen.blit(Ball.image,(b.x-Ball.radius,b.y-Ball.radius))
    def motion():
        shift = 0
        for index,b in enumerate(Ball.instances[:]):
            b.y -= Ball.speed
            if b.y < -2*Ball.radius:
                del Ball.instances[index-shift]
                shift += 1
        
class Ship:
    width = 50
    height = 50
    acceleration = 1.03
    y = Conni.screen_height - height - 2
    pre_image = pygame.image.load("./images/ship.png").convert_alpha()
    def __init__(self):
        self.x = 0
        self.speed = 0
    def draw(self):
        Ship.image = pygame.transform.scale(Ship.pre_image,(Ship.width,Ship.height))

        Conni.screen.blit(Ship.image,(self.x,Ship.y))
    def motion(self):
        Ship.y = Conni.screen_height - Ship.height - 2

        self.speed = self.speed * self.acceleration
        self.x += int(self.speed)
        if self.x < 0:
            self.x = 0
        if self.x > Conni.screen_width - self.width:
            self.x = Conni.screen_width - self.width


Conni.game_start()
