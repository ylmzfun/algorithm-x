"""Computational geometry package."""

from .geometry_basics import Point, dot, cross, distance, angle, polygon_area, point_in_polygon
from .convex_hull import andrew_monotone_chain, graham_scan, jarvis_march
from .line_intersection import segments_intersect, segment_intersection_sweep
from .closest_points import closest_pair_of_points

__all__ = [
    # Basics
    "Point",
    "dot",
    "cross",
    "distance",
    "angle",
    "polygon_area",
    "point_in_polygon",
    # Convex Hull
    "andrew_monotone_chain",
    "graham_scan",
    "jarvis_march",
    # Line Intersection
    "segments_intersect",
    "segment_intersection_sweep",
    # Closest Points
    "closest_pair_of_points",
]
