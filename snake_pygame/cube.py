import pygame

WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)
GREEN = (0,255,0)

class Cube(object):
    rows: int = 20
    w: int = 500
    def __init__(self, start, dirnx=1, dirny=0, color=RED):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i*dis + 1, j*dis + 1, dis - 2, dis - 2))

        if eyes:
            centre = dis//2
            radius = 3
            circleCenter_1 = (i*dis + centre - radius, j*dis + 8)
            circleCenter_2 = (i*dis + dis - 2*radius, j*dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleCenter_1, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleCenter_2, radius)