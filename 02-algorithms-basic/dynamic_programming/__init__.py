"""
Dynamic Programming Module

DP solves problems by breaking them into overlapping sub-problems and
storing their solutions to avoid recomputation.

Sub-modules:
- knapsack    : 0/1 knapsack, unbounded, partition, coin change.
- linear_dp   : 1D DP classics (stairs, house robber, LIS, Kadane).
- string_dp   : LCS, edit distance, regex matching.
- interval_dp : Matrix chain, optimal BST, burst balloons, stone game.
- state_dp    : TSP, grid paths, dungeon game.
"""

from . import knapsack
from . import linear_dp
from . import string_dp
from . import interval_dp
from . import state_dp

__all__ = ["knapsack", "linear_dp", "string_dp", "interval_dp", "state_dp"]
