"""
Greedy Algorithms Module

Greedy algorithms make the locally optimal choice at each step with the
hope of finding a global optimum.
"""

from .greedy_algorithms import (
    activity_selection,
    fractional_knapsack,
    huffman_coding,
    job_sequencing,
    coin_change_greedy,
)

from .interval_problems import (
    merge_intervals,
    insert_interval,
    erase_overlapping_intervals,
    min_arrows_burst_balloons,
    meeting_rooms,
    meeting_rooms_ii,
)

__all__ = [
    "activity_selection",
    "fractional_knapsack",
    "huffman_coding",
    "job_sequencing",
    "coin_change_greedy",
    "merge_intervals",
    "insert_interval",
    "erase_overlapping_intervals",
    "min_arrows_burst_balloons",
    "meeting_rooms",
    "meeting_rooms_ii",
]
