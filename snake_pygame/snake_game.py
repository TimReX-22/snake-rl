from snake_pygame.snake_colors import *
from snake_pygame.cube import Cube
from snake_pygame.snake import Snake, Direction

import pygame
import numpy as np
import random

from enum import Enum
from typing import Tuple, List

import tkinter as tk
from tkinter import messagebox

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))


Action = List[bool]
State = np.ndarray


class SnakeGame(object):
    def __init__(self, width=640, rows=20) -> None:
        self.width = width
        self.rows = rows

        self.display = pygame.display.set_mode((self.width, self.width))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()

        self.snake = Snake((255, 0, 0), (10, 10))
        self.food = Cube(self._randomSnack(), color=GREEN)

        self.frame_iteration = 0

        pygame.init()

    def _randomSnack(self) -> Tuple[int, int]:
        positions = self.snake.body
        while True:
            x = random.randrange(self.rows)
            y = random.randrange(self.rows)
            if (len(list(filter(lambda z: z.pos == (x, y), positions)))) > 0:
                continue
            else:
                break
        return (x, y)

    def _get_action_from_user(self) -> Action:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()  # get a dictionary of all the keys pressed

            for key in keys:
                if keys[pygame.K_LEFT]:
                    return self.snake.get_action(Direction.LEFT)
                elif keys[pygame.K_RIGHT]:
                    return self.snake.get_action(Direction.RIGHT)
                elif keys[pygame.K_UP]:
                    return self.snake.get_action(Direction.UP)
                elif keys[pygame.K_DOWN]:
                    return self.snake.get_action(Direction.DOWN)
        return [0, 0, 0]

    def collision(self, pt=None) -> bool:
        if pt is None:
            pt = self.snake.body[0].pos

        if pt in list(map(lambda z: z.pos, self.snake.body[1:])):
            return True

        if pt[0] < 0 or pt[0] >= self.rows or pt[1] < 0 or pt[1] >= self.rows:
            return True
        return False

    def play_step(self, input_action=None):
        self.frame_iteration += 1

        pygame.time.delay(100)
        self.clock.tick(50)
        action: Action
        if input_action is not None:
            action = input_action
        else:
            action = self._get_action_from_user()

        dist1 = self.distance_to_food()

        self.snake.move(action)
        reward: int = 0
        if self.snake.body[0].pos == self.food.pos:
            self.snake.addCube()
            self.food = Cube(self._randomSnack(), color=GREEN)
            reward = 10
        elif dist1 > self.distance_to_food():
            reward = 1

        if self.collision() or self.frame_iteration > 100 * self.snake.size():
            return True, self.snake.score, -10
        self._redrawWindow()
        return False, self.snake.score, reward

    def _drawGrid(self) -> None:
        sizeBtwn: int = self.width // self.rows

        x: int = 0
        y: int = 0
        for l in range(self.rows):
            pygame.draw.line(self.display, WHITE, (x, 0), (x, self.width-1))
            pygame.draw.line(self.display, WHITE, (0, y), (self.width-1, y))
            x = x + sizeBtwn
            y = y + sizeBtwn
        pygame.draw.line(self.display, WHITE, (self.width-1, 0),
                         (self.width-1, self.width-1))
        pygame.draw.line(self.display, WHITE, (0, self.width-1),
                         (self.width-1, self.width-1))

    def _redrawWindow(self) -> None:
        self.display.fill((0, 0, 0))
        self.snake.draw(self.display)
        self.food.draw(self.display)
        self._drawGrid()
        font = pygame.font.SysFont('Arial', 16)
        text = font.render(
            'Score: ' + str(self.snake.score), True, WHITE, BLACK)
        textRect = text.get_rect()
        textRect.center = (textRect.width // 2, textRect.height // 2)
        self.display.blit(text, textRect)
        pygame.display.update()

    def reset(self):
        self.frame_iteration = 0
        self.snake.reset((self.rows // 2, self.rows // 2))
        self.food = Cube(self._randomSnack(), color=GREEN)

    def get_state(self) -> State:

        snake_head = self.snake.body[0].pos
        food_pos = self.food.pos

        point_r = (snake_head[0] + self.rows // 2, snake_head[1])
        point_l = (snake_head[0] - self.rows // 2, snake_head[1])
        point_u = (snake_head[0], snake_head[1] - self.rows // 2)
        point_d = (snake_head[0], snake_head[1] + self.rows // 2)

        dir_l = self.snake.direction() == Direction.LEFT
        dir_r = self.snake.direction() == Direction.RIGHT
        dir_u = self.snake.direction() == Direction.UP
        dir_d = self.snake.direction() == Direction.DOWN

        state = [
            # danger straight
            (dir_r and self.collision(pt=point_r)) or
            (dir_l and self.collision(pt=point_l)) or
            (dir_u and self.collision(pt=point_u)) or
            (dir_d and self.collision(pt=point_d)),
            # danger right
            (dir_r and self.collision(pt=point_d)) or
            (dir_l and self.collision(pt=point_u)) or
            (dir_u and self.collision(pt=point_r)) or
            (dir_d and self.collision(pt=point_l)),
            # danger left
            (dir_r and self.collision(pt=point_u)) or
            (dir_l and self.collision(pt=point_d)) or
            (dir_u and self.collision(pt=point_l)) or
            (dir_d and self.collision(pt=point_r)),
            # directions
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            # food left
            food_pos[0] < snake_head[0],
            # food right
            food_pos[0] > snake_head[0],
            # food up
            food_pos[1] < snake_head[1],
            # food down
            food_pos[1] > snake_head[1],
            # length of snake
            self.snake.size() / (0.05 * self.rows * self.rows)
        ]
        return np.array(state, dtype=int)

    def distance_to_food(self):
        snake_pos = np.array(self.snake.body[0].pos)
        food_pos = np.array(self.food.pos)
        return np.linalg.norm(snake_pos - food_pos)
