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

layout = hex.Layout(hex.Layout.pointy, hex.Point(20, 20), hex.Point(0, 0))
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

pos = round(layout.to_hex(hex.Point(win.get_width()//2,
                                    win.get_height()//2)))

ms = 0
clock = pygame.time.Clock()

movement_text = "XDEWAZ"
movement = [
    pygame.K_x,
    pygame.K_d,
    pygame.K_e,
    pygame.K_w,
    pygame.K_a,
    pygame.K_z
]


FONT = pygame.font.SysFont(None, 20)

while True:
    changed = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key in movement:
                new = pos.neighbor(movement.index(event.key))
                if new in grid:
                    pos = new

    win.fill((0, 0, 0))

    for h in grid:
        if h != pos:
            width = 0
        else:
            width = 2
        color = [150, 150, 150]
        if h.x > grid.center.x:
            color[0] = 255
        if h.y > grid.center.y:
            color[1] = 255
        if h.z > grid.center.z:
            color[2] = 255
        pygame.draw.polygon(win, color,
                            layout.hex_corners(h, margin=0.9), width=width)

    for i in range(6):
        target = pos.neighbor(i)
        if target in grid:
            text = FONT.render(movement_text[i], True, (0, 0, 0))
            rect = text.get_rect()
            rect.center = layout.from_hex(target)
            win.blit(text, rect.topleft)

    pygame.display.flip()
    ms += clock.tick()
