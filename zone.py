import os
import sys
import numpy as np
import pygame
from pygame.locals import *

WHITE = (255, 255, 255)
NAVY_BLUE = (0,0,128)
BLACK = (0, 0, 0)

class Surface:
    def __init__(self, 
        width: int = 1000,
        divider:int = 20,
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

    def show_surface(self):
        self.empty_surface = pygame.Surface(self.size)
        return self.empty_surface

    def drawGrid(self):
        for x in range(0, self.width, self.blockSize):
            for y in range(0, self.width, self.blockSize):
                rect = pygame.Rect(x, y, self.blockSize, self.blockSize)
                pygame.draw.rect(self.screen, WHITE, rect, 1)
    
    def paintGridBox(self, mouse_position):
        rep_width_index, rep_height_index = mouse_position[0]//self.blockSize, mouse_position[1]//self.blockSize

        # self.screen_representation[rep_width_index][rep_height_index] = 1
        
        for x in range(rep_width_index*self.blockSize, (rep_width_index+1)*self.blockSize):
            for y in range(rep_height_index*self.blockSize, (rep_height_index+1)*self.blockSize):
                pygame.draw.circle(self.screen, WHITE, (x,y), 1)

    def game_init(self):
        pygame.init()

        mouse_position = (0, 0)
        drawing = False

        self.screen = pygame.display.set_mode(self.size)
        done = False
        self.screen.fill(BLACK)

        last_pos = None
        while not done:
            self.drawGrid()            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEMOTION:
                    if (drawing): 
                        mouse_position = pygame.mouse.get_pos()
                        self.paintGridBox(mouse_position)

                elif event.type == MOUSEBUTTONUP:
                    mouse_position = (0, 0)
                    drawing = False

                elif event.type == MOUSEBUTTONDOWN:
                    drawing = True
                    mouse_position = pygame.mouse.get_pos()
                    self.paintGridBox(mouse_position)

                elif event.type == KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()    

            pygame.display.update()



if __name__ == "__main__":
    surface = Surface()

    surface.game_init()