#!/usr/bin/env python3
import hex
import hexgrid
import pygame
import sys
import math
import random

try:
    from better_exceptions import behook
    sys.excepthook = behook
except ImportError:
    pass

pygame.init()

FISH_SIZE = 6
layout = hex.Layout(hex.Layout.pointy, hex.Point(30, 30), hex.Point(0, 0))
grid = hexgrid.HexagonGrid(7)

bounds = [math.inf, math.inf, -math.inf, -math.inf]

for h in grid:
    for p in layout.hex_corners(h):
        bounds[0] = min(bounds[0], p[0])
        bounds[1] = min(bounds[1], p[1])
        bounds[2] = max(bounds[2], p[0])
        bounds[3] = max(bounds[3], p[1])

layout.origin = hex.Point(-bounds[0], -bounds[1])

win = pygame.display.set_mode((int(bounds[2]-bounds[0]),
                               int(bounds[3]-bounds[1])))

pos = round(layout.to_hex(hex.Point(win.get_width()//2,
                                    win.get_height()//2)))

ms = 0
clock = pygame.time.Clock()

distribution = [1, 1, 1, 2, 2, 3]

board = {h: distribution[random.randint(0, 5)] for h in grid}

FONT = pygame.font.SysFont(None, 20)

players = [
    {
        "tokens": [pos],
        "score": 1
    }
]

turn = {
    "player": 0,
    "selected": pos
}

mousehex = None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION):
            h = round(layout.to_hex(hex.Point(event.pos)))
            if h in grid:
                mousehex = h

    win.fill((0, 0, 0))

    for h in grid:
        if board[h] == -1:
            color = (0, 100, 255)
        elif h == turn["selected"]:
            color = (100, 255, 100)
        else:
            color = (160, 255, 255)
        if h == mousehex:
            color = tuple(min(int((i/255)**2*255), 255) for i in color)
        corners = layout.hex_corners(h, 1)
        pygame.draw.polygon(win, [min(255, i*2) for i in color],
                            corners[1:5])
        pygame.draw.polygon(win, [i//2 for i in color],
                            corners[4:] + corners[:2])
        pygame.draw.polygon(win, color,
                            layout.hex_corners(h, 0.75))
        if board[h] == 1:
            pygame.draw.circle(win, (0, 150, 0), round(layout.from_hex(h)),
                               FISH_SIZE)
        if board[h] == 2:
            pygame.draw.circle(win, (150, 0, 255),
                               round(layout.from_hex(h)
                                     + layout.hex_corner_offset(0.5, 0.3)),
                               FISH_SIZE)
            pygame.draw.circle(win, (150, 0, 255),
                               round(layout.from_hex(h)
                                     + layout.hex_corner_offset(3.5, 0.3)),
                               FISH_SIZE)
        if board[h] == 3:
            pygame.draw.circle(win, (255, 150, 0),
                               round(layout.from_hex(h)
                                     + layout.hex_corner_offset(0, 0.3)),
                               FISH_SIZE)
            pygame.draw.circle(win, (255, 150, 0),
                               round(layout.from_hex(h)
                                     + layout.hex_corner_offset(2, 0.3)),
                               FISH_SIZE)
            pygame.draw.circle(win, (255, 150, 0),
                               round(layout.from_hex(h)
                                     + layout.hex_corner_offset(4, 0.3)),
                               FISH_SIZE)

    pygame.display.flip()
    ms += clock.tick()
