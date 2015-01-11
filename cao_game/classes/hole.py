'''
Created on 11 jan. 2015

@author: Sjoerd
'''
import pygame
from cao_game import main

class Hole(object):
    
    def __init__(self, position):
        self.rect = pygame.Rect(position[0], position[1], main.OBJECT_SIZE, main.OBJECT_SIZE)
        return self

