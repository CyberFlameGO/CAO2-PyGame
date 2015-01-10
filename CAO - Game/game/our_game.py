'''
Created on 10 jan. 2015

@author: Sjoerd
'''

#Import pygame_quit
import pygame
import os
import math
import array
from tkinter.tix import Balloon

# Constants
OBJECT_SIZE = 8
                
#Map objects
walls = []
finishes = []
holes = []

# Sprites
sprite_wall = pygame.image.load('wall.png') 
sprite_empty = pygame.image.load('empty.png')
sprite_hole = pygame.image.load('hole.png')
sprite_ball = pygame.image.load('bal.png')
sprite_finish = pygame.image.load('finish.png')

# Initialise pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

#Set up display
screen = pygame.display.set_mode((640, 480))

#Create the ball
ball = Ball()
ball_position = array('d', [16.0, 16.0])


class Ball(object):
    
    def __init__(selfs):
        self.rect = pygame.Rect(START_POSITION[0], START_POSITION[1])
        
    def move(self, x, y):
        if (x != 0):
            self.move_axis(self, x, 0)
        if (y !=0):
            self.move_axis(self, 0, y)
    
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
                    ball_position[0] = self.rect.top
                if y < 0:
                    self.rect.top = wall.rect.bottom
                    ball_position[0] = self.rect.top

       
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


