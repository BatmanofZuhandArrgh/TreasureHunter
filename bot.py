import numpy as np
import random

STARTING_SCORE = 100

class Reinforcement_AI:
    def __init__(self, reward_matrix):
        self.action = [
            'go_left',
            'go_right',
            'go_down',
            'go_up'
        ]
        self.reward_matrix = reward_matrix
        self.score = STARTING_SCORE
    def train():
        pass

    def run():
        pass

class Q_learning_AI(Reinforcement_AI):
    def __init__(
        self, 
        reward_matrix,
        discount_rate = 0.9,
        ):
        super(Q_learning_AI, self).__init__(reward_matrix)
        self.Q_table = np.zeros((len(self.action),) + self.reward_matrix.shape, dtype=np.uint8)

        self.discount_rate = discount_rate 

    def bell_man_update(self, index, jindex):
        self.Q_table[index, jindex] = 0 

    def exploit(self):
        pass

    def explore(self):
        pass

    def get_starting_position(self, type = 'normal'):
        if(type == 'normal'):
            return (0,0)

        elif(type == 'random'):
            i = random.randint(0, self.reward_matrix.shape[0]) 
            j = random.randint(0, self.reward_matrix.shape[1]) 

            return (i, j)

    def train(
        self,
        num_epoch = 1000, 
        learning_rate = 0.9,
        epsilon = 0.8, # rate of how often the bot will explore instead of exploit
        ):

        for epoch in range(num_epoch):
            #Starting position
            row_index, column_index = self.get_starting_position()
            
            while self.score > 0 and self.score < 200:
                
            if random.random() >= epsilon:
                reward = self.explore()
            elif random.random() < epsilon:
                reward = self.exploit()










def main():
    reward_matrix = np.zeros((10,10))
    q = Q_learning_AI(reward_matrix)
    print(q.Q_table)

if __name__ == "__main__":
    main()

    