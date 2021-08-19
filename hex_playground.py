#!/usr/bin/env python3
import hex
import hexgrid
import pygame
import sys
import math

try:
    from better_exceptions import behook
    sys.excepthook = behook
except ImportError:
    pass

pygame.init()

layout = hex.Layout(hex.Layout.pointy, hex.Point(15, 15), hex.Point(0, 0))
grid = hexgrid.HexagonGrid(16)
NUM_MINES = len(list(grid))//10

bounds = [math.inf, math.inf, -math.inf, -math.inf]
MARGIN = 10

for h in grid:
    for p in layout.hex_corners(h):
        bounds[0] = min(bounds[0], p[0])
        bounds[1] = min(bounds[1], p[1])
        bounds[2] = max(bounds[2], p[0])
        bounds[3] = max(bounds[3], p[1])

layout.origin = hex.Point(-bounds[0]+MARGIN, -bounds[1]+MARGIN)

win = pygame.display.set_mode((int(bounds[2]-bounds[0]+MARGIN*2),
                               int(bounds[3]-bounds[1]+MARGIN*2)))

movement_text = "XDEWAZ"
movement = [
    pygame.K_x,
    pygame.K_d,
    pygame.K_e,
    pygame.K_w,
    pygame.K_a,
    pygame.K_z
]


def zero_spread(h):
    for i in range(6):
        tmp = h.neighbor(i)
        if tmp in grid and not revealed[tmp]:
            revealed[tmp] = 1
            if map[tmp] == 0:
                zero_spread(tmp)


mines = {i: False for i in grid}

placed = 0

while placed < NUM_MINES:
    tmp = grid.random()
    if not mines[tmp]:
        mines[tmp] = True
        placed += 1

map = {i: (-1 if mines[i]
           else sum([mines[tmp] for j in range(6)
                     if (tmp := i.neighbor(j)) in grid])
           ) for i in grid}


revealed = {i: 0 for i in grid}

while True:
    tmp = grid.random()
    if map[tmp] == 0:
        zero_spread(tmp)
        break

paused = False

changed = True

FONT = pygame.font.SysFont(None, int(max(layout.size)*1.3))

TEXT_COLOR = [
    "zero",
    (0,   0,   255),
    (0,   255, 0),
    (255, 0,   0),
    (150, 0,   255),
    (0,   0,   0),
    (150, 0,   0)
]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pass  # Regenerate map if won
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION):
            mousehex = round(layout.to_hex(hex.Point(*event.pos)))
            lb, mb, rb = pygame.mouse.get_pressed()
            if mousehex in grid:
                if lb and event.type == pygame.MOUSEBUTTONDOWN:
                    if revealed[mousehex] == 0:
                        revealed[mousehex] = 1
                        if map[mousehex] == 0:
                            zero_spread(mousehex)
                        changed = True
                if mb:
                    if revealed[mousehex] == 1:
                        # Reveal surroundings if satisfied
                        count = sum([revealed[tmp] == -1 for i in range(6)
                                     if (tmp := mousehex.neighbor(i)) in grid])
                        if count == map[mousehex]:
                            for i in range(6):
                                tmp = mousehex.neighbor(i)
                                if tmp in grid and revealed[tmp] == 0:
                                    revealed[tmp] = 1
                                    if map[tmp] == 0:
                                        zero_spread(tmp)
                            changed = True
                        # Mark all if it will satisfy
                        count = sum([revealed[tmp] != 1 for i in range(6)
                                     if (tmp := mousehex.neighbor(i)) in grid])
                        if count == map[mousehex]:
                            for i in range(6):
                                tmp = mousehex.neighbor(i)
                                if tmp in grid and revealed[tmp] == 0:
                                    revealed[tmp] = -1
                            changed = True
                if rb and event.type == pygame.MOUSEBUTTONDOWN:
                    if revealed[mousehex] != 1:
                        revealed[mousehex] = -revealed[mousehex]-1
                        changed = True

    if changed:
        changed = False
        win.fill((0, 0, 0))

        for h in grid:
            if revealed[h] == 1:
                if map[h] == -1:
                    color = (255, 150, 150)
                else:
                    color = (150, 150, 150)
            elif revealed[h] == -1:
                color = (150, 200, 150)
            else:
                color = (100, 100, 100)
            pygame.draw.polygon(win, [i//2 for i in color],
                                layout.hex_corners(h, 0.95))
            pygame.draw.polygon(win, color,
                                layout.hex_corners(h, 0.75))
            if revealed[h] == 1 and map[h] > 0:
                text = FONT.render(str(map[h]), True, TEXT_COLOR[map[h]])
                rect = text.get_rect()
                rect.center = layout.from_hex(h)
                win.blit(text, rect.topleft)

        pygame.display.flip()
