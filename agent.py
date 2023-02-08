import torch
import random
import os
import numpy as np
from collections import deque
import argparse

import matplotlib.pyplot as plt


from snake_pygame.snake_game import SnakeGame, Action, State
from snake_pygame.snake import Direction

from model import Linear_QNet, QTrainer

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


class Agent:
    def __init__(self) -> None:
        self.n_games = 0
        self.epsilon = 0  # randomness
        self.gamma = 0.9  # discount rate [0, 1]
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(model=self.model, lr=LR, gamma=self.gamma)

    def remember(self, state, action: Action, reward: int, next_state, done: bool) -> None:
        # pop left if MAX_MEMORY is reached
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(
                self.memory, BATCH_SIZE)  # returns list of tuples
        else:
            mini_sample = self.memory
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action: Action, reward: int, next_state, done: bool):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state) -> Action:
        # random moves, tradeoff exploration / exploitation
        self.epsilon = 100 - self.n_games
        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move_idx = random.randint(0, 2)
            final_move[move_idx] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move_idx = torch.argmax(prediction).item()
            final_move[move_idx] = 1
        return final_move


def moving_average(x, w):
    if len(x) < (w - 1):
        return np.zeros(len(x))
    return np.convolve(x, np.ones(w), 'valid') / w + np.zeros(w - 1)


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    game = SnakeGame(500, 20)
    agent = Agent()

    while True:
        state_old = game.get_state()

        final_move: Action = agent.get_action(state_old)

        done, score, reward = game.play_step(input_action=final_move)

        state_new = game.get_state()

        agent.train_short_memory(
            state_old, final_move, reward, state_new, done)

        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory (experience replay) and plot:
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save(file_name="model_score_" + str(record))

            print("Game: ", agent.n_games, "Score: ", score, "Record: ", record)
            plot_scores.append(score)


def run(model_name: str):
    pass


def cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Command line Interface for the Snake-Agent')
    parser.add_argument('-t', '--train', action='store_true',
                        help='train a new agent')
    parser.add_argument('-m', '--model', required=False,
                        help="name of model to run, in folder ./model")
    parser.set_defaults(train=False)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = cli()
    if (args.train):
        train()
    elif (args.model):
        if os.path.isfile("./model/" + args.model):
            run("./model/" + args.model)
        else:
            print("model file does not exist!")
    else:
        print("Failure: Eiher specifiy training or which model to run! Aborting...")
