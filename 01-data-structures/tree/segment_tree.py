"""
Segment Tree Implementation
============================

A segment tree that supports range queries (sum, min, max) and point updates
in O(log n) time. Also supports range updates with lazy propagation.

The tree is stored as an array of size 4*n (worst case for a complete
segment tree of n leaves).

Operations:
    - build: O(n) — construct tree from array
    - range_query (sum/min/max): O(log n)
    - point_update: O(log n) — update single element
    - range_update (lazy): O(log n) — add value to all elements in range

Space Complexity: O(n)
"""

from typing import Any, Callable, List, Optional, Union


class SegmentTree:
    """A segment tree that supports range queries and point updates.

    Supports three aggregation modes: sum, min, max.

    Implementation uses 0-based indexing for the underlying array and
    1-based indexing for the segment tree nodes.

    Examples:
        >>> st = SegmentTree([1, 3, 5, 7, 9, 11])
        >>> st.range_query(1, 3)  # arr[1..3] = 3+5+7
        15
        >>> st.point_update(1, 10)  # arr[1] = 10
        >>> st.range_query(1, 3)
        22
    """

    def __init__(self, data: List[int], mode: str = "sum") -> None:
        """Initialize segment tree from a list of integers.

        Args:
            data: List of integers to build the tree from.
            mode: Aggregation mode — "sum" (default), "min", or "max".

        Raises:
            ValueError: If mode is not one of "sum", "min", "max".
        """
        if mode not in ("sum", "min", "max"):
            raise ValueError(f"Unsupported mode '{mode}'. Use 'sum', 'min', or 'max'.")

        self._n = len(data)
        self._mode = mode
        self._data = data[:]  # Keep a copy for point_update reference
        self._tree: List[int] = [0] * (4 * self._n)

        # Lazy propagation support (for range updates)
        self._lazy: List[int] = [0] * (4 * self._n)

        # Select merge and neutral functions
        if mode == "sum":
            self._merge: Callable[[int, int], int] = lambda a, b: a + b
            self._neutral = 0
        elif mode == "min":
            self._merge = min
            self._neutral = float('inf')  # type: ignore[assignment]
        else:  # max
            self._merge = max
            self._neutral = float('-inf')  # type: ignore[assignment]

        if self._n > 0:
            self._build(1, 0, self._n - 1)

    # ── Build ─────────────────────────────────────────────────────────────────

    def _build(self, node: int, start: int, end: int) -> None:
        """Recursively build the segment tree.

        Args:
            node: Current tree node index (1-based).
            start: Start index of the segment in the original array.
            end: End index of the segment.

        Time Complexity: O(n)
        """
        if start == end:
            self._tree[node] = self._data[start]
        else:
            mid = (start + end) // 2
            self._build(2 * node, start, mid)
            self._build(2 * node + 1, mid + 1, end)
            self._tree[node] = self._merge(
                self._tree[2 * node],
                self._tree[2 * node + 1]
            )

    # ── Point Update ──────────────────────────────────────────────────────────

    def point_update(self, idx: int, value: int) -> None:
        """Update the element at index `idx` to `value`.

        Args:
            idx: 0-based index in the original array.
            value: New value.

        Raises:
            IndexError: If idx is out of bounds.

        Time Complexity: O(log n)
        """
        if not 0 <= idx < self._n:
            raise IndexError(f"Index {idx} out of bounds for size {self._n}")

        self._data[idx] = value
        self._point_update(1, 0, self._n - 1, idx, value)

    def _point_update(self, node: int, start: int, end: int,
                      idx: int, value: int) -> None:
        """Recursive point update."""
        if start == end:
            self._tree[node] = value
        else:
            mid = (start + end) // 2
            if idx <= mid:
                self._point_update(2 * node, start, mid, idx, value)
            else:
                self._point_update(2 * node + 1, mid + 1, end, idx, value)
            self._tree[node] = self._merge(
                self._tree[2 * node],
                self._tree[2 * node + 1]
            )

    # ── Range Query ───────────────────────────────────────────────────────────

    def range_query(self, left: int, right: int) -> int:
        """Query the aggregate over [left, right] inclusive.

        Args:
            left: Left bound (0-based, inclusive).
            right: Right bound (0-based, inclusive).

        Returns:
            Aggregated value (sum, min, or max).

        Raises:
            IndexError: If bounds are out of range.

        Time Complexity: O(log n)
        """
        if not 0 <= left <= right < self._n:
            raise IndexError(f"Invalid range [{left}, {right}] for size {self._n}")

        return self._range_query(1, 0, self._n - 1, left, right)

    def _range_query(self, node: int, start: int, end: int,
                     left: int, right: int) -> int:
        """Recursive range query."""
        # Completely outside
        if start > right or end < left:
            return self._neutral  # type: ignore[return-value]

        # Completely inside
        if left <= start and end <= right:
            return self._tree[node]

        # Partial overlap
        mid = (start + end) // 2
        left_res = self._range_query(2 * node, start, mid, left, right)
        right_res = self._range_query(2 * node + 1, mid + 1, end, left, right)
        return self._merge(left_res, right_res)

    # ── Range Update (Lazy Propagation) ──────────────────────────────────────

    def range_update(self, left: int, right: int, delta: int) -> None:
        """Add `delta` to all elements in range [left, right] (inclusive).

        Uses lazy propagation for O(log n) updates. Note: only makes sense
        with "sum" mode. For "min"/"max", semantics may be unexpected.

        Args:
            left: Left bound (0-based, inclusive).
            right: Right bound (0-based, inclusive).
            delta: Value to add to each element in the range.

        Raises:
            IndexError: If bounds are out of range.

        Time Complexity: O(log n)
        """
        if not 0 <= left <= right < self._n:
            raise IndexError(f"Invalid range [{left}, {right}] for size {self._n}")

        self._range_update(1, 0, self._n - 1, left, right, delta)

    def _range_update(self, node: int, start: int, end: int,
                      left: int, right: int, delta: int) -> None:
        """Recursive range update with lazy propagation."""
        # If there's pending lazy update, propagate it first
        if self._lazy[node] != 0:
            self._tree[node] += (end - start + 1) * self._lazy[node]

            if start != end:  # Not a leaf — push lazy to children
                self._lazy[2 * node] += self._lazy[node]
                self._lazy[2 * node + 1] += self._lazy[node]

            self._lazy[node] = 0

        # Completely outside
        if start > right or end < left:
            return

        # Completely inside — apply update lazily
        if left <= start and end <= right:
            self._tree[node] += (end - start + 1) * delta

            if start != end:  # Mark children as lazy
                self._lazy[2 * node] += delta
                self._lazy[2 * node + 1] += delta
            return

        # Partial overlap
        mid = (start + end) // 2
        self._range_update(2 * node, start, mid, left, right, delta)
        self._range_update(2 * node + 1, mid + 1, end, left, right, delta)
        self._tree[node] = self._merge(
            self._tree[2 * node],
            self._tree[2 * node + 1]
        )

    def range_query_lazy(self, left: int, right: int) -> int:
        """Range query that accounts for lazy pending updates.

        Args:
            left: Left bound (0-based).
            right: Right bound (0-based).

        Returns:
            Aggregated value.

        Time Complexity: O(log n)
        """
        if not 0 <= left <= right < self._n:
            raise IndexError(f"Invalid range [{left}, {right}] for size {self._n}")
        return self._range_query_lazy(1, 0, self._n - 1, left, right)

    def _range_query_lazy(self, node: int, start: int, end: int,
                          left: int, right: int) -> int:
        """Recursive range query with lazy propagation."""
        # Push pending lazy
        if self._lazy[node] != 0:
            self._tree[node] += (end - start + 1) * self._lazy[node]
            if start != end:
                self._lazy[2 * node] += self._lazy[node]
                self._lazy[2 * node + 1] += self._lazy[node]
            self._lazy[node] = 0

        if start > right or end < left:
            return self._neutral  # type: ignore[return-value]

        if left <= start and end <= right:
            return self._tree[node]

        mid = (start + end) // 2
        left_res = self._range_query_lazy(2 * node, start, mid, left, right)
        right_res = self._range_query_lazy(2 * node + 1, mid + 1, end, left, right)
        return self._merge(left_res, right_res)

    def __len__(self) -> int:
        """Return number of elements."""
        return self._n

    def __repr__(self) -> str:
        """Return detailed representation."""
        return f"SegmentTree(mode={self._mode!r}, n={self._n})"


# ─── Tests ────────────────────────────────────────────────────────────────────


def _run_tests() -> None:
    """Run all tests and report results."""
    import sys

    passed = 0
    failed = 0

    def check(description: str, condition: bool) -> None:
        nonlocal passed, failed
        if condition:
            passed += 1
            print(f"  ✓ {description}")
        else:
            failed += 1
            print(f"  ✗ {description}", file=sys.stderr)

    # ── Sum Segment Tree ──────────────────────────────────────────────────────
    print("Sum Segment Tree:")
    data = [1, 3, 5, 7, 9, 11]
    st = SegmentTree(data, mode="sum")

    check("range [0,5]", st.range_query(0, 5) == 36)
    check("range [1,3]", st.range_query(1, 3) == 15)
    check("range [0,0]", st.range_query(0, 0) == 1)
    check("range [5,5]", st.range_query(5, 5) == 11)

    # Point update
    st.point_update(1, 10)  # data[1] = 10
    check("after update: [1,3]", st.range_query(1, 3) == 22)  # 10+5+7
    check("after update: [0,5]", st.range_query(0, 5) == 43)

    # Negative test
    try:
        st.point_update(100, 0)
        check("point_update oob", False)
    except IndexError:
        check("point_update oob", True)

    try:
        st.range_query(0, 100)
        check("range_query oob", False)
    except IndexError:
        check("range_query oob", True)

    # ── Min Segment Tree ──────────────────────────────────────────────────────
    print("\nMin Segment Tree:")
    st_min = SegmentTree([5, 2, 8, 1, 9, 3], mode="min")
    check("min [0,5] == 1", st_min.range_query(0, 5) == 1)
    check("min [0,2] == 2", st_min.range_query(0, 2) == 2)
    check("min [3,5] == 1", st_min.range_query(3, 5) == 1)

    st_min.point_update(3, 10)  # [5,2,8,10,9,3]
    check("min after update == 2", st_min.range_query(0, 5) == 2)

    # ── Max Segment Tree ──────────────────────────────────────────────────────
    print("\nMax Segment Tree:")
    st_max = SegmentTree([5, 2, 8, 1, 9, 3], mode="max")
    check("max [0,5] == 9", st_max.range_query(0, 5) == 9)
    check("max [0,2] == 8", st_max.range_query(0, 2) == 8)
    check("max [4,5] == 9", st_max.range_query(4, 5) == 9)

    st_max.point_update(4, 0)
    check("max after update == 8", st_max.range_query(0, 5) == 8)

    # ── Range Update (Lazy) ───────────────────────────────────────────────────
    print("\nRange Update (Lazy):")
    st_lazy = SegmentTree([1, 2, 3, 4, 5], mode="sum")

    st_lazy.range_update(1, 3, 10)  # Add 10 to [1,2,3,4] → [1,12,13,14,5]
    check("lazy [0,4] = 45", st_lazy.range_query_lazy(0, 4) == 45)
    check("lazy [1,3] = 39", st_lazy.range_query_lazy(1, 3) == 39)
    check("lazy [0,0] = 1", st_lazy.range_query_lazy(0, 0) == 1)
    check("lazy [4,4] = 5", st_lazy.range_query_lazy(4, 4) == 5)

    # Multiple range updates
    st_lazy.range_update(2, 4, 5)  # Add 5 to [3,4,5] → [1,12,18,19,10]
    check("multi lazy [0,4] = 60", st_lazy.range_query_lazy(0, 4) == 60)
    check("multi lazy [2,4] = 47", st_lazy.range_query_lazy(2, 4) == 47)

    # ── Invalid mode ──────────────────────────────────────────────────────────
    print("\nInvalid mode:")
    try:
        SegmentTree([1, 2], mode="avg")
        check("invalid mode raises", False)
    except ValueError:
        check("invalid mode raises", True)

    # ── Empty tree ────────────────────────────────────────────────────────────
    print("\nEmpty tree:")
    st_empty = SegmentTree([], mode="sum")
    check("empty len == 0", len(st_empty) == 0)

    # ── Summary ───────────────────────────────────────────────────────────────
    total = passed + failed
    print(f"\n{'='*50}")
    print(f"Results: {passed}/{total} passed, {failed}/{total} failed")
    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    _run_tests()
