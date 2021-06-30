import numpy as np
import random
from tqdm import tqdm

STARTING_SCORE = 100

class Reinforcement_AI:
    def __init__(self, reward_matrix):
        self.action = [
            'left',
            'right',
            'down',
            'up'
        ]
        self.reward_matrix = reward_matrix
        self.score = STARTING_SCORE
    def train():
        pass

    def run():
        pass

class temp(Reinforcement_AI):
    def __init__(self, reward_matrix):
        super(temp, self).__init__(reward_matrix=reward_matrix)
        
    def train(self):
        print('train')

    def run(self):
        print('run')
        return ['right', 'down']*15


class Q_learning_AI(Reinforcement_AI):
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
        if random.random() >= epsilon:
            print('Explore...')
            return random.randint(0,3)
        elif random.random() < epsilon:
            print('Exploit...')
            return np.argmax(self.Q_table[self.position[0], self.position[1]])
    
    def get_next_location(self, action):
        if(action == 3): #up
            self.position = (self.position[0], max(0, self.position[1]-1))
        elif(action == 2): #down
            self.position = (self.position[0], min(self.position[1] + 1, self.width))
        elif(action == 0): #left
            self.position = (max(self.position[0] - 1, 0), self.position[1])
        elif(action == 1): #right
            self.position = (min(self.position[0] + 1, self.width), self.position[1])
        
    def train(
        self,
        num_epoch = 1000, 
        learning_rate = 0.9,
        epsilon = 0.8, # rate of how often the bot will explore instead of exploit
        ):

        for epoch in range(num_epoch):
            #Starting position
            self.get_starting_position()
            
            while not self.is_terminal_state():
                
                #Deciding direction to move
                action = self.get_next_action(epsilon) # from 0 to 3
                print(action)
                #Current position
                old_position = self.position

                #Move self.position to new_position
                self.get_next_location(action)

                #Current position
                new_position = self.position

                reward = self.reward_matrix[new_position[0],new_position[1]]

                old_q_value = self.Q_table[old_position[0], old_position[1], action]

                temporal_difference = reward + (self.discount_rate * np.max(self.Q_table[new_position[0], new_position[1]])) - old_q_value
                #update the Q-value for the previous state and action pair
                new_q_value = old_q_value + (learning_rate * temporal_difference)
                self.Q_table[old_position[0], old_position[1], action] = new_q_value


def main():
    reward_matrix = np.zeros((10,10))
    q = Q_learning_AI(reward_matrix)
    q.train()

if __name__ == "__main__":
    main()

    