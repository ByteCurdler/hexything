#!/usr/bin/env python3
import sys
import os
sys.path.append(os.curdir)
sys.path.append(os.pardir)
sys.path.append(os.pardir + os.sep + os.pardir)

if True:  # satisfy auto-formatter
    import hex
    from hex import hexgrid
    import pygame
    import math

try:
    from better_exceptions import behook
    sys.excepthook = behook
except ImportError:
    pass

pygame.init()
pygame.font.init()

layout = hex.Layout(hex.Layout.pointy, hex.Point(6, 6), hex.Point(0, 0))
grid = hexgrid.HexagonGrid(40)

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

head = round(layout.to_hex(hex.Point(win.get_width()//2,
                                     win.get_height()//2)))

dir = 0

tail = [head]

length = 3

food = grid.random()

movement_text = "XDWQAZ"
movement = [
    pygame.K_x,
    pygame.K_d,
    pygame.K_w,
    pygame.K_q,
    pygame.K_a,
    pygame.K_z
]

movement_text = "XDEWAZ"
movement = [
    pygame.K_x,
    pygame.K_d,
    pygame.K_e,
    pygame.K_w,
    pygame.K_a,
    pygame.K_z
]

movement_text = "XSWQAZ"
movement = [
    pygame.K_x,
    pygame.K_s,
    pygame.K_w,
    pygame.K_q,
    pygame.K_a,
    pygame.K_z
]

movement_text = "369741"
movement = [
    pygame.K_KP_3,
    pygame.K_KP_6,
    pygame.K_KP_9,
    pygame.K_KP_7,
    pygame.K_KP_4,
    pygame.K_KP_1
]


def ai():
    visited = [head]
    frontier = [(new, i, [new]) for i in range(6)
                if (i+3) % 6 != dir and (new := head.neighbor(i)) not in tail]
    done = 0
    while frontier and frontier[0][0] != food:
        item = frontier.pop(0)
        for i in range(6):
            new = item[0].neighbor(i)
            if (new in grid and new not in visited
                    and new not in tail[len(item[2]):]
                    + item[2][min(0, len(item[2]))-length:]):
                visited.append(new)
                frontier.append((new, item[1], item[2] + [new]))
        done += 1
    if frontier:
        return frontier[0][1]
    else:
        return dir


FONT = pygame.font.Font(None, int(min(layout.size)))

while True:
    # Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    # Logic

    dir = ai()

    head = head.neighbor(dir)
    if head in tail or head not in grid:
        break
    tail.append(head)
    if head == food:
        length += 1
        while True:
            food = grid.random()
            if food not in tail:
                break
    if len(tail) > length:
        tail = tail[1:]

    # Render
    win.fill((0, 0, 0))

    for h in grid:
        if h in tail:
            color = (0, 255, 0)
        elif h == food:
            color = (255, 0, 0)
        else:
            color = (127, 127, 127)
        pygame.draw.polygon(win, color,
                            layout.hex_corners(h))
        pygame.draw.polygon(win, (0, 0, 0),
                            layout.hex_corners(h), width=2)

    pygame.display.flip()

pygame.quit()
sys.exit()
