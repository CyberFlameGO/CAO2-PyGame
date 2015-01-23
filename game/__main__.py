'''
Created on 12 jan. 2015

@author: Sjoerd
'''

#import libraries
import os
import sys
import pygame

from game.classes.game import Game
    
def main(argv=sys.argv):
    
    file_path = sys.argv[1] if len(sys.argv) > 1 else ''
    map_name = sys.argv[2] if len(sys.argv) > 1 else 2
    
    # Initialise pygame
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    
    pygame.init()

    #setup screen
    screen = pygame.display.set_mode((1000, 800))
        
    play_game(file_path, map_name, screen)
    
def play_game(file_path, map_name, screen):

    game = Game(file_path, map_name, screen)

    running = True
    game_started  = False
    
    while(running):
        
        if(game_started):
            #running 
            new_game = game.play()
            
            running = new_game
            game_started = False
            
        else:
            # to_do, startup screen
            game.create_map()
            game_started = True

if __name__ == '__main__':
    main()