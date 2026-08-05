"""
Convex hull algorithms.

Contains:
- Andrew's monotone chain (O(n log n))
- Graham scan (O(n log n))
- Jarvis march / gift wrapping (O(nh), h = hull size)
"""

import math
from typing import List

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geometry_basics import Point, cross


# ======================================================================
# Andrew's monotone chain (most commonly used)
# ======================================================================

def andrew_monotone_chain(points: List[Point]) -> List[Point]:
    """
    Compute the convex hull of a set of 2D points using Andrew's
    monotone chain algorithm.

    Args:
        points: List of points.

    Returns:
        Convex hull vertices in counter-clockwise order, without the
        duplicate first point.  Includes collinear points on edges.

    Time:  O(n log n)
    Space: O(n)
    """
    n = len(points)
    if n <= 2:
        return list(points)

    # Sort by x, then y
    pts = sorted(points, key=lambda p: (p.x, p.y))

    # Build lower hull
    lower: List[Point] = []
    for p in pts:
        while len(lower) >= 2:
            a = lower[-2]
            b = lower[-1]
            if cross(b - a, p - a) <= 0:
                lower.pop()
            else:
                break
        lower.append(p)

    # Build upper hull
    upper: List[Point] = []
    for p in reversed(pts):
        while len(upper) >= 2:
            a = upper[-2]
            b = upper[-1]
            if cross(b - a, p - a) <= 0:
                upper.pop()
            else:
                break
        upper.append(p)

    # Remove last point of each (it's duplicated as the first of the other)
    hull = lower[:-1] + upper[:-1]
    return hull


# ======================================================================
# Graham scan
# ======================================================================

def graham_scan(points: List[Point]) -> List[Point]:
    """
    Compute the convex hull using Graham scan.

    Args:
        points: List of points.

    Returns:
        Convex hull vertices in counter-clockwise order.

    Time:  O(n log n)
    Space: O(n)
    """
    n = len(points)
    if n <= 2:
        return list(points)

    # Find the point with the smallest y (and smallest x if tie)
    p0 = min(points, key=lambda p: (p.y, p.x))

    # Sort by polar angle relative to p0, then by distance
    def polar_key(p: Point) -> tuple:
        dx = p.x - p0.x
        dy = p.y - p0.y
        angle = math.atan2(dy, dx)
        dist_sq = dx * dx + dy * dy
        return (angle, dist_sq)

    sorted_pts = sorted(points, key=polar_key)

    hull: List[Point] = []
    for p in sorted_pts:
        while len(hull) >= 2:
            a = hull[-2]
            b = hull[-1]
            if cross(b - a, p - a) <= 0:
                hull.pop()
            else:
                break
        hull.append(p)

    return hull


# ======================================================================
# Jarvis march (gift wrapping)
# ======================================================================

def jarvis_march(points: List[Point]) -> List[Point]:
    """
    Compute the convex hull using Jarvis march (gift wrapping).

    More efficient than O(n log n) when the hull size h is small.

    Args:
        points: List of points.

    Returns:
        Convex hull vertices in counter-clockwise order.

    Time:  O(n * h) where h = hull size
    Space: O(n)
    """
    n = len(points)
    if n <= 2:
        return list(points)

    # Find leftmost point
    start = min(points, key=lambda p: (p.x, p.y))

    hull: List[Point] = []
    cur = start

    while True:
        hull.append(cur)
        nxt = points[0]

        for p in points:
            if p == cur:
                continue
            # Find the most counter-clockwise point
            vec_to_nxt = nxt - cur
            vec_to_p = p - cur
            cp = cross(vec_to_nxt, vec_to_p)
            if cp < 0 or (cp == 0 and vec_to_p.length_squared() > vec_to_nxt.length_squared()):
                nxt = p

        cur = nxt
        if cur == start:
            break

    return hull


# ======================================================================
# Tests
# ======================================================================

if __name__ == "__main__":
    import sys

    all_pass = True

    # Test set: square with some internal points
    pts = [
        Point(0, 0), Point(2, 0), Point(2, 2), Point(0, 2),  # corners
        Point(1, 1), Point(0.5, 0.5),                        # interior
        Point(0, 1), Point(2, 1), Point(1, 0), Point(1, 2),  # edges
    ]
    expected_hull_set = {(0, 0), (2, 0), (2, 2), (0, 2)}

    def hull_set(hull):
        return {p.to_tuple() for p in hull}

    # --- Andrew ---
    hull_andrew = andrew_monotone_chain(pts)
    if hull_set(hull_andrew) != expected_hull_set or len(hull_andrew) != 4:
        print(f"FAIL andrew: {hull_andrew}")
        all_pass = False

    # --- Graham ---
    hull_graham = graham_scan(pts)
    if hull_set(hull_graham) != expected_hull_set or len(hull_graham) != 4:
        print(f"FAIL graham: {hull_graham}")
        all_pass = False

    # --- Jarvis ---
    hull_jarvis = jarvis_march(pts)
    if hull_set(hull_jarvis) != expected_hull_set or len(hull_jarvis) != 4:
        print(f"FAIL jarvis: {hull_jarvis}")
        all_pass = False

    # --- Edge cases ---
    # Two points
    hull2 = andrew_monotone_chain([Point(0, 0), Point(1, 1)])
    if len(hull2) != 2:
        print("FAIL two points")
        all_pass = False

    # Single point
    hull1 = andrew_monotone_chain([Point(5, 5)])
    if hull1 != [Point(5, 5)]:
        print("FAIL single point")
        all_pass = False

    # Collinear points
    collinear = [Point(0, 0), Point(1, 1), Point(2, 2), Point(3, 3)]
    hull_collinear = andrew_monotone_chain(collinear)
    if len(hull_collinear) != 2:
        print(f"FAIL collinear: {hull_collinear}")
        all_pass = False

    # Triangle
    tri_pts = [Point(0, 0), Point(3, 0), Point(1, 2), Point(1, 0.5)]
    hull_tri = andrew_monotone_chain(tri_pts)
    if len(hull_tri) != 3:
        print(f"FAIL triangle: {hull_tri}")
        all_pass = False

    if all_pass:
        print("All convex hull tests PASSED")
    sys.exit(0 if all_pass else 1)
