import pygame
import random
from enum import Enum
from typing import Tuple, List

import tkinter as tk
from tkinter import messagebox

from snake import Snake, Direction
from cube import Cube
from snake_colors import *

Action = List[bool]


class SnakeGame(object):
    def __init__(self, width = 640, rows = 20) -> None:
        self.width = width
        self.rows = rows

        self.display = pygame.display.set_mode((self.width, self.width))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()

        self.snake = Snake((255, 0, 0), (10, 10))
        self.food = Cube(self.randomSnack(), color=GREEN)

        self.frame_iteration = 0

    def randomSnack(self) -> Tuple[int, int]:
        positions = self.snake.body
        while True:
            x = random.randrange(self.rows)
            y = random.randrange(self.rows)
            if (len(list(filter(lambda z:z.pos == (x,y), positions)))) > 0:
                continue
            else:
                break
        return (x,y)

    def get_action_from_user(self) -> Action:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed() # get a dictionary of all the keys pressed

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

    def collision(self) -> bool:
        for x in range(self.snake.size()):
            if self.snake.body[x].pos in list(map(lambda z:z.pos, self.snake.body[x+1:])):
                return True
        head_pos = self.snake.body[0].pos
        if head_pos[0] < 0 or head_pos[0] >= self.rows  or head_pos[1] < 0 or head_pos[1] >= self.rows:
            return True
        return False

    def play_step(self, input_action = None):
        self.frame_iteration += 1

        pygame.time.delay(100)
        self.clock.tick(50)
        action: Action = self.get_action_from_user()
        self.snake.move(action)
        reward: int = 0        
        if self.snake.body[0].pos == self.food.pos:
            self.snake.addCube()
            self.food = Cube(self.randomSnack(), color=GREEN)
            reward = 10
        if self.collision() or self.frame_iteration > 100 * self.snake.size():
            return True, self.snake.score, -10
        self.redrawWindow()
        return False, self.snake.score, reward

    def drawGrid(self) -> None:
        sizeBtwn: int = self.width // self.rows

        x: int = 0
        y: int = 0
        for l in range(self.rows):
            pygame.draw.line(self.display, WHITE, (x, 0), (x, self.width-1))
            pygame.draw.line(self.display, WHITE, (0, y), (self.width-1, y))
            x = x + sizeBtwn
            y = y + sizeBtwn
        pygame.draw.line(self.display, WHITE, (self.width-1, 0), (self.width-1, self.width-1))
        pygame.draw.line(self.display, WHITE, (0, self.width-1), (self.width-1, self.width-1))

    def redrawWindow(self) -> None:
        self.display.fill((0, 0, 0))
        self.snake.draw(self.display)
        self.food.draw(self.display)
        self.drawGrid()
        font = pygame.font.SysFont('Arial', 16)
        text = font.render('Score: ' + str(self.snake.score), True, WHITE, BLACK)
        textRect = text.get_rect()
        textRect.center = (textRect.width // 2, textRect.height // 2)
        self.display.blit(text, textRect)
        pygame.display.update()

def message_box(subject: str, content: str) -> None:
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

# reset function for agent
# reward for agent
# play(action) -> direction
# game_iteration

def main():
    width = 1000
    rows = 40
    pygame.init()
    snake_game = SnakeGame(width, rows)

    game_over = False
    while not game_over:
        game_over, score, reward = snake_game.play_step()

    message_box("You Lost!", "Your Score: " + str(score))
    pygame.quit()

if __name__ == "__main__":
    main()

