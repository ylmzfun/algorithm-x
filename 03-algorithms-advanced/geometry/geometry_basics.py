"""
Basic computational geometry types and operations.

Contains:
- Point / Vector class (2D)
- Dot product, cross product
- Distance, angle
- Polygon area (shoelace formula)
- Point in polygon test (ray casting)
"""

import math
from typing import List, Tuple


class Point:
    """
    A 2D point / vector with x and y coordinates.

    Supports basic vector operations: addition, subtraction, scaling.
    """

    __slots__ = ("x", "y")

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Point") -> "Point":
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> "Point":
        return Point(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> "Point":
        return self.__mul__(scalar)

    def __truediv__(self, scalar: float) -> "Point":
        return Point(self.x / scalar, self.y / scalar)

    def __neg__(self) -> "Point":
        return Point(-self.x, -self.y)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def length_squared(self) -> float:
        """Return the squared Euclidean length."""
        return self.x * self.x + self.y * self.y

    def length(self) -> float:
        """Return the Euclidean length."""
        return math.sqrt(self.length_squared())

    def to_tuple(self) -> Tuple[float, float]:
        """Return (x, y) tuple representation."""
        return (self.x, self.y)


# ---------------------------------------------------------------------------
# Vector operations
# ---------------------------------------------------------------------------

def dot(a: Point, b: Point) -> float:
    """
    Compute the dot product a · b = a.x * b.x + a.y * b.y.

    Args:
        a, b: Two points/vectors.

    Returns:
        Dot product (scalar).

    Time: O(1)
    """
    return a.x * b.x + a.y * b.y


def cross(a: Point, b: Point) -> float:
    """
    Compute the 2D cross product a × b = a.x * b.y - a.y * b.x.

    The sign indicates orientation:
      > 0 → counter-clockwise
      < 0 → clockwise
      = 0 → collinear

    Args:
        a, b: Two points/vectors.

    Returns:
        Cross product (scalar).

    Time: O(1)
    """
    return a.x * b.y - a.y * b.x


# ---------------------------------------------------------------------------
# Geometric properties
# ---------------------------------------------------------------------------

def distance(a: Point, b: Point) -> float:
    """
    Compute the Euclidean distance between two points.

    Args:
        a, b: Two points.

    Returns:
        Euclidean distance.

    Time: O(1)
    """
    return (a - b).length()


def angle(a: Point, b: Point, c: Point) -> float:
    """
    Compute the angle ∠ABC (at point b) in radians.

    Uses the law of cosines on vectors ba = a - b and bc = c - b.

    Args:
        a, b, c: Three points.

    Returns:
        Angle in radians, in [0, π].

    Time: O(1)
    """
    ba = a - b
    bc = c - b
    cos_theta = dot(ba, bc) / (ba.length() * bc.length())
    # Clamping due to floating point
    cos_theta = max(-1.0, min(1.0, cos_theta))
    return math.acos(cos_theta)


# ---------------------------------------------------------------------------
# Polygon area (Shoelace formula)
# ---------------------------------------------------------------------------

def polygon_area(polygon: List[Point]) -> float:
    """
    Compute the area of a simple polygon using the shoelace formula.

    The polygon vertices must be given in order (clockwise or counter-
    clockwise).  The result is the absolute area.

    Args:
        polygon: List of vertices in order.

    Returns:
        Absolute area of the polygon.

    Time:  O(n), where n = number of vertices
    Space: O(1)
    """
    n = len(polygon)
    if n < 3:
        return 0.0

    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += cross(polygon[i], polygon[j])
    return abs(area) / 2.0


# ---------------------------------------------------------------------------
# Point in polygon (Ray casting)
# ---------------------------------------------------------------------------

def point_in_polygon(point: Point, polygon: List[Point]) -> bool:
    """
    Determine whether a point lies inside a simple polygon using the
    ray-casting (even-odd) algorithm.

    A ray is cast to the right (+x direction).  If it crosses the polygon
    boundary an odd number of times, the point is inside.

    Args:
        point: The query point.
        polygon: List of polygon vertices in order.

    Returns:
        True if the point is inside (or on the boundary), False otherwise.

    Time:  O(n)
    Space: O(1)
    """
    n = len(polygon)
    if n < 3:
        return False

    inside = False
    for i in range(n):
        a = polygon[i]
        b = polygon[(i + 1) % n]

        # Check if point lies on the segment (floating-point tolerance)
        if distance(a, point) + distance(point, b) - distance(a, b) < 1e-9:
            return True

        # Ray casting
        # Check if the edge crosses the horizontal ray at point.y
        cond1 = (a.y > point.y) != (b.y > point.y)
        if cond1:
            # Compute the x-coordinate of the intersection
            x_intersect = a.x + (point.y - a.y) * (b.x - a.x) / (b.y - a.y)
            if point.x < x_intersect:
                inside = not inside

    return inside


# ======================================================================
# Tests
# ======================================================================

if __name__ == "__main__":
    import sys

    all_pass = True

    # --- Point operations ---
    p1 = Point(3, 4)
    p2 = Point(1, 2)
    if p1.length() != 5.0:
        print(f"FAIL length: {p1.length()}")
        all_pass = False
    if p1 + p2 != Point(4, 6):
        print(f"FAIL add: {p1 + p2}")
        all_pass = False
    if p1 - p2 != Point(2, 2):
        print(f"FAIL sub: {p1 - p2}")
        all_pass = False

    # --- Dot product ---
    if dot(Point(1, 0), Point(0, 1)) != 0.0:
        print("FAIL dot orthogonal")
        all_pass = False
    if dot(Point(1, 0), Point(1, 0)) != 1.0:
        print("FAIL dot parallel")
        all_pass = False

    # --- Cross product ---
    if cross(Point(1, 0), Point(0, 1)) != 1.0:
        print("FAIL cross ccw")
        all_pass = False
    if cross(Point(0, 1), Point(1, 0)) != -1.0:
        print("FAIL cross cw")
        all_pass = False
    if cross(Point(1, 0), Point(2, 0)) != 0.0:
        print("FAIL cross collinear")
        all_pass = False

    # --- Distance ---
    d = distance(Point(0, 0), Point(3, 4))
    if abs(d - 5.0) > 1e-9:
        print(f"FAIL distance: {d}")
        all_pass = False

    # --- Angle ---
    ang = angle(Point(1, 0), Point(0, 0), Point(0, 1))
    if abs(ang - math.pi / 2) > 1e-9:
        print(f"FAIL angle: {ang}")
        all_pass = False

    # --- Polygon area ---
    square = [Point(0, 0), Point(2, 0), Point(2, 2), Point(0, 2)]
    area = polygon_area(square)
    if abs(area - 4.0) > 1e-9:
        print(f"FAIL area square: {area}")
        all_pass = False

    triangle = [Point(0, 0), Point(4, 0), Point(0, 3)]
    area2 = polygon_area(triangle)
    if abs(area2 - 6.0) > 1e-9:
        print(f"FAIL area triangle: {area2}")
        all_pass = False

    # --- Point in polygon ---
    # Square from (0,0) to (2,2)
    if not point_in_polygon(Point(1, 1), square):
        print("FAIL point_in_polygon center")
        all_pass = False
    if point_in_polygon(Point(3, 3), square):
        print("FAIL point_in_polygon outside")
        all_pass = False
    if not point_in_polygon(Point(0, 0), square):
        print("FAIL point_in_polygon vertex")
        all_pass = False

    if all_pass:
        print("All geometry basics tests PASSED")
    sys.exit(0 if all_pass else 1)
