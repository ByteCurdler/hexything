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

pygame.init()

layout = hex.Layout(hex.Layout.pointy, hex.Point(15, 15), hex.Point(0, 0))
grid = hexgrid.HexagonGrid(15)

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

movement_text = "XDEWAZ"
movement = [
    pygame.K_x,
    pygame.K_d,
    pygame.K_e,
    pygame.K_w,
    pygame.K_a,
    pygame.K_z
]


walls = defaultdict(bool)

FONT = pygame.font.SysFont(None, 20)

lastHovered = None

changed = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key in movement:
                new = pos.neighbor(movement.index(event.key))
                if new in grid and not walls[new]:
                    pos = new
                    changed = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            lastHovered = None
        if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
            mousehex = round(layout.to_hex(hex.Point(*event.pos)))
            lb, mb, rb = pygame.mouse.get_pressed()
            if mousehex != lastHovered and mousehex in grid:
                lastHovered = mousehex
                if lb and mousehex != pos:
                    walls[mousehex] = True
                    changed = True
                if mb:
                    pos = mousehex
                    changed = True
                if rb:
                    walls[mousehex] = False
                    changed = True

    if changed:
        changed = False
        win.fill((0, 0, 0))

        for h in grid:
            if walls[h]:
                color = (127, 127, 127)
            elif pos == h:
                color = (255, 255, 0)
            else:
                for i in hex.Hex.linedraw(pos, h):
                    if walls[i]:
                        color = (255, 150, 150)
                        break
                else:
                    color = (150, 255, 150)
            pygame.draw.polygon(win, [i//2 for i in color],
                                layout.hex_corners(h, 1))
            pygame.draw.polygon(win, color,
                                layout.hex_corners(h, 0.75))

        for i in range(6):
            target = pos.neighbor(i)
            if target in grid and not walls[target]:
                text = FONT.render(movement_text[i], True, (0, 0, 0))
                rect = text.get_rect()
                rect.center = layout.from_hex(target)
                win.blit(text, rect.topleft)

        pygame.display.flip()
