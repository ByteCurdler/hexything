#!/usr/bin/env python3

import hex
import random


class Grid:
    def __init__(self):
        pass

    def __init_subclass__(self):
        self.__contains__ = self.valid

    def valid(self, hex):
        """
        Returns True if a hex can be in this grid.
        """
        return True
    __contains__ = valid

    def __iter__(self, hex):
        """
        Returns an iterable looping through all hexes in this grid
        """
        return []

    def random(self) -> hex.Hex:
        return random.choice(list(self))


class RectangleGrid(Grid):
    def __init__(self, width, height):
        self.width, self.height = width, height

    def valid(self, hex):
        return (hex.y in range(self.height)
                and hex.x in range(0-(hex.y//2), self.width-(hex.y//2)))

    def __iter__(self):
        for y in range(self.height):
            for x in range(0-(y//2), self.width-(y//2)):
                yield hex.Hex(x, y)


class RhombusGrid(Grid):
    def __init__(self, width, height):
        self.width, self.height = width, height

    def valid(self, hex):
        return hex.y in range(self.height) and hex.x in range(self.width)

    def __iter__(self):
        for y in range(self.height):
            for x in range(self.width):
                yield hex.Hex(x, y)


class HexagonGrid(Grid):
    def __init__(self, radius):
        self.radius = radius
        self.diameter = radius*2 - 1
        self.center = hex.Hex(radius-1, radius-1)

    def valid(self, hex):
        return (hex.y in range(self.diameter)
                and hex.x in range(max(0, self.radius - hex.y - 1),
                                   min(self.diameter,
                                       self.diameter + self.radius - hex.y - 1)
                                   ))

    def __iter__(self):
        for y in range(self.diameter):
            for x in range(max(0, self.radius - y - 1),
                           min(self.diameter,
                               self.diameter + self.radius - y - 1)
                           ):
                yield hex.Hex(x, y)
