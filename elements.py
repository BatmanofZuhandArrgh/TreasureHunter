from lib2to3 import pygram
import os
import sys
import numpy as np
import pygame
from pygame import mouse
from pygame.locals import *

from search_bot import breadth_first_tree_search
from reinforcement_ai import Q_learning_AI, temp

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
        self.bot_type = None
        self.bot_infer_path = None

    def get_bot(self):
        print('Create bot')
        if(self.bot_type == 'temp'):
            self.bot = temp(reward_matrix = self.screen_representation)
        elif(self.bot_type == 'Q_learning_AI'):
            self.bot = Q_learning_AI(reward_matrix = self.screen_representation)
        elif(self.bot_type == 'breadth_first_tree_search'):
            self.bot = breadth_first_tree_search(position = self.position)
        else:
            raise(ValueError("Bot type not found"))

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
        
    def get_surrounding(self, leaf_node):
        position = leaf_node.position
        parent_position = leaf_node.parent.position

        surroundings = []
        for i in range(-1,2):
            for j in range(-1,2):
                x = position[0]+i
                y = position[1]+j
                if x >= 0 and y >= 0 and x <= len(self.screen_representation)-1 and y <= len(self.screen_representation)-1:
                    surroundings.append((x, y))

        # Remove parent position, so that the path won't return to its parent
        if parent_position != (-1,-1):
            surroundings.remove(parent_position)
        surroundings.remove(position)

        return surroundings

    def game_init(self, player = 'bot', bot_type = 'temp'):
        self.bot_type = bot_type
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

        cell_type = base_cell

        design_mode = True 

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                elif event.type == MOUSEMOTION and design_mode:
                    if (drawing): 
                        mouse_position = pygame.mouse.get_pos()
                        mouse_position = (mouse_position[-1],mouse_position[0])
                        self.changeScreenRep(mouse_position, cell_type)

                elif event.type == MOUSEBUTTONUP and design_mode:
                    mouse_position = (-1, -1)
                    drawing = False

                elif event.type == MOUSEBUTTONDOWN and design_mode:
                    drawing = True
                    mouse_position = pygame.mouse.get_pos()
                    mouse_position = (mouse_position[-1],mouse_position[0])
                    self.changeScreenRep(mouse_position, cell_type)

                elif event.type == KEYDOWN:
                    if event.key in  (pygame.K_q,pygame.K_ESCAPE):
                        #Quit
                        pygame.quit()
                        sys.exit()    

                    elif event.key == pygame.K_SPACE and text != self.TEXT_PHASE[-1] and text in self.TEXT_PHASE and design_mode:
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
                        elif player == "bot":
                            break

                        self.gain_or_lose_score()

                        text = f'Score: {self.score}'
                        text_surface = font.render(text, True, WHITE)
                        
            self.screen.fill(BLACK)
            self.drawGrid()   

            if(player == 'bot') and design_mode == False:
                if (self.bot == None):
                    #If bot is not created, create bot and train bot and infer path
                    self.get_bot()

                    text = f'Score: {self.score}'
                    text_surface = font.render(text, True, WHITE)

                if 'tree_search' in self.bot_type:
                    outer_leaves = self.bot.outer_leaves
                    fringe_positions = [x.position for x in outer_leaves]
                    print(fringe_positions)
                    fringe = []
                    for leaf in outer_leaves:
                        fringe.append(self.get_surrounding(leaf))
                    paths2draw = self.bot.query_surrounding(fringe)
                    
                    for path in paths2draw:
                        # Drawing paths
                        # print(path)
                        start_point = (25+path[0][0]*50,25+path[0][1]*50)
                        end_point = (25+path[1][0]*50,25+path[1][1]*50)
                        pygame.draw.line(self.screen, (255,255,255), start_pos=start_point, end_pos=end_point, width= 10)
                        pygame.draw.circle(self.screen, color=(255,0,0),center=start_point, radius = 5)
                        # pygame.draw.circle(self.screen, color=(255,0,0),center=end_point, radius = 5)
    
                    print('-------------------------')
                    pygame.time.delay(1000)

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