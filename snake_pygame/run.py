from tkinter import messagebox
import tkinter as tk
import pygame
from snake_pygame.snake_game import SnakeGame
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))


def message_box(subject: str, content: str) -> None:
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    width = 1000
    rows = 40

    snake_game = SnakeGame(width, rows)

    game_over = False
    while not game_over:
        game_over, score, reward = snake_game.play_step()

    message_box("You Lost!", "Your Score: " + str(score))
    pygame.quit()


if __name__ == "__main__":
    main()
