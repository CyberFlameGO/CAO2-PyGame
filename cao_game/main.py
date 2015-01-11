'''
Created on 10 jan. 2015

@author: Sjoerd
'''

#import libraries
import os
import sys
import pygame
from cao_game.classes.game import Game

# Constants
OBJECT_SIZE = 16
HOLE_OVERLAP = 12
PROGRAM_SPEED = 60
PIXEL_SPEED_INC = 0.02
MAX_SPEED = 50.0
DEAD_ZONE = 8.0

def main(argv=sys.argv):
    
    file_path = sys.argv[1] if len(sys.argv) > 1 else ''
    map = sys.argv[2] if len(sys.argv) > 1 else 2
    
    # Initialise pygame
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    
    pygame.init()

    #setup screen
    screen = pygame.display.set_mode((1000, 800))
        
    play_game(file_path, map, screen)
    
    
def play_game(file_path, map, screen):

    game = Game(file_path, map, screen)

    running = True
    game_started  = False
    
    while(running):
        
        if(game_started):
            #running cao_game
            game_over = game.play()
            
        else:
            # to_do, startup screen
            game.create_map()
            game_started = True
            
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False

if __name__ == '__main__':
    main()




         
         

