"""
Closest pair of points — divide and conquer algorithm.

Finds the pair of points with the minimum Euclidean distance in O(n log n) time.
"""

import math
from typing import List, Tuple

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geometry_basics import Point, distance


def closest_pair_of_points(points: List[Point]) -> Tuple[float, Point, Point]:
    """
    Find the closest pair of points using divide and conquer.

    Args:
        points: List of 2D points (at least 2 points required).

    Returns:
        (min_distance, p1, p2) — the two closest points and their distance.

    Time:  O(n log n)
    Space: O(n)

    Raises:
        ValueError: If fewer than 2 points are provided.
    """
    n = len(points)
    if n < 2:
        raise ValueError("At least 2 points are required")

    # Sort by x-coordinate
    pts_x = sorted(points, key=lambda p: p.x)
    # Pre-sort by y for the merge step
    pts_y = sorted(points, key=lambda p: p.y)

    return _closest_pair(pts_x, pts_y)


def _dist_sq(a: Point, b: Point) -> float:
    """Squared distance (to avoid sqrt in comparisons)."""
    dx = a.x - b.x
    dy = a.y - b.y
    return dx * dx + dy * dy


def _closest_pair(
    pts_x: List[Point], pts_y: List[Point]
) -> Tuple[float, Point, Point]:
    """
    Recursive divide-and-conquer for closest pair.

    Args:
        pts_x: Points sorted by x.
        pts_y: Points sorted by y.

    Returns:
        (min_dist, p1, p2).
    """
    n = len(pts_x)

    # Base cases
    if n == 2:
        d = distance(pts_x[0], pts_x[1])
        return (d, pts_x[0], pts_x[1])
    if n == 3:
        # Brute force for 3 points
        p0, p1, p2 = pts_x
        d01 = distance(p0, p1)
        d02 = distance(p0, p2)
        d12 = distance(p1, p2)
        min_d = min(d01, d02, d12)
        if min_d == d01:
            return (d01, p0, p1)
        elif min_d == d02:
            return (d02, p0, p2)
        else:
            return (d12, p1, p2)

    # Divide
    mid = n // 2
    mid_x = pts_x[mid].x

    left_x = pts_x[:mid]
    right_x = pts_x[mid:]

    # Partition pts_y into left and right subsets
    left_y = [p for p in pts_y if p.x < mid_x or (p.x == mid_x and p in set(left_x))]
    right_y = [p for p in pts_y if p not in set(left_y)]

    # Conquer
    d_left, p1_left, p2_left = _closest_pair(left_x, left_y)
    d_right, p1_right, p2_right = _closest_pair(right_x, right_y)

    if d_left < d_right:
        min_d, p1, p2 = d_left, p1_left, p2_left
    else:
        min_d, p1, p2 = d_right, p1_right, p2_right

    # Combine: check points near the dividing line
    # Build strip of points within min_d of the midline
    strip = [p for p in pts_y if abs(p.x - mid_x) < min_d]

    # Check at most 7 points ahead in the strip (by geometry property)
    for i in range(len(strip)):
        j = i + 1
        while j < len(strip) and (strip[j].y - strip[i].y) < min_d:
            d = distance(strip[i], strip[j])
            if d < min_d:
                min_d = d
                p1, p2 = strip[i], strip[j]
            j += 1

    return (min_d, p1, p2)


# ======================================================================
# Tests
# ======================================================================

if __name__ == "__main__":
    import sys

    all_pass = True

    # --- Simple pair ---
    pts1 = [Point(0, 0), Point(1, 1), Point(3, 4)]
    d, a, b = closest_pair_of_points(pts1)
    if abs(d - math.sqrt(2)) > 1e-9:
        print(f"FAIL simple pair distance: {d}")
        all_pass = False

    # --- Multiple points ---
    pts2 = [
        Point(2, 3), Point(12, 30), Point(40, 50),
        Point(5, 1), Point(12, 10), Point(3, 4),
    ]
    d2, a2, b2 = closest_pair_of_points(pts2)
    # Brute force check
    min_bf = float("inf")
    for i in range(len(pts2)):
        for j in range(i + 1, len(pts2)):
            min_bf = min(min_bf, distance(pts2[i], pts2[j]))
    if abs(d2 - min_bf) > 1e-9:
        print(f"FAIL m-pair: d={d2}, brute={min_bf}")
        all_pass = False

    # --- Exactly 2 points ---
    pts3 = [Point(0, 0), Point(3, 4)]
    d3, a3, b3 = closest_pair_of_points(pts3)
    if abs(d3 - 5.0) > 1e-9:
        print(f"FAIL 2 points: {d3}")
        all_pass = False

    # --- Many collinear points ---
    pts4 = [Point(0, 0), Point(1, 0), Point(1.5, 0), Point(3, 0), Point(3.5, 0)]
    d4, a4, b4 = closest_pair_of_points(pts4)
    if abs(d4 - 0.5) > 1e-9:
        print(f"FAIL collinear: {d4}")
        all_pass = False

    # --- All points at same position ---
    pts5 = [Point(1, 1), Point(1, 1), Point(2, 2)]
    d5, a5, b5 = closest_pair_of_points(pts5)
    if abs(d5 - 0.0) > 1e-9:
        print(f"FAIL identical: {d5}")
        all_pass = False

    if all_pass:
        print("All closest pair tests PASSED")
    sys.exit(0 if all_pass else 1)
