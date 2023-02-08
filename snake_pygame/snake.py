from snake_pygame.snake_colors import BLUE1, BLUE2
from snake_pygame.cube import Cube
from typing import List
from enum import Enum

import pygame

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


class Snake(object):
    body = []
    turns = {}
    score: int = 0

    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos, color=BLUE1, color2=BLUE2)
        self.body.append(self.head)
        self.body.append(Cube((pos[0] - 1, pos[1]), color=BLUE1, color2=BLUE2))
        self.body.append(Cube((pos[0] - 2, pos[1]), color=BLUE1, color2=BLUE2))
        self.dirnx = 1  # direction of snake in x axis
        self.dirny = 0  # direction of snake in y axis

    def move(self, action: List[bool]):

        if action[1]:
            # right turn
            if self.dirnx == 1:
                self.dirnx = 0
                self.dirny = 1
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            elif self.dirnx == -1:
                self.dirnx = 0
                self.dirny = -1
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            elif self.dirny == 1:
                self.dirnx = -1
                self.dirny = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            elif self.dirny == -1:
                self.dirnx = 1
                self.dirny = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        elif action[2]:
            # left turn
            if self.dirnx == 1:
                self.dirnx = 0
                self.dirny = -1
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            elif self.dirnx == -1:
                self.dirnx = 0
                self.dirny = 1
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            elif self.dirny == 1:
                self.dirnx = 1
                self.dirny = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            elif self.dirny == -1:
                self.dirnx = -1
                self.dirny = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                # if c.dirnx == -1 and c.pos[0] <= 0:
                #     c.pos = (c.rows-1, c.pos[1])
                # elif c.dirnx == 1 and c.pos[0] >= c.rows-1:
                #     c.pos = (0,c.pos[1])
                # elif c.dirny == 1 and c.pos[1] >= c.rows-1:
                #     c.pos = (c.pos[0], 0)
                # elif c.dirny == -1 and c.pos[1] <= 0:
                #     c.pos = (c.pos[0],c.rows-1)
                # else:
                c.move(c.dirnx, c.dirny)

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        new_cube_x: int = tail.pos[0]
        new_cube_y: int = tail.pos[1]

        if dx == 1:
            new_cube_x -= 1
        elif dx == -1:
            new_cube_x += 1
        elif dy == 1:
            new_cube_y -= 1
        elif dy == -1:
            new_cube_y += 1

        self.body.append(Cube((new_cube_x, new_cube_y), dx,
                         dy, color=BLUE1, color2=BLUE2))
        self.score += 1

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)

    def reset(self, pos):
        self.head = Cube(pos, color=BLUE1, color2=BLUE2)
        self.body = []
        self.body.append(self.head)
        self.body.append(Cube((pos[0] - 1, pos[1]), color=BLUE1, color2=BLUE2))
        self.body.append(Cube((pos[0] - 2, pos[1]), color=BLUE1, color2=BLUE2))
        self.turns = {}
        self.dirnx = 1
        self.dirny = 0
        self.score = 0

    def size(self) -> int:
        return len(self.body)

    def get_action(self, dir: Direction) -> List[bool]:
        if dir == Direction.DOWN:
            if self.dirny == 1:
                return [1, 0, 0]
            if self.dirny == -1:
                return [1, 0, 0]
            if self.dirnx == 1:
                return [0, 1, 0]
            if self.dirnx == -1:
                return [0, 0, 1]
        elif dir == Direction.UP:
            if self.dirny == 1:
                return [1, 0, 0]
            if self.dirny == -1:
                return [1, 0, 0]
            if self.dirnx == 1:
                return [0, 0, 1]
            if self.dirnx == -1:
                return [0, 1, 0]
        elif dir == Direction.RIGHT:
            if self.dirny == 1:
                return [0, 0, 1]
            if self.dirny == -1:
                return [0, 1, 0]
            if self.dirnx == 1:
                return [1, 0, 0]
            if self.dirnx == -1:
                return [1, 0, 0]
        elif dir == Direction.LEFT:
            if self.dirny == 1:
                return [0, 1, 0]
            if self.dirny == -1:
                return [0, 0, 1]
            if self.dirnx == 1:
                return [1, 0, 0]
            if self.dirnx == -1:
                return [1, 0, 0]
        return [0, 0, 0]

    def direction(self) -> Direction:
        if self.dirnx == 1:
            return Direction.RIGHT
        elif self.dirnx == -1:
            return Direction.LEFT
        elif self.dirny == 1:
            return Direction.DOWN
        elif self.dirny == -1:
            return Direction.UP
        return None
