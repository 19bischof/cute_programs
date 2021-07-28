import pygame
import random
pygame.init()
screen_height = 500
screen_width = 500
ship_width = 50
ship_height = 50
ball_radius = 20
ball_speed=5
ufo_width = 32
ufo_height = 18 
ufo_speed = 1
list_of_ufos = []
frame_count = 0
# pygame.draw.circle(screen, (0,0,255),(250,250),75)
screen = pygame.display.set_mode([screen_height, screen_width])
pygame.display.set_caption('Alien_invasion')
shipx = 0
shipy = screen_height - ship_height - 2
shipv = 0
list_of_cannonballs = []
max_number_of_empty_balls = 10
number_of_empty_balls = max_number_of_empty_balls - 1
space_pressed = False
running = True
ball_image = pygame.image.load("./images/medicine-ball.png").convert_alpha()
ball_image = pygame.transform.smoothscale(ball_image,(ball_radius*2,ball_radius*2))
ship_image = pygame.image.load("./images/ship.png").convert_alpha()
ship_image = pygame.transform.smoothscale(ship_image,(ship_width,ship_height))
ufo_image = pygame.image.load("./images/ufo.png").convert_alpha()
ufo_image = pygame.transform.smoothscale(ufo_image,(ufo_width,ufo_height))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                shipv=-2
            if event.key == pygame.K_RIGHT:
                shipv= 2
            if event.key == pygame.K_SPACE:
                space_pressed = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                if shipv<0:
                    shipv = 0
            if event.key == pygame.K_RIGHT:
                if shipv > 0:
                    shipv = 0
            if event.key == pygame.K_SPACE:
                space_pressed = False
                number_of_empty_balls = max_number_of_empty_balls - 1
    if space_pressed:
        number_of_empty_balls += 1 
        number_of_empty_balls=  number_of_empty_balls % max_number_of_empty_balls
        if number_of_empty_balls == 0:
            cannonball = [shipx+ship_width/2,shipy]
            list_of_cannonballs.append(cannonball)

    screen.fill((255,255,255))
    pygame.draw.rect(screen,(3, 127, 252),(0,screen_height*0.96,screen_width,screen_height*0.04))   #drawing the sea
    shipv *= 1.03                                                                                        #acceleration 
    shipx+=shipv
    if shipx < 0:
        shipx = 0
    if shipx > screen_width  - ship_width:
        shipx = screen_width - ship_width


    for index,ball in enumerate(list_of_cannonballs[:]):
        ball[1] -= ball_speed
        if ball[1] <0:
            del list_of_cannonballs[index]
        pygame.draw.circle(screen, (255,0,0),tuple(ball),ball_radius)

        screen.blit(ball_image,(ball[0]-ball_radius,ball[1]-ball_radius))
        for index,ufo in enumerate(list_of_ufos[:]):
            if ufo[1] + ufo_height >= ball[1] - ball_radius:
                if ufo[0]>ball[0]-ball_radius and  ufo[0] < ball[0]+ball_radius or ufo[0]<ball[0] -ball_radius and ufo[0] + ufo_width >= ball[0]-ball_radius:
                    del list_of_ufos[index]
                

    if frame_count % 100 == 0:
       current_ufo = [random.randint(ufo_width/2,screen_width-ufo_width),0]
       list_of_ufos.append(current_ufo)

    for index,ufo in enumerate(list_of_ufos[:]):
        ufo[1] += ufo_speed
        if ufo[1] + ufo_height > screen_height:
            print("You lost the game!")
            running = False
        # if ufo is hit by ball:
        #     del list_of_ufos[index]
        screen.blit(ufo_image,(ufo[0],ufo[1]))
    screen.blit(ship_image,(shipx,shipy))
    pygame.display.flip()
    clock = pygame.time.Clock()
    clock.tick(60)
    frame_count +=1
 
pygame.quit()