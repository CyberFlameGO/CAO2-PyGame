'''
Created on 23 jan. 2015

@author: Sjoerd
'''
import pygame
import game.constants as c

class Hole(object):
    
    def __init__(self, position):
        self.rect = pygame.Rect(position[0], position[1], c.OBJECT_SIZE, c.OBJECT_SIZE)
    
