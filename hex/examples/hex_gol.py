#!/usr/bin/env python3
import sys
import os
sys.path.append(os.curdir)
sys.path.append(os.pardir)
sys.path.append(os.pardir + os.sep + os.pardir)

if True:  # satisfy auto-formatter
    import math
    import pygame
    from hex import hexgrid
    import hex


try:
    from better_exceptions import behook
    sys.excepthook = behook
except ImportError:
    pass

pygame.init()

layout = hex.Layout(hex.Layout.pointy, hex.Point(15, 15), hex.Point(0, 0))
grid = hexgrid.HexagonGrid(12)

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

movement_text = "XDEWAZ"
movement = [
    pygame.K_x,
    pygame.K_d,
    pygame.K_e,
    pygame.K_w,
    pygame.K_a,
    pygame.K_z
]


def gol_step(state):
    newstate = {}
    for h in state:
        count = sum([state[n] for i in range(6)
                     if (n := h.neighbor(i)) in grid])
        if state[h]:
            newstate[h] = (count in (3, 4))
        else:
            newstate[h] = (count == 2)
    return newstate


clock = pygame.time.Clock()
ticktime = 0

state = {i: False for i in grid}

lastHovered = None

paused = False

changed = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
                changed = True
            if event.key == pygame.K_f:
                state = gol_step(state)
                changed = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            lastHovered = None
        if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
            mousehex = round(layout.to_hex(hex.Point(*event.pos)))
            lb, mb, rb = pygame.mouse.get_pressed()
            if mousehex != lastHovered and mousehex in grid:
                lastHovered = mousehex
                if lb:
                    state[mousehex] = True
                    changed = True
                if mb:
                    pos = mousehex
                    changed = True
                if rb:
                    state[mousehex] = False
                    changed = True

    if not paused:
        ticktime += clock.tick()
        if ticktime > 0:
            ticktime -= 120
            state = gol_step(state)
            changed = True
        if ticktime > 0:
            ticktime = 0
    else:
        clock.tick()

    if changed:
        changed = False
        win.fill((0, 0, 0))

        for h in grid:
            if state[h]:
                color = (150, 255, 255)
            else:
                if paused:
                    color = (100, 100, 100)
                else:
                    color = (60, 60, 60)
            pygame.draw.polygon(win, [i//2 for i in color],
                                layout.hex_corners(h, 1))
            pygame.draw.polygon(win, color,
                                layout.hex_corners(h, 0.75))

        pygame.display.flip()
