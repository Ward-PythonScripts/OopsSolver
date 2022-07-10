import gym
from gym import Env
from gym.spaces import Discrete, Box, Dict, Tuple, MultiBinary, MultiDiscrete
import numpy as np
import random
import os
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import VecFrameStack
from stable_baselines3.common.evaluation import evaluate_policy
import glob
import pickle
from stable_baselines3.common.env_checker import check_env

"""
Grid format: pieces: standard piece -> 1, wizard -> 20, hat -> 10, empty -> 0, double_stack -> 2
"""


class OopsEnv(Env):
    def __init__(self):
        # Actions we can take: from 25 positions to 25 other positions -> 5 bit + 5 bit = 10bit
        self.action_space = MultiBinary(10)
        # Observations is gewoon het speelbord
        self.observation_space = MultiDiscrete([[21, 21, 21, 21, 21], [21, 21, 21, 21, 21], [21, 21, 21, 21, 21]
                                                   , [21, 21, 21, 21, 21], [21, 21, 21, 21, 21]])
        # get the grid from a random level from the level directory
        self.state = get_grid()
        self.attempts = 30

    def step(self, action):
        # reduce attempts and stop if we don't have any attempts left
        self.attempts -= 1

        if self.attempts <= 0:
            done = True
        else:
            done = False

        # placeholder for info
        info = {}
        # check if attempted step is a valid step and calculate reward
        print(action)
        reward = 1



        return self.state,reward,done,info

    def render(self):
        pass

    def reset(self):
        self.state = get_grid()
        self.attempts = 30
        return self.state


def get_grid():
    file_names = glob.glob("Levels/*")
    if len(file_names) == 0:
        print("No levels to train from were found, bitch plz")
        exit(-1)
    select_nr = random.randint(0, len(file_names) - 1)
    selected_level = file_names[select_nr]
    print(selected_level)
    with open(os.path.join(selected_level), "rb") as f:
        grid = pickle.load(f)
        print(np.array(grid))
        return np.array(grid)


def test_environment(env):
    episodes = 5
    for episode in range(1, episodes + 1):
        state = env.reset()
        done = False
        score = 0

        while not done:
            env.render()
            action = env.action_space.sample()
            n_state, reward, done, info = env.step(action)
            score += reward
        print('Episode:{} Score:{}'.format(episode, score))
    env.close()


def get_env():
    env = OopsEnv()
    check_env(env, warn=True)
    return env


# MAIN
g_env = get_env()
"""

def CheckGameFinished(a_board):
    if a_board is not None:
        amountOfPiecesFound = 0
        for x in range(len(board)):
            for y in range(len(board[0])):
                if a_board[x][y] != 0:
                    amountOfPiecesFound += 1
        if amountOfPiecesFound <= 1:
            gameFinished = True
            return True
        else:
            return False



def PrintBoard(a_board):
    print("#" * 30)
    for x in range(len(a_board)):
        print(a_board[x])
    print("#" * 30)

"""
