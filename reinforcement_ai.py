import numpy as np
import random

from bot import Bot

class Reinforcement_AI(Bot):
    def __init__(self):
        super(Bot, self).__init__()
        pass
    def train(self):
        pass

    def run(self):
        pass

class temp(Bot):
    def __init__(self, reward_matrix):
        super(temp, self).__init__(reward_matrix=reward_matrix)
        
    def train(self, position):
        print('train')

    def run(self):
        print('run')
        return ['right', 'down']*15


class Q_learning_AI(Bot):
    def __init__(
        self, 
        reward_matrix,
        discount_rate = 0.9,
        ):
        super(Q_learning_AI, self).__init__(reward_matrix)
        self.width = self.reward_matrix.shape[0]
        self.Q_table = np.zeros((len(self.action),) + self.reward_matrix.shape, dtype=np.uint8)

        self.discount_rate = discount_rate 

        self.position = None
        self.score = None

    def get_starting_position(self, type = 'normal'):
        self.score = 100
        if(type == 'normal'):
            self.position = (0,0)

        elif(type == 'random'):
            i = random.randint(0, self.reward_matrix.shape[0]) 
            j = random.randint(0, self.reward_matrix.shape[1]) 

            self.position = (i, j)
    
    def is_terminal_state(self):
        if(self.score < 0 or self.score > 200):
            return True
        return False

    def get_next_action(self, epsilon):
        rand = random.random()
        print(rand)
        if rand >= epsilon:
            print('Explore...', )
            return random.randint(0,3)
        elif rand < epsilon:
            print('Exploit...')
            return np.argmax(self.Q_table[self.position[0], self.position[1]])
    
    def get_next_location(self, action):
        if(action == 3): #up
            self.position = (max(self.position[0] - 1, 0), self.position[1])
        elif(action == 2): #down
            self.position = (min(self.position[0] + 1, self.width), self.position[1])
        elif(action == 0): #left
            self.position = (self.position[0], max(0, self.position[1]-1))
        elif(action == 1): #right
            self.position = (self.position[0], min(self.position[1] + 1, self.width))
                
    def train(
        self,
        num_epoch = 1000, 
        learning_rate = 0.9,
        epsilon = 0.2, # rate of how often the bot will explore instead of exploit
        ):

        for epoch in range(num_epoch):
            #Starting position
            self.get_starting_position()
            
            while not self.is_terminal_state():
                
                #Deciding direction to move
                action = self.get_next_action(epsilon) # from 0 to 3
                print('action', self.action[action])
                
                #Current position
                old_position = self.position

                #Move self.position to new_position
                self.get_next_location(action)
                print('position', self.position)
                temp_reward_matrix = self.reward_matrix
                # temp_reward_matrix[self.position[0], self.position[1]] = 0
                print(temp_reward_matrix)

                #Current position
                new_position = self.position

                reward = self.reward_matrix[new_position[0],new_position[1]]

                old_q_value = self.Q_table[old_position[0], old_position[1], action]

                temporal_difference = reward + (self.discount_rate * np.max(self.Q_table[new_position[0], new_position[1]])) - old_q_value
                #update the Q-value for the previous state and action pair
                new_q_value = old_q_value + (learning_rate * temporal_difference)
                self.Q_table[action, old_position[0], old_position[1]] = new_q_value
                print(self.Q_table)

    def run(self, position):
        actions = []
        self.position = position # Set position for bot in the game
            
        while not self.is_terminal_state():
            action_index = np.argmax(self.Q_table[self.position[0], self.position[1]]) #Full exploitation
            
            self.get_next_location()
            actions.append(self.action[action_index])

        return actions

def main():
    reward_matrix = np.zeros((10,10))
    reward_matrix = np.array([
        [1,-1,-2,-5,1],
        [-4,-1,-2,-5,-10],
        [-3,-5,-5,-5,3],
        [2,3,5,-200,9],
        [9,1,2,-5,200]
    ])

    print(reward_matrix)
    q = Q_learning_AI(reward_matrix)
    q.train()

if __name__ == "__main__":
    main()

    