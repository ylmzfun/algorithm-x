"""
Interval-Based Greedy Problems
===============================

Many greedy problems involve scheduling or merging intervals.  The common
pattern is sorting by start or end time, then making a greedy choice.

Functions:
- merge_intervals             : Merge all overlapping intervals.
- insert_interval             : Insert a new interval into a sorted non-
                                overlapping list.
- erase_overlapping_intervals : Min number of intervals to remove to make
                                the rest non-overlapping.
- min_arrows_burst_balloons   : Min arrows to burst all balloons (intervals).
- meeting_rooms               : Whether a person can attend all meetings.
- meeting_rooms_ii            : Min number of meeting rooms required.
"""

import heapq
from typing import List, Tuple


# ---------------------------------------------------------------------------
# Merge Intervals
# ---------------------------------------------------------------------------

def merge_intervals(intervals: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    Merge all overlapping intervals.

    Parameters
    ----------
    intervals : List[Tuple[int, int]]
        Possibly overlapping intervals.

    Returns
    -------
    List[Tuple[int, int]]
        Merged, non-overlapping intervals sorted by start.

    Time  : O(n log n)
    Space : O(n)

    Example
    -------
    >>> merge_intervals([(1, 3), (2, 6), (8, 10), (15, 18)])
    [(1, 6), (8, 10), (15, 18)]
    """
    if not intervals:
        return []
    sorted_int = sorted(intervals, key=lambda x: x[0])
    merged = [sorted_int[0]]
    for start, end in sorted_int[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))
    return merged


# ---------------------------------------------------------------------------
# Insert Interval
# ---------------------------------------------------------------------------

def insert_interval(
    intervals: List[Tuple[int, int]], new_interval: Tuple[int, int]
) -> List[Tuple[int, int]]:
    """
    Insert a new interval into a list of **non-overlapping**, sorted-by-start
    intervals, merging if necessary.

    Parameters
    ----------
    intervals : List[Tuple[int, int]]
        Non-overlapping intervals sorted by start.
    new_interval : Tuple[int, int]
        Interval to insert.

    Returns
    -------
    List[Tuple[int, int]]
        Resulting list of non-overlapping intervals.

    Time  : O(n)
    Space : O(n)

    Example
    -------
    >>> insert_interval([(1, 3), (6, 9)], (2, 5))
    [(1, 5), (6, 9)]
    """
    result: List[Tuple[int, int]] = []
    i = 0
    n = len(intervals)
    new_start, new_end = new_interval

    # Add all intervals that end before the new interval starts
    while i < n and intervals[i][1] < new_start:
        result.append(intervals[i])
        i += 1

    # Merge overlapping intervals
    while i < n and intervals[i][0] <= new_end:
        new_start = min(new_start, intervals[i][0])
        new_end = max(new_end, intervals[i][1])
        i += 1
    result.append((new_start, new_end))

    # Add remaining intervals
    while i < n:
        result.append(intervals[i])
        i += 1

    return result


# ---------------------------------------------------------------------------
# Erase Overlapping Intervals (Min Removals)
# ---------------------------------------------------------------------------

def erase_overlapping_intervals(intervals: List[Tuple[int, int]]) -> int:
    """
    Minimum number of intervals to remove so that the remaining intervals
    are non-overlapping.

    Greedy: sort by end time, keep the interval that ends earliest among
    overlapping candidates.

    Parameters
    ----------
    intervals : List[Tuple[int, int]]
        List of intervals.

    Returns
    -------
    int
        Minimum removals.

    Time  : O(n log n)
    Space : O(1)

    Example
    -------
    >>> erase_overlapping_intervals([(1, 2), (2, 3), (3, 4), (1, 3)])
    1   # remove (1, 3)
    """
    if not intervals:
        return 0
    intervals.sort(key=lambda x: x[1])
    count = 0
    last_end = intervals[0][1]
    for start, end in intervals[1:]:
        if start < last_end:
            count += 1
        else:
            last_end = end
    return count


# ---------------------------------------------------------------------------
# Minimum Arrows to Burst Balloons
# ---------------------------------------------------------------------------

def min_arrows_burst_balloons(points: List[Tuple[int, int]]) -> int:
    """
    Find the minimum number of arrows that must be shot vertically to burst
    all balloons.  Each balloon is represented by an interval [x_start,
    x_end].

    Greedy: sort by end coordinate, shoot at balloon ends whenever a new
    balloon starts after the current arrow position.

    Parameters
    ----------
    points : List[Tuple[int, int]]
        Balloon intervals.

    Returns
    -------
    int
        Minimum arrows needed.

    Time  : O(n log n)
    Space : O(1)

    Example
    -------
    >>> min_arrows_burst_balloons([(10, 16), (2, 8), (1, 6), (7, 12)])
    2
    """
    if not points:
        return 0
    points.sort(key=lambda x: x[1])
    arrows = 1
    arrow_pos = points[0][1]
    for start, end in points[1:]:
        if start > arrow_pos:
            arrows += 1
            arrow_pos = end
    return arrows


# ---------------------------------------------------------------------------
# Meeting Rooms I — Can Attend All?
# ---------------------------------------------------------------------------

def meeting_rooms(intervals: List[Tuple[int, int]]) -> bool:
    """
    Determine if a person can attend all meetings (no overlaps).

    Parameters
    ----------
    intervals : List[Tuple[int, int]]
        Meeting intervals (start, end).

    Returns
    -------
    bool
        True if no meetings overlap.

    Time  : O(n log n)
    Space : O(1)

    Example
    -------
    >>> meeting_rooms([(0, 30), (5, 10), (15, 20)])
    False
    >>> meeting_rooms([(7, 10), (2, 4)])
    True
    """
    intervals.sort(key=lambda x: x[0])
    for i in range(1, len(intervals)):
        if intervals[i][0] < intervals[i - 1][1]:
            return False
    return True


# ---------------------------------------------------------------------------
# Meeting Rooms II — Min Rooms Needed
# ---------------------------------------------------------------------------

def meeting_rooms_ii(intervals: List[Tuple[int, int]]) -> int:
    """
    Minimum number of meeting rooms required (maximum simultaneous meetings).

    Uses a min-heap of end times to track currently occupied rooms.

    Parameters
    ----------
    intervals : List[Tuple[int, int]]
        Meeting intervals.

    Returns
    -------
    int
        Minimum rooms needed.

    Time  : O(n log n)
    Space : O(n)

    Example
    -------
    >>> meeting_rooms_ii([(0, 30), (5, 10), (15, 20)])
    2
    """
    if not intervals:
        return 0
    intervals.sort(key=lambda x: x[0])
    heap: List[int] = []  # min-heap of end times
    max_rooms = 0

    for start, end in intervals:
        # Free rooms whose meeting has ended before this meeting starts
        while heap and heap[0] <= start:
            heapq.heappop(heap)
        heapq.heappush(heap, end)
        max_rooms = max(max_rooms, len(heap))

    return max_rooms


# ===========================================================================
# Tests
# ===========================================================================

if __name__ == "__main__":
    print("=== Interval Problems Tests ===\n")

    # merge_intervals
    assert merge_intervals([(1, 3), (2, 6), (8, 10)]) == [(1, 6), (8, 10)]
    assert merge_intervals([]) == []
    print("  PASS merge_intervals")

    # insert_interval
    assert insert_interval([(1, 3), (6, 9)], (2, 5)) == [(1, 5), (6, 9)]
    assert insert_interval([], (5, 7)) == [(5, 7)]
    assert insert_interval([(1, 5)], (2, 3)) == [(1, 5)]
    print("  PASS insert_interval")

    # erase_overlapping_intervals
    assert erase_overlapping_intervals([(1, 2), (2, 3), (3, 4), (1, 3)]) == 1
    assert erase_overlapping_intervals([(1, 2), (1, 2), (1, 2)]) == 2
    assert erase_overlapping_intervals([]) == 0
    print("  PASS erase_overlapping_intervals")

    # min_arrows_burst_balloons
    assert min_arrows_burst_balloons([(10, 16), (2, 8), (1, 6), (7, 12)]) == 2
    assert min_arrows_burst_balloons([(1, 2), (3, 4), (5, 6)]) == 3
    assert min_arrows_burst_balloons([]) == 0
    print("  PASS min_arrows_burst_balloons")

    # meeting_rooms
    assert meeting_rooms([(0, 30), (5, 10), (15, 20)]) == False
    assert meeting_rooms([(7, 10), (2, 4)]) == True
    assert meeting_rooms([]) == True
    print("  PASS meeting_rooms")

    # meeting_rooms_ii
    assert meeting_rooms_ii([(0, 30), (5, 10), (15, 20)]) == 2
    assert meeting_rooms_ii([(7, 10), (2, 4)]) == 1
    assert meeting_rooms_ii([(0, 10), (10, 20)]) == 1
    assert meeting_rooms_ii([]) == 0
    print("  PASS meeting_rooms_ii")

    print("\nAll interval problems tests completed!")
