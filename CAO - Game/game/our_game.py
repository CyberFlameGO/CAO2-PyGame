'''
Created on 10 jan. 2015

@author: Sjoerd
'''

#Import pygame_quit
import os

import pygame


# Constants
OBJECT_SIZE = 16
PROGRAM_SPEED = 60
PIXEL_SPEED_INC = 0.02
MAX_SPEED = 50.0
DEAD_ZONE = 8.0
                
#Map objects
walls = []
finishes = []
holes = []

level = [
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
"WS        W                                      W",
"W         W                                      W",
"WWWWWWWW  WWWWW                                  W",
"W         W                                      W",
"W H       W                                      W",
"W         W                                      W",
"W         W                                      W",
"W         W                                      W",
"W    H    W                                      W",
"W         W                                      W",
"W         W                                      W",
"W         W                                      W",
"W  WWWWWWWW  WWWWW                               W",
"W        W      HW                               W",
"W        W       WWWWW                           W",
"WWWWWWW  W  H        W                           W",
"W        W           W                           W",
"W        WWWWWWWW    W                           W",
"W  WWWW  W      WWW  W                           W",
"W  W     W      W    W                           W",
"W  W     W  W   W    W                           W",
"W  W   WWW  W   W  WWW                           W",
"W  W        W   W    W                           W",
"W  W        W   W    W                           W",
"W  WWWWWWWWWW   WWW  W                           W",
"W                    W                           W",
"W                    W                           W",
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW                 W",
"W                                                W",
"W                                                W",
"W                                                W",
"W                                                W",
"W                                                W",
"W                                                W",
"W                                                W",
"W                                                W",
"W                                                W",
"W                                                W",
"W                                                W",
"W                                                W",
"W                                                W",
"W                                                W",
"W                                                W",
"W                                                W",
"W                                                W",
"W                                                W",
"W                                                W",
"W                                                W",
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
]

# Initialise pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()
clock = pygame.time.Clock()

#Create the ball
ball_position = [16.0, 16.0]
speed_x = 5.0
speed_y = -10.0

# Sprites
sprite_wall = pygame.image.load('wall2.png') 
sprite_hole = pygame.image.load('hole.png')
#sprite_ball = pygame.image.load('bal.png')
#sprite_finish = pygame.image.load('finish.png')
sprite_background = pygame.image.load('background2.png')

# Input
clicked_pos = (0,0)
clicked = False

class Ball(object):
    
    def __init__(self, position):
        ball_position[0] = position[0]
        ball_position[1] = position[1]
        self.rect = pygame.Rect(position[0], position[1], OBJECT_SIZE, OBJECT_SIZE)
        
    def move(self, x, y):
        if (x != 0):
            self.move_axis(x, 0)
        if (y !=0):
            self.move_axis(0, y)
    
    def move_axis(self, x, y):
        
        ball_position[0]+= x
        ball_position[1]+= y 
        
        # USe float coordinates
        self.rect.x = round(ball_position[0])
        self.rect.y = round(ball_position[1])
        
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if x > 0:
                    self.rect.right = wall.rect.left
                    ball_position[0] = self.rect.left
                if x < 0: 
                    self.rect.left = wall.rect.right
                    ball_position[0] = self.rect.left
                if y > 0: 
                    self.rect.bottom = wall.rect.top
                    ball_position[1] = self.rect.top
                if y < 0:
                    self.rect.top = wall.rect.bottom
                    ball_position[1] = self.rect.top

       
        # Check for holes
        
class Wall(object):
    
    def __init__(self, position):
        walls.append(self)
        self.rect = pygame.Rect(position[0], position[1], OBJECT_SIZE, OBJECT_SIZE)
    
class Finish(object):
    
    def __init__(self, position):
        finishes.append(self)
        self.rect = pygame.Rect(position[0], position[1], OBJECT_SIZE, OBJECT_SIZE)

class Hole(object):
    
    def __init__(self, position):
        holes.append(self)
        self.rect = pygame.Rect(position[0], position[1], OBJECT_SIZE, OBJECT_SIZE)


#Set up display
screen = pygame.display.set_mode((1000, 800))

#Create level
x = y = 0
for row in level:
    for coll in row:
        if coll == "W" :
            Wall((x,y))
        if coll == "E" :
            Finish((x,y))
        if coll == "S" :
            ball = Ball((x,y))
        if coll == "H":
            Hole((x,y))
        x+= OBJECT_SIZE
    y+= OBJECT_SIZE
    x=0

running = True

while running:
    
    clock.tick(PROGRAM_SPEED)
    
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False
    
    # Do something with input
    if pygame.mouse.get_pressed()[0]:
        if not clicked:
            clicked = True
            clicked_pos = pygame.mouse.get_pos()
        else:
            xdif = (pygame.mouse.get_pos()[0] - clicked_pos[0])
            if (xdif > 0 and xdif > DEAD_ZONE) or  (xdif < 0 and xdif < DEAD_ZONE):
                if xdif < 0:
                    xdif = xdif + DEAD_ZONE
                if xdif > 0:
                    xdif = xdif - DEAD_ZONE
                speed_x = speed_x + ((xdif) * PIXEL_SPEED_INC)
                if speed_x > MAX_SPEED:
                    speed_x = MAX_SPEED
                if speed_x < -MAX_SPEED:
                    speed_x = -MAX_SPEED
            ydif = (pygame.mouse.get_pos()[1] - clicked_pos[1])
            if (ydif > 0 and ydif > DEAD_ZONE) or  (ydif < 0 and ydif < DEAD_ZONE):
                if ydif < 0:
                    ydif = ydif + DEAD_ZONE
                if ydif > 0:
                    ydif = ydif - DEAD_ZONE
                speed_y = speed_y + ((ydif) * PIXEL_SPEED_INC)
                if speed_y > MAX_SPEED:
                    speed_y = MAX_SPEED
                if speed_y < -MAX_SPEED:
                    speed_y = -MAX_SPEED
    else:
        clicked = False
        
    # Get the movement of the ball
    dx = speed_x * (PROGRAM_SPEED / 1000);
    dy = speed_y * (PROGRAM_SPEED / 1000);
    ball.move(dx, dy)
    

    #Fill level
    screen.fill((0,0,0))
    background_image = sprite_background.get_rect()
    screen.blit(sprite_background, background_image)
    for wall in walls:
        pygame.draw.rect(screen, (255, 255, 255), wall.rect)
        screen.blit(sprite_wall, wall.rect)  
    for hole in holes:
        pygame.draw.rect(screen, (255, 255, 255), hole.rect)
        screen.blit(sprite_hole, hole.rect)  
    for finish in finishes:
        pygame.draw.rect(screen, (255, 255, 255), finish.rect)   
    pygame.draw.circle(screen, (0, 180, 0), (ball.rect.centerx, ball.rect.centery), 8)        
    #pygame.draw.rect(screen, (255, 200, 0), ball.rect)
    
    font = pygame.font.Font(None, 20)
    text = font.render("xspeed=" + str(speed_x), 1, (0, 0, 0))
    textpos = text.get_rect()
    textpos.left = 820
    textpos.centery = 20
    screen.blit(text, textpos)
    text = font.render("yspeed=" + str(speed_y), 1, (0, 0, 0))
    textpos = text.get_rect()
    textpos.left = 820
    textpos.centery = 50
    screen.blit(text, textpos)
    
    # Clicked location indicator
    if pygame.mouse.get_pressed()[0]:
        pygame.draw.circle(screen, (0, 0, 0), (clicked_pos[0], clicked_pos[1]), 5)
    
    pygame.display.flip()






         
         

