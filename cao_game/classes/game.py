'''
Created on 11 jan. 2015

@author: Sjoerd
'''

import pygame
import array
from cao_game.classes.ball import Ball
from cao_game.classes.wall import Wall
from cao_game.classes.finish import Finish
from cao_game.classes.hole import Hole
import cao_game

class Game(object):
    
    # Maps
    map = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "WS H      W                                      W",
    "WH        W                                      W",
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
    
    #main objects
    screen = ''

    #Game objects
    walls = []
    finishes = []
    holes = []
    ball = ''
    sprites = []
    clock = ''
    clicked_pos = [0,0]
    
    #Sprites
    sprites = {}

    # Current map
    current_map = 0

    def __init__(self, file_path, set_map, screen):
        
        self.sprites["wall"] = pygame.image.load(file_path + 'images/wall2.png') 
        self.sprites["hole"] = pygame.image.load(file_path + 'images/hole.png')
        #self.sprites[ball] = pygame.image.load(sys.argv[1] + 'images/hbal.png')
        #self.sprites[finish] = pygame.image.load(sys.argv[1] + 'images/hfinish.png')
        self.sprites["background"] = pygame.image.load(file_path + 'images/background2.png')

        #set screen
        self.screen = screen
        
        # Set map
        self.current_map = set_map
        
        # Set clock
        self.clock = pygame.time.Clock()
   
   
    def play(self):
        
        running = True
        
        while(running):
            
            # Stop running
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    running = False
                            
            #check cao_game over
            if self.ball.get_lives() <= 0:
                return False
            
            else :   
                # Game do step
                self.game.game_move()
                
                # Draw new cao_game field
                self.game.draw_play_screen()
                
                # Wait a clock tick
                self.clock.tick(cao_game.main.PROGRAM_SPEED)
   
   
    def getHoles(self):
        return self.holes

    def getWalls(self):
        return self.walls
   
    def create_map(self):
        x = y = 0
        for row in self.map:
            for coll in row:
                if coll == "W" :
                    self.walls.append(Wall((x,y)))
                if coll == "E" :
                    self.finishes.append(Finish((x,y)))
                if coll == "S" :
                    self.ball = Ball((x,y), cao_game.main.HOLE_OVERLAP, self)
                if coll == "H":
                    self.holes.append(Hole((x,y)))
                x+= cao_game.main.OBJECT_SIZE
            y+= cao_game.main.OBJECT_SIZE
            x=0
            
    def game_move(self):
        
        speed_x = self.ball.get_speed()[0]
        speed_y = self.ball.get_speed()[1]
        
        self.clicked_pos = (0,0)
        clicked = False
            
        if pygame.mouse.get_pressed()[0]:
            if not clicked:
                clicked = True
                self.clicked_pos = pygame.mouse.get_pos()
            else:
                xdif = (pygame.mouse.get_pos()[0] - self.clicked_pos[0])
                if (xdif > 0 and xdif > cao_game.main.DEAD_ZONE) or  (xdif < 0 and xdif < cao_game.main.DEAD_ZONE):
                    if xdif < 0:
                        xdif = xdif + cao_game.main.DEAD_ZONE
                    if xdif > 0:
                        xdif = xdif - cao_game.main.DEAD_ZONE
                    speed_x = speed_x + ((xdif) * cao_game.main.PIXEL_SPEED_INC)
                    if speed_x > cao_game.main.MAX_SPEED:
                        speed_x = cao_game.main.MAX_SPEED
                    if speed_x < -cao_game.main.MAX_SPEED:
                        speed_x = -cao_game.main.MAX_SPEED
                ydif = (pygame.mouse.get_pos()[1] - self.clicked_pos[1])
                if (ydif > 0 and ydif > cao_game.main.DEAD_ZONE) or  (ydif < 0 and ydif < cao_game.main.DEAD_ZONE):
                    if ydif < 0:
                        ydif = ydif + cao_game.main.DEAD_ZONE
                    if ydif > 0:
                        ydif = ydif - cao_game.main.DEAD_ZONE
                    speed_y = speed_y + ((ydif) * cao_game.main.PIXEL_SPEED_INC)
                    if speed_y > cao_game.main.MAX_SPEED:
                        speed_y = cao_game.main.MAX_SPEED
                    if speed_y < -cao_game.main.MAX_SPEED:
                        speed_y = -cao_game.main.MAX_SPEED
        else:
            clicked = False
        
        # Get the movement of the ball
        dx = speed_x * (cao_game.main.PROGRAM_SPEED / 500);
        dy = speed_y * (cao_game.main.PROGRAM_SPEED / 500);
        self.ball.set_speed((speed_x, speed_y))
        self.ball.move(dx, dy)
    
    def draw_play_screen(self):
        
        self.screen.fill((0,0,0))
        background_image = self.sprite_background.get_rect()
        self.screen.blit(self.sprite["background"], background_image)
        for wall in self.walls:
            pygame.draw.rect(self.screen, (255, 255, 255), wall.rect)
            self.screen.blit(self.sprite["wall"], wall.rect)  
        for hole in self.holes:
            pygame.draw.rect(self.screen, (255, 255, 255), hole.rect)
            self.screen.blit(self.sprite["hole"], hole.rect)  
        for finish in self.finishes:
            pygame.draw.rect(self.screen, (255, 255, 255), finish.rect)   
        pygame.draw.circle(self.screen, (0, 180, 0), (self.ball.rect.centerx, self.ball.rect.centery), 8)        
        #pygame.draw.rect(screen, (255, 200, 0), ball.rect)
        
        font = pygame.font.Font(None, 20)
        text = font.render("xspeed=" + str(self.bal.get_speed[0]), 1, (0, 0, 0))
        textpos = text.get_rect()
        textpos.left = 820
        textpos.centery = 20
        self.screen.blit(text, textpos)
        text = font.render("yspeed=" + str(self.bal.get_speed[1]), 1, (0, 0, 0))
        textpos = text.get_rect()
        textpos.left = 820
        textpos.centery = 50
        self.screen.blit(text, textpos)
        text = font.render("Lives=" + str(self.ball.get_lives()), 1, (0, 0, 0))
        textpos = text.get_rect()
        textpos.left = 820
        textpos.centery = 80
        self.screen.blit(text, textpos)
        text = font.render("Top:" + str(self.ball.rect.top) + " Left: " + str(self.ball.rect.left), 1, (0, 0, 0))
        textpos = text.get_rect()
        textpos.left = 820
        textpos.centery = 110
        self.screen.blit(text, textpos)
        text = font.render("Bot:" + str(self.ball.rect.bottom) + " Right: " + str(self.ball.rect.right), 1, (0, 0, 0))
        textpos = text.get_rect()
        textpos.left = 820
        textpos.centery = 140
        self.screen.blit(text, textpos)
        
        # Clicked location indicator
        if pygame.mouse.get_pressed()[0]:
            pygame.draw.circle(self.screen, (0, 0, 0), (self.clicked_pos[0], self.clicked_pos[1]), 5)
        
        pygame.display.flip()
        
    
                