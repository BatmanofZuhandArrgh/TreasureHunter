import os
import sys
import numpy as np
import pygame
from pygame import mouse
from pygame.locals import *

from bot import Q_learning_AI, temp

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
        # divider:int = 20,
        divider:int = 5,
        
        icon_image_path:str = 'assets/icons8-batman-48.png', 
        bot_type = 'temp'
        ):
        
        if(width % divider != 0):
            width -= width%divider
        
        self.divider = divider
        self.width = width
        self.size = (width, width)
        self.empty_surface = None
        self.screen = None

        self.blockSize = int(width // divider)

        self.screen_representation = np.zeros(((divider, divider)))
        self.screen_full = np.zeros((self.size))
        
        #Player position
        self.icon = pygame.image.load(icon_image_path)
        self.position = (0,0)
        self.score = 100

        #Bot
        self.bot = None
        self.bot_type = bot_type
        self.bot_infer_path = None

    def get_bot(self):
        if(self.bot_type == 'temp'):
            self.bot = temp(reward_matrix = self.screen_representation)
        elif(self.bot_type == 'Q_learning_AI'):
            self.bot = Q_learning_AI(reward_matrix = self.screen_representation)

    def show_surface(self):
        self.empty_surface = pygame.Surface(self.size)
        return self.empty_surface

    def drawGrid(self):
        # Draw lines in grid
        for x in range(0, self.width, self.blockSize):
            for y in range(0, self.width, self.blockSize):
                rect = pygame.Rect(x, y, self.blockSize, self.blockSize)
                pygame.draw.rect(self.screen, WHITE, rect, 1)
        
        # Paint grid box
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
        rep_width_index, rep_height_index =   rep_height_index,rep_width_index
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
        
        
    def game_init(self, player = 'bot'):
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

        design_mode = True 

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                elif event.type == MOUSEMOTION and design_mode == True:
                    if (drawing): 
                        mouse_position = pygame.mouse.get_pos()
                        mouse_position = (mouse_position[-1],mouse_position[0])
                        self.changeScreenRep(mouse_position, cell_type)

                elif event.type == MOUSEBUTTONUP and design_mode == True:
                    mouse_position = (-1, -1)
                    drawing = False

                elif event.type == MOUSEBUTTONDOWN and design_mode == True:
                    drawing = True
                    mouse_position = pygame.mouse.get_pos()
                    mouse_position = (mouse_position[-1],mouse_position[0])
                    self.changeScreenRep(mouse_position, cell_type)

                elif event.type == KEYDOWN:
                    if event.key == pygame.K_q:
                        #Quit
                        pygame.quit()
                        sys.exit()    

                    elif event.key == pygame.K_SPACE and text != self.TEXT_PHASE[-1] and text in self.TEXT_PHASE and design_mode == True:
                        # Programming the next phase in design mode
                        text = self.TEXT_PHASE[self.TEXT_PHASE.index(text)+1]
                        text_surface = font.render(text, True, WHITE)
                        cell_type = INDEX_DICT[self.TEXT_PHASE.index(text)]

                    elif text == self.TEXT_PHASE[-1] or 'Score' in text:
                        # Controls for player
                        design_mode = False #Shut off design mode
                        mouse_position = (-1,-1)
                        if(player == 'human'):
                            if(event.key == pygame.K_UP):
                                self.position = (max(self.position[0] - 1, 0), self.position[1])
                            elif(event.key == pygame.K_DOWN):
                                self.position = (min(self.position[0] + 1, self.divider-1), self.position[1])
                            elif(event.key == pygame.K_LEFT):
                                self.position = (self.position[0], max(0, self.position[1]-1))
                            elif(event.key == pygame.K_RIGHT):
                                self.position = (self.position[0], min(self.position[1] + 1, self.divider-1))
                                
                        elif(player == 'bot'):
                            if (self.bot == None):
                                #If bot is not created, create bot and train bot and infer path
                                self.get_bot()

                                self.bot.train()
                    
                                self.bot_infer_path = self.bot.run(self.position)

                                path_index = 0
                                                        
                            #Moving a bot
                            if(self.bot_infer_path[path_index] == 'up'):
                                self.position = (max(self.position[0] - 1, 0), self.position[1])
                            elif(self.bot_infer_path[path_index] == 'down'):
                                self.position = (min(self.position[0] + 1, self.divider-1), self.position[1])
                            elif(self.bot_infer_path[path_index] == 'left'):
                                self.position = (self.position[0], max(0, self.position[1]-1))
                            elif(self.bot_infer_path[path_index] == 'right'):
                                self.position = (self.position[0], min(self.position[1] + 1, self.divider-1))
                            path_index += 1

                            if(path_index == len(self.bot_infer_path)):
                                raise IndexError("Bot inferred path does not finish the game")

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
        
            self.screen.blit(self.icon, (self.position[1] * self.blockSize, self.position[0] *  self.blockSize))
            self.screen.blit(text_surface, (0,0))

            pygame.display.update()

if __name__ == "__main__":
    main_game = Adventure()

    main_game.game_init()