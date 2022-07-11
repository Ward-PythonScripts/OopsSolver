import gym
from gym import Env
from gym.spaces import Discrete, Box, Dict, Tuple, MultiBinary, MultiDiscrete
import numpy as np
import random
import os
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import VecFrameStack
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.callbacks import EvalCallback,StopTrainingOnRewardThreshold


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
        # Observations is gewoon het speelbord, we have to flatten the matrix because otherwise it crashes
        self.observation_space = MultiDiscrete(np.array([31, 31, 31, 31, 31,31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31]))
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
        # print("Registered input, from ", bx , by, " to ", ex, ey)
        if not valid_pickup(begin_position, self.state):
            reward = -20
            # print("Not valid pickup")
            return self.state, reward, done, info
        elif not valid_end(end_position, self.state):
            reward = -15
            # print("Not valid end")
            return self.state, reward, done, info
        elif not valid_steps(bx, by, ex, ey,begin_position, self.state):
            reward = -1
            # print("Not valid amount of steps")
            return self.state, reward, done, info
        # print("Valid action")
        # else, the action was valid, could still not be the best one to complete the game ofcourse
        self.state = execute_step(begin_position,end_position, self.state)
        if is_game_won(self.state):
            reward = 200
            done = True
            #print("A game was completed, you did it you crazy son of a bitch, you did it :)")
            return self.state, reward, done, info
        elif no_more_valid_steps(self.state):
            #print("no more valid steps to take")
            reward = 0
            done = True
            return self.state, reward, done, info
        else:
            # one step done a few more to go
            reward = 20
            return self.state, reward, done, info

    def render(self):
        print("#" * 30)
        row_str = ""
        row_ind = 0
        for x in range(len(self.state)):
            str_element = str(self.state[x])
            if len(str_element) <= 1:
                # we need to add a space to make the print more alligned
                row_str += "     " + str_element
            else:
                row_str += "    " + str_element
            row_ind +=1
            if row_ind >= 5:
                print(row_str)
                row_str = ""
                row_ind = 0
        print("#" * 30)

    def reset(self):
        self.state = get_grid()
        self.attempts = 30
        return self.state


def execute_step(begin_pos,end_pos,grid):
    # check which piece is going to go where and create the new grid
    # add the two new spaces up
    grid[end_pos] += grid[begin_pos]
    # # where the piece used to be there will now be an empty space
    grid[begin_pos] = 0
    return grid


def valid_pickup(begin_pos, grid):
    # target_pos is the position we are trying to pick up, this needs to be valid
    # can't pick up empty space or the hat
    target_piece = grid[begin_pos]
    if target_piece in [0, 10]:
        return False
    else:
        return True


def valid_end(end_pos, grid):
    # we need to put the pieces down on a valid space(not on the wizards' head) and on another piece
    target_piece = grid[end_pos]
    if target_piece == 0 or target_piece >= 20:
        return False
    else:
        return True

def no_more_valid_steps(grid):
    # check if there are pieces left on the board and get their position, than check if the distance between any is a
    # valid distance to cover
    list_pieces = []
    for x in range(0,len(grid)-1):
        if x != 0:
            #found a piece
            list_pieces.append(x)
    for piece_pos in list_pieces:
        steps = get_piece_steps(grid,piece_pos)
        for second_piece in list_pieces:
            if steps == get_piece_distance(piece_pos,second_piece):
                #we have found a valid option(the piece can reach the other piece
                #only need to check that that move would be valid
                if valid_pickup(piece_pos,grid) and valid_end(second_piece,grid):
                    #there is in fact still a valid move left
                    return False
    return True


def get_piece_steps(grid,pos):
    picked_up_piece = grid[pos]
    # we need to remove the wizards identifier from the equation ( is 20)
    if picked_up_piece >= 20:
        picked_up_piece -= 19
    return picked_up_piece

def get_piece_distance(pos1,pos2):
    x1,y1 = pos2indices(pos1)
    x2,y2 = pos2indices(pos2)
    x_dist = abs(x1 - x2)
    y_dist = abs(y1 - y2)
    tot_dist = x_dist + y_dist
    return tot_dist
def valid_steps(bx, by, ex, ey,begin_pos, grid):
    # and we need to check if the amount of steps we have done is valid
    x_dist = abs(bx - ex)
    y_dist = abs(by - ey)
    tot_dist = x_dist + y_dist
    piece_steps = get_piece_steps(grid,begin_pos)
    if tot_dist == piece_steps:
        return True
    else:
        return False


def is_game_won(grid):
    # if the game is won we can give the ai a big bonus
    amountOfPiecesFound = 0
    for x in range(len(grid)):
        if grid[x] != 0:
            amountOfPiecesFound += 1
    if amountOfPiecesFound <= 1:
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
        return np.array(grid).flatten()


def test_environment_manuel(env):
    episodes = 5
    for episode in range(1, episodes + 1):
        state = env.reset()
        done = False
        score = 0

        while not done:
            env.render()
            # action = env.action_space.sample()
            action = list(map(int, input("\nEnter the numbers : ").strip().split()))
            n_state, reward, done, info = env.step(action)
            score += reward
        print('Episode:{} Score:{}'.format(episode, score))
    env.close()


def get_env():
    env = OopsEnv()
    check_env(env, warn=True)
    return env

def load_model(env):
    return PPO.load(os.path.join(model_path,"best_model"),env)

def train_model(model, amount_of_steps):
    model.learn(total_timesteps=amount_of_steps,callback=eval_callback)
    model.save(model_path)


def get_new_model(env):
    log_path = os.path.join("Logs")
    model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=log_path)
    return model


# MAIN
g_env = get_env()
g_env.reset()
#load the previous best model in and continue training that one
model_path = os.path.join("Models","Oops_Model")
#add callback that saves the best model -> you can quit whenever really
eval_callback = EvalCallback(g_env,eval_freq=20000,best_model_save_path=model_path,verbose=1)
test_environment_manuel(g_env)
#g_model = get_new_model(g_env)
#g_model = load_model(g_env)
#train_model(g_model, 4000000)

