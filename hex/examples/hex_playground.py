#!/usr/bin/env python3
import sys
import os
sys.path.append(os.curdir)
sys.path.append(os.pardir)
sys.path.append(os.pardir + os.sep + os.pardir)

if True:  # satisfy auto-formatter
    from hex import Point, Layout
    from hex import hexgrid
    import pygame
    import sys

try:
    from better_exceptions import hook
    hook()
except ImportError:
    pass

pygame.init()

layout = Layout(Layout.pointy, Point(30, 30), Point(0, 0), Point(1000, 1000))
targetlayout = Layout(layout.orientation, layout.scale,
                      layout.origin, layout.size)
grid = hexgrid.HexagonGrid(12)

# bounds = [math.inf, math.inf, -math.inf, -math.inf]

# for h in grid:
#     for p in layout.hex_corners(h):
#         bounds[0] = min(bounds[0], p[0])
#         bounds[1] = min(bounds[1], p[1])
#         bounds[2] = max(bounds[2], p[0])
#         bounds[3] = max(bounds[3], p[1])
#
# layout.origin = Point(-bounds[0], -bounds[1])
# targetlayout.origin = Point(-bounds[0], -bounds[1])

# win = pygame.display.set_mode((int(bounds[2]-bounds[0]),
#                                int(bounds[3]-bounds[1])))

# pos = round(layout.to_hex(Point(win.get_width()//2,
#                                 win.get_height()//2)))

win = pygame.display.set_mode((1000, 1000))

pos = grid.center


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


font_cache = {}


def getfont(size):
    if size in font_cache:
        return font_cache[size]
    else:
        font = pygame.font.SysFont(None, size)
        font_cache[size] = font
        return font


font = getfont(int(min(layout.scale)))


lastmousepos = None
mousepos = Point(0, 0)

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
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                lastmousepos = Point(event.pos)
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                lastmousepos = None
        if event.type == pygame.MOUSEWHEEL:
            winpos = Point(0, 0)
            centerhex = targetlayout.to_hex(winpos + mousepos)
            targetlayout.scale *= 1.25 ** event.y
            targetlayout.origin = Point(0, 0)
            winpos = targetlayout.from_hex(centerhex)
            targetlayout.origin = -Point(winpos) + mousepos
        if event.type == pygame.MOUSEMOTION:
            mousepos = Point(event.pos)
            if lastmousepos is not None:
                diff = Point(event.rel)
                targetlayout.origin += diff

    win.fill((0, 0, 0))

    for h in grid:
        if h in layout:
            color = [127+h.x*2, 127+h.y*2, 127+h.z*2]
            pygame.draw.polygon(win, color,
                                layout.hex_corners(h, margin=0.9))
            if h == pos:
                pygame.draw.polygon(win, (0, 0, 0),
                                    layout.hex_corners(h, margin=0.5))

    for i in range(6):
        target = pos.neighbor(i)
        if target in grid and target in layout:
            text = font.render(movement_text[i], True, (0, 0, 0))
            rect = text.get_rect()
            rect.center = layout.from_hex(target)
            win.blit(text, rect.topleft)

    pygame.display.flip()
    ms += clock.tick(30)
    layout.origin = layout.origin*0.6 + targetlayout.origin*0.4
    layout.scale = layout.scale*0.6 + targetlayout.scale*0.4
    font = getfont(int(min(layout.scale)))
