from model import Linear_QNet, QTrainer
from snake_pygame.snake import Direction
from snake_pygame.snake_game import SnakeGame, Action, State
import matplotlib.pyplot as plt
import torch
import random
import os
import numpy as np
from collections import deque
from typing import List
import argparse

import matplotlib
matplotlib.use('TkAgg')


MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


class Agent:
    def __init__(self, model_path: str = None, train: bool = True) -> None:
        self.n_games = 0
        self.epsilon = 0  # randomness
        self.gamma = 0.9  # discount rate [0, 1]
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(12, 256, 3)
        if train:
            self.trainer = QTrainer(model=self.model, lr=LR, gamma=self.gamma)
        else:
            self.trainer = None
        if model_path is not None:
            self.model.load_state_dict(torch.load(model_path))
        self.train = train

    def remember(self, state, action: Action, reward: int, next_state, done: bool) -> None:
        # pop left if MAX_MEMORY is reached
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(
                self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action: Action, reward: int, next_state, done: bool):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state) -> Action:
        # random moves, tradeoff exploration / exploitation, only during training
        if self.train:
            self.epsilon = 100 - self.n_games

        final_move = [0, 0, 0]
        if self.train and random.randint(0, 200) < self.epsilon:
            move_idx = random.randint(0, 2)
            final_move[move_idx] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move_idx = torch.argmax(prediction).item()
            final_move[move_idx] = 1
        return final_move


def moving_average(x: List[int], size: int) -> int:
    if len(x) < size:
        return 0
    sum = 0
    for i in range(len(x) - size, len(x)):
        sum += x[i]
    return sum / size


def train(checkpoint):
    plot_scores = []
    plot_mean_scores = []
    plot_games = []
    window_size = 10
    total_score = 0
    record = 0
    game = SnakeGame(500, 20)
    if checkpoint is not None:
        checkpoint = "./model/" + checkpoint

    agent = Agent(model_path=checkpoint)

    plt.ion()

    figure, ax = plt.subplots(figsize=(10, 8))
    line1, = ax.plot(plot_games, plot_scores, label="Scores")
    line2, = ax.plot(plot_games, plot_mean_scores,
                     label="Moving Average Score")
    plt.title("Scores", fontsize=20)
    plt.xlabel("Nr. of Games")
    plt.ylabel("Score")

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
            plot_games.append(agent.n_games)
            plot_mean_scores.append(moving_average(plot_scores, window_size))

            # line1.set_xdata(plot_games)
            # line1.set_ydata(plot_scores)
            # line2.set_xdata(plot_games)
            # line2.set_ydata(plot_mean_scores)
            # figure.canvas.draw()
            # figure.canvas.flush_events()
            # plt.show()


def run(model_name: str):
    game = SnakeGame(500, 20)
    agent = Agent(model_path=model_name, train=False)
    done = False
    record: int = 0

    while not done:
        state = game.get_state()
        move: Action = agent.get_action(state)
        done, score, _ = game.play_step(input_action=move)

        if done:
            game.reset()
            agent.n_games += 1

            if score > record:
                record = score
            print("Game: ", agent.n_games, "Score: ", score, "Record: ", record)
            cont_str = input("Continue? [y/n] ")
            if cont_str == "y":
                done = False


def cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Command line Interface for the Snake-Agent')
    parser.add_argument('-t', '--train', action='store_true',
                        help='train a new agent')
    parser.add_argument('-m', '--model', required=False,
                        help="name of model to run, in folder ./model")
    parser.add_argument('-c', '--checkpoint', required=False,
                        help="name of checkpoint to continue training, in folder ./model")
    parser.set_defaults(train=False)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = cli()
    if (args.train):
        checkpoint = None
        if args.checkpoint:
            checkpoint = args.checkpoint
        train(checkpoint)
    elif (args.model):
        if os.path.isfile("./model/" + args.model):
            run("./model/" + args.model)
        else:
            print("Model file does not exist!")
    else:
        print("Failure: Eiher specifiy training or which model to run! Aborting...")
