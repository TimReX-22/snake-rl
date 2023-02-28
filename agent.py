import json
from model import Linear_QNet, QTrainer
from snake_pygame.snake import Direction
from snake_pygame.snake_game import SnakeGame, Action, State

import torch
import random
import argparse
import os
import numpy as np
import matplotlib.pyplot as plt

from collections import deque
from typing import List
from dataclasses import dataclass

import matplotlib
matplotlib.use('TkAgg')


@dataclass
class AgentParameters:
    max_memory: int
    batch_size: int
    lr: int
    gamma: int
    epsilon: int
    model_name: str = None
    train: bool = True


class Agent:
    def __init__(self, parameters: AgentParameters) -> None:
        self.n_games = 0
        self.parameters = parameters
        self.memory = deque(maxlen=self.parameters.max_memory)
        self.model = Linear_QNet(12, 256, 3)
        if self.parameters.train:
            self.trainer = QTrainer(
                model=self.model, lr=self.parameters.lr, gamma=self.parameters.gamma)
        else:
            self.trainer = None
            self.model.load_state_dict(torch.load(self.parameters.model_name))

    def remember(self, state, action: Action, reward: int, next_state, done: bool) -> None:
        # pop left if MAX_MEMORY is reached
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > self.parameters.batch_size:
            mini_sample = random.sample(
                self.memory, self.parameters.batch_size)
        else:
            mini_sample = self.memory
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action: Action, reward: int, next_state, done: bool):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state) -> Action:
        # random moves, tradeoff exploration / exploitation, only during training
        if self.parameters.train:
            randomness = self.parameters.epsilon - self.n_games

        final_move = [0, 0, 0]
        if self.parameters.train and random.randint(0, 200) < randomness:
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


def train(parameters: AgentParameters):
    plot_scores = []
    plot_mean_scores = []
    plot_games = []
    window_size = 10
    total_score = 0
    record = 0

    game = SnakeGame(500, 20)
    agent = Agent(parameters)

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


def run(parameters: AgentParameters):
    game = SnakeGame(500, 20)
    agent = Agent(parameters)
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


def get_parameters(filename: str) -> AgentParameters:
    with open(filename, 'r') as f:
        data = json.load(f)
    if "model_name" in data:
        return AgentParameters(data["max_memory"], data["batch_size"],
                               data["lr"], data["gamma"], data["epsilon"],
                               data["model_name"], train=False)
    return AgentParameters(data["max_memory"], data["batch_size"],
                           data["lr"], data["gamma"], data["epsilon"])


def cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Command line Interface for the Snake-Agent')
    parser.add_argument('parameter_filename')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = cli()
    params = get_parameters(args.parameter_filename)
    if (params.train):
        train(params)
    else:
        if os.path.isfile(params.model_name):
            run(params)
        else:
            print("Model file does not exist!")
