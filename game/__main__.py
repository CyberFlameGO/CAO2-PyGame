'''
Created on 12 jan. 2015

@author: Sjoerd
'''

#import libraries
import os
import sys
import pygame
import time

import game.constants as c
from tkinter.constants import CENTER


class Game(object):
    
    # Maps
    map = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "WS H      W                                      W",
    "WH        W                                  E   W",
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
    start_screen = True

    #Game objects
    walls = []
    finishes = []
    holes = []
    ball = ''
    sprites = []
    clock = ''
    clicked_pos = (0,0)
    clicked = False
    start_time = 0
    end_time = 0
    win = False
    end_lives = 0
    end_win = False
    
    #Sprites
    sprites = {}

    # Current map
    current_map = 0

    def __init__(self, file_path, set_map, screen):
        
        self.sprites["wall"] = pygame.image.load(file_path + 'images/wall2.png') 
        self.sprites["hole"] = pygame.image.load(file_path + 'images/hole.png')
        self.sprites["finish"] = pygame.image.load(file_path + 'images/finish.png')
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
                    return False
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    return False
                if e.type == pygame.KEYDOWN:
                    self.start_time = time.time()
                    self.start_screen = False
                                 
            #check  over
            if self.ball.get_lives() <= 0 or self.win:
                
                self.end_time = int(time.time() - self.start_time)
                self.end_lives = self.ball.get_lives()
                self.end_win = self.win
                return True               
            
            else :   
                # Game do step
                if not self.start_screen:
                    self.game_move()
                
                # Draw new  field
                self.draw_play_screen()
                
                # Wait a clock tick
                self.clock.tick(c.PROGRAM_SPEED)
                
    def getHoles(self):
        return self.holes

    def getWalls(self):
        return self.walls
    
    def getFinishes(self):
        return self.finishes
    
    def setWin(self):
        self.win = True
   
    def create_map(self):
        self.walls = []
        self.finishes = []
        self.holes = []
        self.start_screen = True
        self.win = False
        x = y = 0
        for row in self.map:
            for coll in row:
                if coll == "W" :
                    self.walls.append(Wall((x,y)))
                if coll == "E" :
                    self.finishes.append(Finish((x,y)))
                if coll == "S" :
                    self.ball = Ball((x,y), c.HOLE_OVERLAP, self)
                if coll == "H":
                    self.holes.append(Hole((x,y)))
                x+= c.OBJECT_SIZE
            y+= c.OBJECT_SIZE
            x=0
            
    def game_move(self):
        
        speed_x = self.ball.get_speed()[0]
        speed_y = self.ball.get_speed()[1]
            
        if pygame.mouse.get_pressed()[0]:
            if not self.clicked:
                self.clicked = True
                self.clicked_pos = pygame.mouse.get_pos()
            else:
                xdif = (pygame.mouse.get_pos()[0] - self.clicked_pos[0])
                if (xdif > 0 and xdif > c.DEAD_ZONE) or  (xdif < 0 and xdif < c.DEAD_ZONE):
                    if xdif < 0:
                        xdif = xdif + c.DEAD_ZONE
                    if xdif > 0:
                        xdif = xdif - c.DEAD_ZONE
                    speed_x = speed_x + ((xdif) * c.PIXEL_SPEED_INC)
                    if speed_x > c.MAX_SPEED:
                        speed_x = c.MAX_SPEED
                    if speed_x < -c.MAX_SPEED:
                        speed_x = -c.MAX_SPEED
                ydif = (pygame.mouse.get_pos()[1] - self.clicked_pos[1])
                if (ydif > 0 and ydif > c.DEAD_ZONE) or  (ydif < 0 and ydif < c.DEAD_ZONE):
                    if ydif < 0:
                        ydif = ydif + c.DEAD_ZONE
                    if ydif > 0:
                        ydif = ydif - c.DEAD_ZONE
                    speed_y = speed_y + ((ydif) * c.PIXEL_SPEED_INC)
                    if speed_y > c.MAX_SPEED:
                        speed_y = c.MAX_SPEED
                    if speed_y < -c.MAX_SPEED:
                        speed_y = -c.MAX_SPEED
        else:
            self.clicked = False
        
        # Get the movement of the ball
        dx = speed_x * (c.PROGRAM_SPEED / 500);
        dy = speed_y * (c.PROGRAM_SPEED / 500);
        self.ball.set_speed((speed_x, speed_y))
        self.ball.move(dx, dy)
    
    def draw_play_screen(self):
        
        self.screen.fill((0,0,0))
        background_image = self.sprites["background"].get_rect()
        self.screen.blit(self.sprites["background"], background_image)
        
        if self.start_screen :
            font_startscreen = pygame.font.Font(None, 80)
            text = font_startscreen.render("Press a key to start!", 1, (0, 0, 0))
            textpos = text.get_rect()
            textpos.centery = 400
            textpos.centerx = 500
            self.screen.blit(text, textpos)
            
            if not self.end_time == 0 :
                font_startscreen = pygame.font.Font(None, 50)
                if self.end_win :
                    text = font_startscreen.render("You won!", 1, (0, 255, 0))
                else:
                    text = font_startscreen.render("You failed!", 1, (255, 0, 0))
                textpos = text.get_rect()
                textpos.centery = 200
                textpos.centerx = 500
                self.screen.blit(text, textpos)
                font_startscreen = pygame.font.Font(None, 30)
                text = font_startscreen.render("Time: " + str(self.end_time) + " seconds", 1, (0, 0, 0))
                textpos = text.get_rect()
                textpos.centery = 250
                textpos.centerx = 500
                self.screen.blit(text, textpos)
                text = font_startscreen.render(" Lives: " + str(self.end_lives) , 1, (0, 0, 0))
                textpos = text.get_rect()
                textpos.centery = 290
                textpos.centerx = 500
                self.screen.blit(text, textpos)
                
        else :
            for wall in self.walls:
                self.screen.blit(self.sprites["wall"], wall.rect)  
            for hole in self.holes:
                self.screen.blit(self.sprites["hole"], hole.rect)  
            pygame.draw.circle(self.screen, (0, 180, 0), (self.ball.rect.centerx, self.ball.rect.centery), 8)        
            #pygame.draw.rect(screen, (255, 200, 0), ball.rect)
            
            font = pygame.font.Font(None, 20)
            text = font.render("xspeed=" + str(self.ball.get_speed()[0]), 1, (0, 0, 0))
            textpos = text.get_rect()
            textpos.left = 820
            textpos.centery = 20
            self.screen.blit(text, textpos)
            text = font.render("yspeed=" + str(self.ball.get_speed()[1]), 1, (0, 0, 0))
            textpos = text.get_rect()
            textpos.left = 820
            textpos.centery = 50
            self.screen.blit(text, textpos)
            text = font.render("Lives=" + str(self.ball.get_lives()), 1, (0, 0, 0))
            textpos = text.get_rect()
            textpos.left = 820
            textpos.centery = 80
            self.screen.blit(text, textpos)
            play_time = int(time.time() - self.start_time);
            text = font.render("Time =" + str(play_time), 1, (0, 0, 0))
            textpos = text.get_rect()
            textpos.left = 820
            textpos.centery = 110
            self.screen.blit(text, textpos)
            
            for finish in self.finishes:
                draw_finish = finish.rect.copy()
                draw_finish.centery = draw_finish.centery - 16
                self.screen.blit(self.sprites["finish"], draw_finish)  
            
            # Clicked location indicator
            if pygame.mouse.get_pressed()[0]:
                pygame.draw.circle(self.screen, (0, 0, 0), (self.clicked_pos[0], self.clicked_pos[1]), 5)
            
        pygame.display.flip()

class Wall(object):
    
    def __init__(self, position):
        self.rect = pygame.Rect(position[0], position[1], c.OBJECT_SIZE, c.OBJECT_SIZE)
 

class Hole(object):
    
    def __init__(self, position):
        self.rect = pygame.Rect(position[0], position[1], c.OBJECT_SIZE, c.OBJECT_SIZE)
    

class Finish(object):
    
    def __init__(self, position):
        self.rect = pygame.Rect(position[0], position[1],c.OBJECT_SIZE, c.OBJECT_SIZE)

class Ball(object):
    
    #game object
    game = ''
    
    #ball objects
    start_position = [0.0, 0.0]     # Start position from the map
    ball_position = [16.0, 16.0]    # Ball position when started
    speed_x = 1.0
    speed_y = 0.0
    lives = 3
    lives_down_set = False
    hole_overlap = 12
        
    def __init__(self, position, hole_overlap, game):
        self.ball_position[0] = position[0]
        self.ball_position[1] = position[1]
        self.start_position[0] = position[0]
        self.start_position[1] = position[1]
        self.lives = 3
        self.lives_down_set = False
        self.rect = pygame.Rect(position[0], position[1], c.OBJECT_SIZE, c.OBJECT_SIZE)
        self.hole_overlap = hole_overlap
        self.game = game
        
    def move(self, x, y):
        if (x != 0):
            self.move_axis(x, 0)
        if (y !=0):
            self.move_axis(0, y)
    
    def move_axis(self, x, y):
        
        self.ball_position[0]+= x
        self.ball_position[1]+= y 
        
        # USe float coordinates
        self.rect.x = round(self.ball_position[0])
        self.rect.y = round(self.ball_position[1])
        
        for wall in self.game.getWalls():
            if self.rect.colliderect(wall.rect):
                if x > 0:
                    self.rect.right = wall.rect.left
                    self.ball_position[0] = self.rect.left
                if x < 0: 
                    self.rect.left = wall.rect.right
                    self.ball_position[0] = self.rect.left
                if y > 0: 
                    self.rect.bottom = wall.rect.top
                    self.ball_position[1] = self.rect.top
                if y < 0:
                    self.rect.top = wall.rect.bottom
                    self.ball_position[1] = self.rect.top  
        
        # Check for holes
        for hole in self.game.getHoles():
            if self.rect.right > (hole.rect.left + self.hole_overlap) and self.rect.left < (hole.rect.right - self.hole_overlap) and self.rect.top < (hole.rect.bottom - self.hole_overlap) and self.rect.bottom > (hole.rect.top + self.hole_overlap):
                self.lives_down()
        
        for finish in self.game.getFinishes():
            if self.rect.right > (finish.rect.left + self.hole_overlap) and self.rect.left < (finish.rect.right - self.hole_overlap) and self.rect.top < (finish.rect.bottom - self.hole_overlap) and self.rect.bottom > (finish.rect.top + self.hole_overlap):
                self.game.setWin()
    
    def lives_down(self):
        self.lives-=1
        self.ball_position[0] = self.start_position[0]
        self.ball_position[1] = self.start_position[1]
        self.speed_x = 0
        self.speed_y = 0

    
    def set_speed(self, speed):
        self.speed_x = speed[0]
        self.speed_y = speed[1]
    
    def get_speed(self):
        return [self.speed_x, self.speed_y]
    
    def set_live(self, lives):
        self.lives = lives
    
    def get_lives(self):
        return self.lives
    
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