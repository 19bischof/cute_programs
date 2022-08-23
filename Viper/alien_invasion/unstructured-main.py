import pygame
import random
import pathlib
#important:
#ufo[] gives first x then y of the upper left corner of the rect.
#ball[] gives first x then y of the middle of the sphere
project_path = pathlib.Path(__file__).absolute().parent.as_posix()
pygame.init()
screen_height = 500
screen_width = 1000
ship_width = 50
ship_height = 50
ball_radius = 20
ball_speed=5
ufo_width = 32
ufo_height = 18 
ufo_speed = 1
spawn_speed = 0
list_of_ufos = []
frame_count = 0
list_of_colors = [(239,7,73),(224,93,244),(93,216,244),(93,244,133),(222,244,93),(242,114,29)]
color_id = 0
# pygame.draw.circle(screen, (0,0,255),(250,250),75)
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption('Alien Invasion')
shipx = 0
shipy = screen_height - ship_height - 2
shipv = 0
list_of_cannonballs = []
max_number_of_empty_balls = 10
number_of_empty_balls = max_number_of_empty_balls - 1
space_pressed = False
running = True
ball_image = pygame.image.load(project_path+"/images/medicine-ball.png").convert_alpha()
ball_image = pygame.transform.smoothscale(ball_image,(ball_radius*2,ball_radius*2))
ship_image = pygame.image.load(project_path+"/images/ship.png").convert_alpha()
ship_image = pygame.transform.smoothscale(ship_image,(ship_width,ship_height))
ufo_image = pygame.image.load(project_path+"/images/ufo.png").convert_alpha()
ufo_image = pygame.transform.smoothscale(ufo_image,(ufo_width,ufo_height))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                shipv=-3
            if event.key == pygame.K_RIGHT:
                shipv= 3
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
        if number_of_empty_balls == 0:                                                      #number_of_empty_balls limits the amount of balls released by holding space
            cannonball = [shipx+ship_width/2,shipy,list_of_colors[color_id]]
            color_id = (color_id +1) % len(list_of_colors)
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
        pygame.draw.circle(screen, ball[2],tuple(ball[:2]),ball_radius)

        screen.blit(ball_image,(ball[0]-ball_radius,ball[1]-ball_radius))
        correction = 0                                                  #because delete shortens the list->may cause index out of range

        for index,ufo in enumerate(list_of_ufos[:]):
            if ufo[1] + ufo_height >= ball[1] - ball_radius:
                if ufo[0]>ball[0]-ball_radius and  ufo[0] < ball[0]+ball_radius or ufo[0]<ball[0] -ball_radius and ufo[0] + ufo_width >= ball[0]-ball_radius:
                    del list_of_ufos[index-correction]
                    correction +=1
                

    if frame_count % int(100-spawn_speed)== 0:
        spawn_speed += 5 - (5*spawn_speed/99)
        print (spawn_speed)
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
    ufo_speed += 0.001
 
pygame.quit()