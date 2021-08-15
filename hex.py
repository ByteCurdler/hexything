#!/usr/bin/env python3
from collections import namedtuple
import math
from pygame import Vector2 as Point

# Point = namedtuple("Point", ["x", "y"])
Cube = namedtuple("Cube", ["x", "y", "z"])


class Hex:

    NEIGHBOR_NW = 0
    NEIGHBOR_NE = 1
    NEIGHBOR_E = 2
    NEIGHBOR_SE = 3
    NEIGHBOR_SW = 4
    NEIGHBOR_W = 5

    DIAGONAL_NW = 0
    DIAGONAL_N = 1
    DIAGONAL_NE = 2
    DIAGONAL_SE = 3
    DIAGONAL_S = 4
    DIAGONAL_SW = 5

    hex_grid = None

    def __init__(self, x=..., y=..., z=...):
        if type(x) in (list, tuple, Cube):
            x, y, z = x
        elif [x, y, z].count(...) > 1:
            raise ValueError("Two or more of x,y,z must be defined, "
                             "or x must be Cube, tuple or list")
        elif x is ...:
            x = -y-z
        elif y is ...:
            y = -x-z
        elif z is ...:
            z = -x-y
        else:
            assert x + y + z == 0, "x + y + z must be 0"
        self.x, self.y, self.z = x, y, z
        # self.data = Hex.hex_grid.get_data(self.key())

    def key(self):
        return "{:+}{:+}{:+}".format(self.x, self.y, self.z)

    def __hash__(self):
        return hash(self.key())

    def __add__(self, other):
        if type(other) is Hex:
            return Hex(self.x + other.x, self.y + other.y, self.z + other.z)
        elif type(other) is int:
            return Hex(self.x + other, self.y + other, self.z + other)
        else:
            return NotImplemented

    def __sub__(self, other):
        if type(other) is Hex:
            return Hex(self.x - other.x, self.y - other.y, self.z - other.z)
        elif type(other) is int:
            return Hex(self.x - other, self.y - other, self.z - other)
        else:
            return NotImplemented

    def __mult__(self, other):
        if type(other) is int:
            return Hex(self.x * other, self.y * other, self.z * other)
        else:
            return NotImplemented

    def __str__(self):
        return f"Hex({self.x}, {self.y}, {self.z})"

    __repr__ = __str__

    def rotate_left(self, n=1):
        if n > 1:
            return self.rotate_left().rotate_left(n=n-1)
        return Hex(-self.z, -self.x, -self.y)

    def rotate_right(self, n=1):
        if n > 1:
            return self.rotate_right().rotate_right(n=n-1)
        return Hex(-self.y, -self.z, -self.x)

    def neighbor(self, direction):
        return self + Hex.hex_directions[direction]

    def diagonal(self, direction):
        return self.add(Hex.hex_diagonals[direction])

    def magnitude(self):
        return (abs(self.x) + abs(self.y) + abs(self.z)) // 2

    def distance(self, other):
        return (self - other).magnitude()

    def __eq__(self, other):
        # If two match, the third will too.
        return type(other) is Hex and self.x == other.x and self.y == other.y

    def __bool__(self):
        # If two are zero, the third will be too.
        return self.x or self.y

    def __ne__(self, other):
        # If two match, the third will too.
        return type(other) is not Hex or self.x != other.x or self.y != other.y

    def __neg__(self, other):
        return Hex(-self.x, -self.y, -self.z)

    def __round__(self):
        xi = int(round(self.x))
        yi = int(round(self.y))
        zi = int(round(self.z))
        x_diff = abs(xi - self.x)
        y_diff = abs(yi - self.y)
        z_diff = abs(zi - self.z)
        if x_diff > y_diff and x_diff > z_diff:
            xi = -yi - zi
        else:
            if y_diff > z_diff:
                yi = -xi - zi
            else:
                zi = -xi - yi
        return Hex(xi, yi, zi)

    round = __round__

    @classmethod
    def lerp(cls, a, b, t):
        return cls(a.x * (1.0 - t) + b.x * t,
                   a.y * (1.0 - t) + b.y * t,
                   a.z * (1.0 - t) + b.z * t)


Hex.hex_directions = [
    Hex(0, 1, -1),
    Hex(1, 0, -1),
    Hex(1, -1, 0),
    Hex(0, -1, 1),
    Hex(-1, 0, 1),
    Hex(-1, 1, 0),
]
Hex.hex_diagonals = [
    Hex(-1, 2, -1),
    Hex(1, 1, -2),
    Hex(2, -1, -1),
    Hex(1, -2, 1),
    Hex(-1, -1, 2),
    Hex(-2, 1, 1),
]

# def hex_linedraw(a, b):
#     N = hex_distance(a, b)
#     a_nudge = Hex(a.q + 1e-06, a.r + 1e-06, a.s - 2e-06)
#     b_nudge = Hex(b.q + 1e-06, b.r + 1e-06, b.s - 2e-06)
#     results = []
#     step = 1.0 / max(N, 1)
#     for i in range(0, N + 1):
#         results.append(hex_round(hex_lerp(a_nudge, b_nudge, step * i)))
#     return results
#
#
#
#
#
Orientation = namedtuple("Orientation", ["f0", "f1", "f2", "f3",
                                         "b0", "b1", "b2", "b3",
                                         "start_angle"])
#
#
#
#


class Layout:
    pointy = Orientation(math.sqrt(3.0), math.sqrt(3.0) / 2.0,
                         0.0, 3.0 / 2.0,
                         math.sqrt(3.0) / 3.0, -1.0 / 3.0,
                         0.0, 2.0 / 3.0,
                         0.5)
    flat = Orientation(3.0 / 2.0, 0.0,
                       math.sqrt(3.0) / 2.0, math.sqrt(3.0),
                       2.0 / 3.0, 0.0,
                       -1.0 / 3.0, math.sqrt(3.0) / 3.0,
                       0.0)

    def __init__(self, orientation, size, origin=Point(0, 0)):
        self.orientation, self.size, self.origin = orientation, size, origin

    def from_hex(self, hex):
        M = self.orientation
        size = self.size
        origin = self.origin
        x = (M.f0 * hex.x + M.f1 * hex.y) * size.x
        y = (M.f2 * hex.x + M.f3 * hex.y) * size.y
        return Point(x + origin.x, y + origin.y)

    def to_hex(self, pixel):
        M = self.orientation
        size = self.size
        origin = self.origin
        pt = Point((pixel.x - origin.x) / size.x,
                   (pixel.y - origin.y) / size.y)
        x = M.b0 * pt.x + M.b1 * pt.y
        y = M.b2 * pt.x + M.b3 * pt.y
        return Hex(x, y)

    def hex_corner_offset(self, corner, margin=1):
        M = self.orientation
        size = self.size * margin
        angle = 2.0 * math.pi * (M.start_angle - corner) / 6.0
        return Point(size.x * math.cos(angle), size.y * math.sin(angle))

    def hex_corners(self, hex, margin=1):
        corners = []
        center = self.from_hex(hex)
        for i in range(0, 6):
            offset = self.hex_corner_offset(i, margin)
            corners.append(Point(center.x + offset.x, center.y + offset.y))
        return corners
#
#
#
#
# Tests


if __name__ == "__main__":
    def equal(name, a, b):
        print(f"\033[1m{name.center(30)}"
              + ("\033[32mSUCCESS" if a == b else "\033[31mFAIL")
              + "\033[0m")

    # def equal_hex_array(name, a, b):
    #     equal_int(name, len(a), len(b))
    #     for i in range(0, len(a)):
    #         equal_hex(name, a[i], b[i])

    def test_hex_arithmetic():
        equal("hex + hex", Hex(4, -10, 6), Hex(1, -3, 2) + Hex(3, -7, 4))
        equal("hex - hex", Hex(-2, 4, -2), Hex(1, -3, 2) - Hex(3, -7, 4))

    # def test_hex_direction():
    #     equal_hex("hex_direction", Hex(0, -1, 1), hex_direction(2))
    #
    # def test_hex_neighbor():
    #     equal_hex("hex_neighbor", Hex(1, -3, 2),
    #               hex_neighbor(Hex(1, -2, 1), 2))
    #
    # def test_hex_diagonal():
    #     equal_hex("hex_diagonal", Hex(-1, -1, 2),
    #               hex_diagonal_neighbor(Hex(1, -2, 1), 3))
    #
    def test_hex_distance():
        equal("hex.distance(hex)", 7, Hex(3, -7, 4).distance(Hex(0, 0, 0)))

    def test_hex_rotate():
        equal("hex.rotate_right()",
              Hex(1, -3, 2).rotate_right(), Hex(3, -2, -1))
        equal("hex.rotate_left()", Hex(1, -3, 2).rotate_left(), Hex(-2, -1, 3))

    def test_hex_round():
        a = Hex(0.0, 0.0, 0.0)
        b = Hex(1.0, -1.0, 0.0)
        c = Hex(0.0, -1.0, 1.0)
        equal("hex.round() 1", Hex(5, -10, 5),
              round(Hex.lerp(Hex(0.0, 0.0, 0.0), Hex(10.0, -20.0, 10.0), 0.5)))
        equal("hex.round() 2", round(a),
              round(Hex.lerp(a, b, 0.499)))
        equal("hex.round() 3", round(b),
              round(Hex.lerp(a, b, 0.501)))
        equal("hex.round() 4", round(a),
              round(Hex(a.x * 0.4 + b.x * 0.3 + c.x * 0.3,
                        a.y * 0.4 + b.y * 0.3 + c.y * 0.3,
                        a.z * 0.4 + b.z * 0.3 + c.z * 0.3)))
        equal("hex.round() 5", round(c),
              round(Hex(a.x * 0.25 + b.x * 0.25 + c.x * 0.5,
                        a.y * 0.25 + b.y * 0.25 + c.y * 0.5,
                        a.z * 0.25 + b.z * 0.25 + c.z * 0.5)))
    #

    # def test_hex_linedraw():
    #     equal_hex_array("hex_linedraw", [Hex(0, 0, 0), Hex(0, -1, 1),
    #                                      Hex(0, -2, 2), Hex(1, -3, 2),
    #                                      Hex(1, -4, 3), Hex(1, -5, 4)],
    #                     hex_linedraw(Hex(0, 0, 0), Hex(1, -5, 4)))
    #
    def test_layout():
        h = Hex(3, 4, -7)
        flat = Layout(Layout.flat, Point(10.0, 15.0), Point(35.0, 71.0))
        equal("layout flat", h, round(flat.to_hex(flat.from_hex(h))))
        pointy = Layout(Layout.pointy, Point(
            10.0, 15.0), Point(35.0, 71.0))
        equal("layout pointy", h, round(pointy.to_hex(pointy.from_hex(h))))
    #
    # def test_offset_roundtrip():
    #     a = Hex(3, 4, -7)
    #     b = OffsetCoord(1, -3)
    #     equal_hex("conversion_roundtrip even-q", a,
    #               qoffset_to_cube(EVEN, qoffset_from_cube(EVEN, a)))
    #     equal_offsetcoord("conversion_roundtrip even-q", b,
    #                       qoffset_from_cube(EVEN, qoffset_to_cube(EVEN, b)))
    #     equal_hex("conversion_roundtrip odd-q", a,
    #               qoffset_to_cube(ODD, qoffset_from_cube(ODD, a)))
    #     equal_offsetcoord("conversion_roundtrip odd-q", b,
    #                       qoffset_from_cube(ODD, qoffset_to_cube(ODD, b)))
    #     equal_hex("conversion_roundtrip even-r", a,
    #               roffset_to_cube(EVEN, roffset_from_cube(EVEN, a)))
    #     equal_offsetcoord("conversion_roundtrip even-r", b,
    #                       roffset_from_cube(EVEN, roffset_to_cube(EVEN, b)))
    #     equal_hex("conversion_roundtrip odd-r", a,
    #               roffset_to_cube(ODD, roffset_from_cube(ODD, a)))
    #     equal_offsetcoord("conversion_roundtrip odd-r", b,
    #                       roffset_from_cube(ODD, roffset_to_cube(ODD, b)))
    #
    # def test_offset_from_cube():
    #     equal_offsetcoord("offset_from_cube even-q", OffsetCoord(1,
    #                                                              3),
    #                       qoffset_from_cube(EVEN, Hex(1, 2, -3)))
    #     equal_offsetcoord("offset_from_cube odd-q", OffsetCoord(1,
    #                                                             2),
    #                       qoffset_from_cube(ODD, Hex(1, 2, -3)))
    #
    # def test_offset_to_cube():
    #     equal_hex("offset_to_cube even-", Hex(1, 2, -3),
    #               qoffset_to_cube(EVEN, OffsetCoord(1, 3)))
    #     equal_hex("offset_to_cube odd-q", Hex(1, 2, -3),
    #               qoffset_to_cube(ODD, OffsetCoord(1, 2)))
    #
    # def test_doubled_roundtrip():
    #     a = Hex(3, 4, -7)
    #     b = DoubledCoord(1, -3)
    #     equal_hex("conversion_roundtrip doubled-q", a,
    #               qdoubled_to_cube(qdoubled_from_cube(a)))
    #     equal_doubledcoord("conversion_roundtrip doubled-q",
    #                        b, qdoubled_from_cube(qdoubled_to_cube(b)))
    #     equal_hex("conversion_roundtrip doubled-r", a,
    #               rdoubled_to_cube(rdoubled_from_cube(a)))
    #     equal_doubledcoord("conversion_roundtrip doubled-r",
    #                        b, rdoubled_from_cube(rdoubled_to_cube(b)))
    #
    # def test_doubled_from_cube():
    #     equal_doubledcoord("doubled_from_cube doubled-q",
    #                        DoubledCoord(1, 5),
    #                        qdoubled_from_cube(Hex(1, 2, -3)))
    #     equal_doubledcoord("doubled_from_cube doubled-r",
    #                        DoubledCoord(4, 2)
    #                        rdoubled_from_cube(Hex(1, 2, -3)))
    #
    # def test_doubled_to_cube():
    #     equal_hex("doubled_to_cube doubled-q", Hex(1, 2, -3),
    #               qdoubled_to_cube(DoubledCoord(1, 5)))
    #     equal_hex("doubled_to_cube doubled-r", Hex(1, 2, -3),
    #               rdoubled_to_cube(DoubledCoord(4, 2)))

    def test_all():
        test_hex_arithmetic()
        # test_hex_direction()
        # test_hex_neighbor()
        # test_hex_diagonal()
        test_hex_distance()
        test_hex_rotate()
        test_hex_round()
        # test_hex_linedraw()
        test_layout()
        # test_offset_roundtrip()
        # test_offset_from_cube()
        # test_offset_to_cube()
        # test_doubled_roundtrip()
        # test_doubled_from_cube()
        # test_doubled_to_cube()

    test_all()
