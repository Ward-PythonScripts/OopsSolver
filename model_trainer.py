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
        self.action_space = MultiDiscrete([25, 25])
        # Observations is gewoon het speelbord
        self.observation_space = MultiDiscrete([[21, 21, 21, 21, 21], [21, 21, 21, 21, 21], [21, 21, 21, 21, 21]
                                                   , [21, 21, 21, 21, 21], [21, 21, 21, 21, 21]])
        # get the grid from a random level from the level directory
        # state = grid
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
        begin_position = action[0]
        bx, by = pos2indices(begin_position)
        end_position = action[1]
        ex, ey = pos2indices(end_position)
        print("Registered input, from ", bx , by, " to ", ex, ey)
        if not valid_pickup(bx, by, self.state):
            reward = -20
            print("Not valid pickup")
            return self.state, reward, done, info
        elif not valid_end(ex, ey, self.state):
            reward = -15
            print("Not valid end")
            return self.state, reward, done, info
        elif not valid_steps(bx, by, ex, ey, self.state):
            reward = -1
            print("Not valid amount of steps")
            return self.state, reward, done, info
        print("Valid action")
        # else, the action was valid, could still not be the best one to complete the game ofcourse
        reward = 20
        self.state = execute_step(bx, by, ex, ey, self.state)
        if is_game_won(self.state):
            reward = 200
            done = True
            print("A game was completed, you did it you crazy son of a bitch, you did it :)")
            return self.state, reward, done, info
        else:
            # one step done a few more to go
            return self.state, reward, done, info

    def render(self):
        print("#" * 30)
        row_str = ""
        for y in range(len(self.state)):
            for x in range(len(self.state[0])):
                str_element = str(self.state[y][x])
                if len(str_element) <= 1:
                    #we need to add a space to make the print more alligned
                    row_str += "     " + str_element
                else:
                    row_str += "    " + str_element
            print(row_str)
            row_str = ""
        print("#" * 30)


    def reset(self):
        self.state = get_grid()
        self.attempts = 30
        return self.state


def execute_step(bx, by, ex, ey, grid):
    # check which piece is going to go where and create the new grid
    # add the two new spaces up
    grid[ey][ex] += grid[by][bx]
    # where the piece used to be there will now be an empty space
    grid[by][bx] = 0
    return np.array(grid)


def valid_pickup(x, y, grid):
    # target_pos is the position we are trying to pick up, this needs to be valid
    # can't pick up empty space or the hat
    target_piece = grid[y][x]
    if target_piece in [0, 10]:
        return False
    else:
        return True


def valid_end(x, y, grid):
    # we need to put the pieces down on a valid space(not on the wizards' head) and on another piece
    target_piece = grid[y][x]
    if target_piece == 0 or target_piece >= 20:
        return False
    else:
        return True


def valid_steps(bx, by, ex, ey, grid):
    # and we need to check if the amount of steps we have done is valid
    x_dist = abs(bx - ex)
    y_dist = abs(by - ey)
    tot_dist = x_dist + y_dist
    picked_up_piece = grid[by][bx]
    # we need to remove the wizards identifier from the equation ( is 20)
    if picked_up_piece >= 20:
        picked_up_piece -= 19
    if tot_dist == picked_up_piece:
        return True
    else:
        return False

def is_game_won(grid):
    # if the game is won we can give the ai a big bonus
    amountOfPiecesFound = 0
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] != 0:
                amountOfPiecesFound += 1
    if amountOfPiecesFound <= 1:
        gameFinished = True
        return True
    else:
        return False


def pos2indices(pos):
    pos_var = pos
    for y in range(0, 5):
        for x in range(0, 5):
            if pos_var <= 0:
                return x, y
            pos_var -= 1
    return 4, 4


def get_grid():
    file_names = glob.glob("Levels/*")
    if len(file_names) == 0:
        print("No levels to train from were found, bitch plz")
        exit(-1)
    select_nr = random.randint(0, len(file_names) - 1)
    selected_level = file_names[select_nr]
    with open(os.path.join(selected_level), "rb") as f:
        grid = pickle.load(f)
        return np.array(grid)


def test_environment_manuel(env):
    episodes = 5
    for episode in range(1, episodes + 1):
        state = env.reset()
        done = False
        score = 0

        while not done:
            env.render()
            #action = env.action_space.sample()
            action = list(map(int, input("\nEnter the numbers : ").strip().split()))
            n_state, reward, done, info = env.step(action)
            score += reward
        print('Episode:{} Score:{}'.format(episode, score))
    env.close()


def get_env():
    env = OopsEnv()
    #check_env(env, warn=True)
    return env


# MAIN
g_env = get_env()
test_environment_manuel(g_env)

