#!/usr/bin/env python3
import hex
import hexgrid
import pygame
import sys
import math
from collections import defaultdict

try:
    from better_exceptions import behook
    sys.excepthook = behook
except ImportError:
    pass


def calculate_field(grid, walls, target):
    """
        -2: target
        -1: cannot reach target
        0+: that dir
    """
    field = defaultdict(lambda: -1)
    frontier = [target]
    while frontier:
        h = frontier.pop(0)
        for i in range(6):
            dhex = hex.Hex.hex_directions[i]
            new = h - dhex
            if (new in grid
                    and field[new] == -1
                    and not walls[new]):
                field[new] = i
                frontier.append(new)    # good.
                # frontier.insert(1, new) # BAD!!!!!!
    field[target] = -2
    return field


layout = hex.Layout(hex.Layout.pointy, hex.Point(20, 20), hex.Point(0, 0))
grid = hexgrid.RectangleGrid(25, 25)

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

mousehex = hex.Hex(0, 0, 0)

target = round(layout.to_hex(hex.Point(win.get_width()//2,
                                       win.get_height()//2)))

walls = defaultdict(bool)

field = calculate_field(grid, walls, target)

lastHovered = None


def hue_to_rgb(hue, low=0, high=255):
    diff = high-low
    return (low+diff*(max(0, min(1, -abs(((hue+3) % 6)-3)+2))),
            low+diff*(max(0, min(1, -abs(((hue+1) % 6)-3)+2))),
            low+diff*(max(0, min(1, -abs(((hue+5) % 6)-3)+2))))


ms = 0
clock = pygame.time.Clock()

COLORS = [
    (255, 0, 0),
    (255, 255, 0),
    (0, 255, 0),
    (0, 150, 255),
    (150, 0, 255),
    (255, 0, 255)
]

while True:
    changed = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            lastHovered = None
        if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
            mousehex = round(layout.to_hex(hex.Point(*event.pos)))
            lb, mb, rb = pygame.mouse.get_pressed()
            if mousehex != lastHovered and mousehex in grid:
                lastHovered = mousehex
                if lb:
                    walls[mousehex] = True
                    changed = True
                if mb:
                    target = mousehex
                    changed = True
                if rb:
                    walls[mousehex] = False
                    changed = True
    if changed:
        field = calculate_field(grid, walls, target)

    win.fill((0, 0, 0))

    for h in grid:
        if walls[h] or field[h] == -2:
            width = 2
        else:
            width = 0
        if h == mousehex or field[h] == -2:
            color = (255, 255, 255)
        elif field[h] == -1:
            color = (127, 127, 127)
            # color = ((h.x*32) % 64 + 64,
            #          (h.y*32) % 64 + 64,  # TODO: rainbow off dir
            #          (h.z*32) % 64 + 64)
        else:
            color = COLORS[field[h]]
        pygame.draw.polygon(win, color,
                            layout.hex_corners(h, margin=0.9), width=width)
        if field[h] >= 0:
            corner = field[h]
            sin = math.sin(ms/75)
            point1 = (layout.hex_corner_offset(corner+1.75 + sin*0.25,
                                               0.4 + sin*0.1)
                      + layout.from_hex(h))
            point2 = (layout.hex_corner_offset(corner-2.75 - sin*0.25,
                                               0.4 + sin*0.1)
                      + layout.from_hex(h))
            point3 = (layout.hex_corner_offset(corner-0.5,
                                               0.5 + sin*0.25)
                      + layout.from_hex(h))
            pygame.draw.aalines(win, (0, 0, 0), True, [point1, point2, point3])

    pygame.display.flip()
    ms += clock.tick()
