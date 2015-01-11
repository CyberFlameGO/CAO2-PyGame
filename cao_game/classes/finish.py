'''
Created on 11 jan. 2015

@author: Sjoerd
'''


class Finish(object):
    
    def __init__(self, position):
        self.rect = pygame.Rect(position[0], position[1], OBJECT_SIZE, OBJECT_SIZE)
        return self
