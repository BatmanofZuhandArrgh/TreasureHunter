import os
import sys
import numpy as np
import pygame
from pygame import mouse
from pygame.locals import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class base_cell:
    color = (0,0,0)
    index = 0
    change_score = 0

class lava(base_cell):
    #Slowly hurts player if walked on
    color = (180,41,33)
    index = 1
    change_score = -100

class water(base_cell): 
    #Severely hurts player if walked on
    color = (0,0,205)
    index = 2
    change_score = -5

class escape_door(base_cell):
    #Finish game
    color = (0,220,0)
    index = 3
    change_score = 0

INDEX_DICT = {
    0: base_cell,
    1: lava,
    2: water,
    3: escape_door,
}

class Adventure:
    TEXT_PHASE = [
        "Designing phase:   Press q to quit, spacebar to continue",
        "Locating lava",
        "Locating water",
        "Locating escape door",
    ]

    def __init__(self, 
        width: int = 1000,
        divider:int = 20,
        icon_image_path:str = 'assets/icons8-batman-48.png', 
        ):
        
        if(width % divider != 0):
            width -= width%divider
        
        self.width = width
        self.size = (width, width)
        self.empty_surface = None
        self.screen = None

        self.blockSize = int(width // divider)

        self.screen_representation = np.zeros(((self.blockSize, self.blockSize)))
        self.screen_full = np.zeros((self.size))
        
        #Player position
        self.icon = pygame.image.load(icon_image_path)
        self.position = (0,0)
        self.score = 100

    def show_surface(self):
        self.empty_surface = pygame.Surface(self.size)
        return self.empty_surface

    def drawGrid(self):
        for x in range(0, self.width, self.blockSize):
            for y in range(0, self.width, self.blockSize):
                rect = pygame.Rect(x, y, self.blockSize, self.blockSize)
                pygame.draw.rect(self.screen, WHITE, rect, 1)
            
        for i in range(len(self.screen_representation)):
            for j in range(len(self.screen_representation)):
                if self.screen_representation[i][j] != 0:
                    self.paintGridBox(i, j, INDEX_DICT[self.screen_representation[i][j]])
    
    def changeScreenRep(self, mouse_position, cell_type):
        #Changing a specific index number in the screen representation, to signal the gridbox to change color
        rep_width_index, rep_height_index = mouse_position[0]//self.blockSize, mouse_position[1]//self.blockSize

        self.screen_representation[rep_width_index][rep_height_index] = cell_type.index
            
    def paintGridBox(self, rep_width_index, rep_height_index, cell_type):
        #Painting inside gridbox, either lava, spikes or exit_door
        
        for x in range(rep_width_index*self.blockSize, (rep_width_index+1)*self.blockSize):
            for y in range(rep_height_index*self.blockSize, (rep_height_index+1)*self.blockSize):
                pygame.draw.circle(self.screen, cell_type.color, (x,y), 1)

    def check_win_condition(self):
        if(3 not in self.screen_representation):
            return False
        
        if(self.screen_representation[self.position[0], self.position[1]] == 3):
            return True
    
    def check_loss_condition(self):
        if self.score < 0:
            return True
        return False

    def gain_or_lose_score(self):
        self.score += INDEX_DICT[self.screen_representation[self.position[0], self.position[1]]].change_score

    def game_init(self):
        pygame.init()

        mouse_position = (-1, -1)
        drawing = False

        self.screen = pygame.display.set_mode(self.size)
        font = pygame.font.SysFont('Comic Sans MS', 30)

        done = False
        self.screen.fill(BLACK)
        
        text = self.TEXT_PHASE[0]
        text_surface = font.render(text, True, WHITE)
        self.screen.blit(text_surface, dest=(0,0))

        cell_type = lava

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                elif event.type == MOUSEMOTION:
                    if (drawing): 
                        mouse_position = pygame.mouse.get_pos()
                        self.changeScreenRep(mouse_position, cell_type)

                elif event.type == MOUSEBUTTONUP:
                    mouse_position = (-1, -1)
                    drawing = False

                elif event.type == MOUSEBUTTONDOWN:
                    drawing = True
                    mouse_position = pygame.mouse.get_pos()
                    self.changeScreenRep(mouse_position, cell_type)

                elif event.type == KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()    
                    elif event.key == pygame.K_SPACE and text != self.TEXT_PHASE[-1] and text in self.TEXT_PHASE:
                        text = self.TEXT_PHASE[self.TEXT_PHASE.index(text)+1]
                        text_surface = font.render(text, True, WHITE)
                        cell_type = INDEX_DICT[self.TEXT_PHASE.index(text)]
                    elif text == self.TEXT_PHASE[-1] or 'Score' in text:
                        mouse_position = (-1,-1)
                        if(event.key == pygame.K_UP):
                            self.position = (self.position[0], max(0, self.position[1]-1))
                        elif(event.key == pygame.K_DOWN):
                            self.position = (self.position[0], min(self.position[1] + 1, self.width))
                        elif(event.key == pygame.K_LEFT):
                            self.position = (max(self.position[0] - 1, 0), self.position[1])
                        elif(event.key == pygame.K_RIGHT):
                            self.position = (min(self.position[0] + 1, self.width), self.position[1])

                        self.gain_or_lose_score()

                        text = f'Score: {self.score}'
                        text_surface = font.render(text, True, WHITE)
                        

            self.screen.fill(BLACK)
            self.drawGrid()        

            if(self.check_win_condition()):
                text = 'You won'
                text_surface = font.render(text, True, (0,255,0))
            
            if(self.check_loss_condition()):
                text = 'You lost'
                text_surface = font.render(text, True, (255,0,0))
             
            self.screen.blit(self.icon, (self.position[0] * self.blockSize, self.position[1] *  self.blockSize))
            self.screen.blit(text_surface, (0,0))

            pygame.display.update()


if __name__ == "__main__":
    main_game = Adventure()

    main_game.game_init()