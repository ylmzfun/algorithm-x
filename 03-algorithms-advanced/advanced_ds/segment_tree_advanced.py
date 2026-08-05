"""
Segment Tree with lazy propagation.

Supports:
- Range updates (add a value to all elements in a range)
- Range queries (sum, minimum, maximum)
- Lazy propagation for O(log n) range operations
"""

from typing import Callable, List, Optional


class LazySegmentTree:
    """
    Segment Tree with lazy propagation.

    Supports range updates and range queries for associative operations
    (sum, min, max) in O(log n) time.

    The tree is 0-indexed externally and 1-indexed internally.
    """

    def __init__(
        self,
        arr: List[int],
        op: str = "sum",
    ) -> None:
        """
        Initialize the segment tree with the given array.

        Args:
            arr: Initial array values.
            op: One of "sum", "min", "max" — the query operation.

        Time: O(n)
        """
        self.n = len(arr)
        self.op_name = op
        size = 4 * self.n
        self.tree = [0] * size
        self.lazy = [0] * size

        # Define operation identities
        if op == "sum":
            self._neutral = 0
        elif op == "min":
            self._neutral = float("inf")
            self.tree = [self._neutral] * size
            self.lazy = [0] * size
        elif op == "max":
            self._neutral = float("-inf")
            self.tree = [self._neutral] * size
            self.lazy = [0] * size
        else:
            raise ValueError(f"Unknown operation: {op}")

        self._build(arr, 1, 0, self.n - 1)

    # ------------------------------------------------------------------
    # Build
    # ------------------------------------------------------------------

    def _build(self, arr: List[int], node: int, left: int, right: int) -> None:
        """Recursively build the segment tree."""
        if left == right:
            self.tree[node] = arr[left]
            return

        mid = (left + right) // 2
        self._build(arr, node * 2, left, mid)
        self._build(arr, node * 2 + 1, mid + 1, right)
        self.tree[node] = self._combine(
            self.tree[node * 2], self.tree[node * 2 + 1]
        )

    # ------------------------------------------------------------------
    # Combine
    # ------------------------------------------------------------------

    def _combine(self, a: int, b: int) -> int:
        """Combine two child values according to the operation."""
        if self.op_name == "sum":
            return a + b
        elif self.op_name == "min":
            return min(a, b)
        elif self.op_name == "max":
            return max(a, b)
        return 0

    def _apply(self, node: int, left: int, right: int, value: int) -> None:
        """Apply the lazy value to a node spanning [left, right]."""
        if self.op_name == "sum":
            self.tree[node] += value * (right - left + 1)
            self.lazy[node] += value
        elif self.op_name == "min":
            self.tree[node] += value
            self.lazy[node] += value
        elif self.op_name == "max":
            self.tree[node] += value
            self.lazy[node] += value

    def _push(self, node: int, left: int, right: int) -> None:
        """Push lazy value down to children."""
        if self.lazy[node] != 0:
            mid = (left + right) // 2
            self._apply(node * 2, left, mid, self.lazy[node])
            self._apply(node * 2 + 1, mid + 1, right, self.lazy[node])
            self.lazy[node] = 0

    # ------------------------------------------------------------------
    # Range Update
    # ------------------------------------------------------------------

    def update(self, ql: int, qr: int, value: int) -> None:
        """
        Add `value` to all elements in range [ql, qr] (0-based, inclusive).

        Args:
            ql: Query left bound.
            qr: Query right bound.
            value: Value to add.

        Time: O(log n)
        """
        self._update(1, 0, self.n - 1, ql, qr, value)

    def _update(
        self,
        node: int,
        left: int,
        right: int,
        ql: int,
        qr: int,
        value: int,
    ) -> None:
        if ql > right or qr < left:
            return
        if ql <= left and right <= qr:
            self._apply(node, left, right, value)
            return

        self._push(node, left, right)
        mid = (left + right) // 2
        self._update(node * 2, left, mid, ql, qr, value)
        self._update(node * 2 + 1, mid + 1, right, ql, qr, value)
        self.tree[node] = self._combine(
            self.tree[node * 2], self.tree[node * 2 + 1]
        )

    # ------------------------------------------------------------------
    # Range Query
    # ------------------------------------------------------------------

    def query(self, ql: int, qr: int) -> int:
        """
        Query the aggregate value over range [ql, qr] (0-based, inclusive).

        Args:
            ql: Query left bound.
            qr: Query right bound.

        Returns:
            The aggregate value (sum, min, or max).

        Time: O(log n)
        """
        return self._query(1, 0, self.n - 1, ql, qr)

    def _query(
        self, node: int, left: int, right: int, ql: int, qr: int
    ) -> int:
        if ql > right or qr < left:
            return self._neutral
        if ql <= left and right <= qr:
            return self.tree[node]

        self._push(node, left, right)
        mid = (left + right) // 2
        left_val = self._query(node * 2, left, mid, ql, qr)
        right_val = self._query(node * 2 + 1, mid + 1, right, ql, qr)
        return self._combine(left_val, right_val)

    # ------------------------------------------------------------------
    # Point Update
    # ------------------------------------------------------------------

    def point_update(self, idx: int, value: int) -> None:
        """
        Set the element at position idx to value.

        Args:
            idx: 0-based index.
            value: New value.

        Time: O(log n)
        """
        self._point_update(1, 0, self.n - 1, idx, value)

    def _point_update(
        self, node: int, left: int, right: int, idx: int, value: int
    ) -> None:
        if left == right:
            self.tree[node] = value
            return
        self._push(node, left, right)
        mid = (left + right) // 2
        if idx <= mid:
            self._point_update(node * 2, left, mid, idx, value)
        else:
            self._point_update(node * 2 + 1, mid + 1, right, idx, value)
        self.tree[node] = self._combine(
            self.tree[node * 2], self.tree[node * 2 + 1]
        )


# ======================================================================
# Tests
# ======================================================================

if __name__ == "__main__":
    import sys

    all_pass = True

    # --- Sum segment tree ---
    arr = [1, 3, 5, 7, 9, 11]
    st = LazySegmentTree(arr, op="sum")

    # Range sum
    if st.query(0, 5) != 36:
        print(f"FAIL sum all: {st.query(0, 5)}")
        all_pass = False
    if st.query(1, 3) != 15:
        print(f"FAIL sum 1-3: {st.query(1, 3)}")
        all_pass = False

    # Range update
    st.update(1, 3, 2)  # arr → [1,5,7,9,9,11]
    if st.query(1, 3) != 21:  # 5+7+9
        print(f"FAIL after update sum 1-3: {st.query(1, 3)}")
        all_pass = False
    if st.query(0, 5) != 42:  # 1+5+7+9+9+11
        print(f"FAIL after update sum all: {st.query(0, 5)}")
        all_pass = False

    # Point query via range query
    if st.query(2, 2) != 7:
        print(f"FAIL point query: {st.query(2, 2)}")
        all_pass = False

    # --- Min segment tree ---
    st_min = LazySegmentTree(arr, op="min")
    if st_min.query(0, 5) != 1:
        print(f"FAIL min all: {st_min.query(0, 5)}")
        all_pass = False
    st_min.update(0, 2, 10)  # arr → [11,13,15,7,9,11]
    if st_min.query(0, 2) != 11:
        print(f"FAIL min after update: {st_min.query(0, 2)}")
        all_pass = False
    if st_min.query(3, 5) != 7:
        print(f"FAIL min unchanged: {st_min.query(3, 5)}")
        all_pass = False

    # --- Max segment tree ---
    st_max = LazySegmentTree(arr, op="max")
    if st_max.query(0, 5) != 11:
        print(f"FAIL max all: {st_max.query(0, 5)}")
        all_pass = False
    st_max.update(3, 5, -5)
    if st_max.query(3, 5) != 6:  # 7-5=2, 9-5=4, 11-5=6
        print(f"FAIL max after update: {st_max.query(3, 5)}")
        all_pass = False

    # --- Point update (set) ---
    st2 = LazySegmentTree([10, 20, 30], op="sum")
    st2.point_update(1, 99)
    if st2.query(0, 2) != 139:
        print(f"FAIL point_update: {st2.query(0, 2)}")
        all_pass = False

    if all_pass:
        print("All Segment Tree (lazy) tests PASSED")
    sys.exit(0 if all_pass else 1)
