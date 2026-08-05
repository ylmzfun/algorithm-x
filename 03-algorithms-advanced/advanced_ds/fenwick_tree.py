"""
Fenwick Tree (Binary Indexed Tree) implementations.

Contains:
- FenwickTree: Point update, prefix sum query.
- FenwickTreeRangeUpdate: Range update, point query.
- FenwickTreeRangeUpdateRangeQuery: Range update, range query (two BITs).
"""

from typing import List


# ======================================================================
# Standard Fenwick Tree: point update + prefix sum query
# ======================================================================

class FenwickTree:
    """
    Fenwick Tree (Binary Indexed Tree) for point updates and prefix sum queries.

    All indices are 1-based internally.  Public methods accept 0-based indices
    and convert automatically.
    """

    def __init__(self, n: int) -> None:
        """
        Initialize a Fenwick Tree for n elements (0-based indices 0 … n-1).

        Args:
            n: Number of elements.

        Time: O(n)
        """
        self.n = n
        self.tree = [0] * (n + 1)  # 1-based indexing

    def add(self, idx: int, delta: int) -> None:
        """
        Add delta to the value at position idx (0-based).

        Args:
            idx: 0-based index.
            delta: Value to add (can be negative).

        Time: O(log n)
        """
        i = idx + 1
        while i <= self.n:
            self.tree[i] += delta
            i += i & -i

    def prefix_sum(self, idx: int) -> int:
        """
        Compute the sum of elements from 0 to idx (inclusive).

        Args:
            idx: 0-based index.

        Returns:
            Sum of arr[0] + arr[1] + … + arr[idx].

        Time: O(log n)
        """
        i = idx + 1
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & -i
        return s

    def range_sum(self, left: int, right: int) -> int:
        """
        Compute the sum of elements in [left, right] (inclusive, 0-based).

        Args:
            left: Left index (0-based, inclusive).
            right: Right index (0-based, inclusive).

        Returns:
            Sum of arr[left] + … + arr[right].

        Time: O(log n)
        """
        if left == 0:
            return self.prefix_sum(right)
        return self.prefix_sum(right) - self.prefix_sum(left - 1)


# ======================================================================
# Range Update + Point Query
# ======================================================================

class FenwickTreeRangeUpdate:
    """
    Fenwick Tree variant for range updates and point queries.

    Uses difference array: add(l, r, delta) adds delta to all elements
    in [l, r]; point_query(idx) returns the current value at idx.
    """

    def __init__(self, n: int) -> None:
        """
        Initialize for n elements.

        Args:
            n: Number of elements.

        Time: O(n)
        """
        self.n = n
        self.bit = FenwickTree(n)

    def add(self, left: int, right: int, delta: int) -> None:
        """
        Add delta to all elements in the range [left, right] (0-based).

        Args:
            left: Start index (inclusive).
            right: End index (inclusive).
            delta: Value to add.

        Time: O(log n)
        """
        self.bit.add(left, delta)
        if right + 1 < self.n:
            self.bit.add(right + 1, -delta)

    def point_query(self, idx: int) -> int:
        """
        Get the value at position idx (0-based).

        Returns:
            Current value at idx.

        Time: O(log n)
        """
        return self.bit.prefix_sum(idx)


# ======================================================================
# Range Update + Range Query (two BITs)
# ======================================================================

class FenwickTreeRangeUpdateRangeQuery:
    """
    Fenwick Tree supporting range updates and range sum queries.

    Uses two BITs (B1 for delta*t, B2 for delta) to support:
      - add(l, r, delta): O(log n)
      - range_sum(l, r): O(log n)
    """

    def __init__(self, n: int) -> None:
        """
        Initialize for n elements.

        Args:
            n: Number of elements.

        Time: O(n)
        """
        self.n = n
        self.bit1 = FenwickTree(n)  # stores delta * idx
        self.bit2 = FenwickTree(n)  # stores delta

    def add(self, left: int, right: int, delta: int) -> None:
        """
        Add delta to all elements in [left, right] (0-based).

        Args:
            left: Start index (inclusive).
            right: End index (inclusive).
            delta: Value to add.

        Time: O(log n)
        """
        self._add_to_bit(self.bit1, left, delta * left)
        self._add_to_bit(self.bit1, right + 1, -delta * (right + 1))
        self._add_to_bit(self.bit2, left, delta)
        self._add_to_bit(self.bit2, right + 1, -delta)

    def _add_to_bit(self, bit: FenwickTree, idx: int, delta: int) -> None:
        """Helper: add delta at idx (if in bounds)."""
        if 0 <= idx < self.n:
            bit.add(idx, delta)

    def prefix_sum(self, idx: int) -> int:
        """
        Compute prefix sum from 0 to idx (0-based, inclusive).

        Returns:
            Sum of arr[0] + … + arr[idx].

        Time: O(log n)
        """
        if idx < 0:
            return 0
        return (idx + 1) * self.bit2.prefix_sum(idx) - self.bit1.prefix_sum(idx)

    def range_sum(self, left: int, right: int) -> int:
        """
        Compute sum of elements in [left, right] (0-based, inclusive).

        Args:
            left: Start index.
            right: End index.

        Returns:
            Range sum.

        Time: O(log n)
        """
        return self.prefix_sum(right) - self.prefix_sum(left - 1)


# ======================================================================
# Tests
# ======================================================================

if __name__ == "__main__":
    import sys

    all_pass = True

    # --- Standard Fenwick ---
    ft = FenwickTree(6)
    arr = [1, 3, 5, 7, 9, 11]
    for i, v in enumerate(arr):
        ft.add(i, v)

    # prefix sums
    for i in range(6):
        expected = sum(arr[: i + 1])
        if ft.prefix_sum(i) != expected:
            print(f"FAIL prefix_sum({i}): expected {expected}, got {ft.prefix_sum(i)}")
            all_pass = False

    # range sum
    if ft.range_sum(1, 3) != 15:
        print(f"FAIL range_sum(1,3): {ft.range_sum(1, 3)}")
        all_pass = False

    # Point update
    ft.add(2, 10)  # arr[2] = 15
    if ft.range_sum(2, 2) != 15:
        print(f"FAIL after update: {ft.range_sum(2, 2)}")
        all_pass = False

    # --- Range Update / Point Query ---
    ft_ru = FenwickTreeRangeUpdate(5)
    ft_ru.add(1, 3, 5)  # add 5 to indices 1,2,3
    if ft_ru.point_query(0) != 0:
        print(f"FAIL RU point 0: {ft_ru.point_query(0)}")
        all_pass = False
    if ft_ru.point_query(1) != 5:
        print(f"FAIL RU point 1: {ft_ru.point_query(1)}")
        all_pass = False
    if ft_ru.point_query(3) != 5:
        print(f"FAIL RU point 3: {ft_ru.point_query(3)}")
        all_pass = False
    if ft_ru.point_query(4) != 0:
        print(f"FAIL RU point 4: {ft_ru.point_query(4)}")
        all_pass = False

    # --- Range Update / Range Query ---
    ft_rr = FenwickTreeRangeUpdateRangeQuery(5)
    ft_rr.add(1, 3, 2)   # indices 1,2,3 += 2
    ft_rr.add(2, 4, 3)   # indices 2,3,4 += 3 → [0, 2, 5, 5, 3]
    if ft_rr.prefix_sum(0) != 0:
        print(f"FAIL RR prefix 0: {ft_rr.prefix_sum(0)}")
        all_pass = False
    if ft_rr.prefix_sum(1) != 2:
        print(f"FAIL RR prefix 1: {ft_rr.prefix_sum(1)}")
        all_pass = False
    if ft_rr.prefix_sum(4) != 15:  # 0+2+5+5+3
        print(f"FAIL RR prefix 4: {ft_rr.prefix_sum(4)}")
        all_pass = False
    if ft_rr.range_sum(1, 3) != 12:  # 2+5+5
        print(f"FAIL RR range 1-3: {ft_rr.range_sum(1, 3)}")
        all_pass = False

    if all_pass:
        print("All Fenwick Tree tests PASSED")
    sys.exit(0 if all_pass else 1)
