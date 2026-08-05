"""
Monotonic Stack and Monotonic Queue
=====================================

Specialized stack/queue variants that maintain elements in monotonic
(increasing or decreasing) order. These structures enable efficient
solutions for problems involving "next greater/smaller element" and
"sliding window" patterns.

Problems solved:
    1. Next Greater Element (monotonic decreasing stack)
    2. Largest Rectangle in Histogram (monotonic increasing stack)
    3. Sliding Window Maximum (monotonic decreasing deque)
"""

from typing import Any, List, Tuple
from collections import deque


# ─── 1. Next Greater Element ──────────────────────────────────────────────────


def next_greater_element(nums: List[int]) -> List[int]:
    """For each element, find the next element to the right that is greater.

    Uses a monotonic decreasing stack. When a larger element is encountered,
    it is the answer for all smaller elements on the stack.

    Args:
        nums: List of integers.

    Returns:
        List where result[i] = next greater element to the right of nums[i],
        or -1 if none exists.

    Time Complexity: O(n) — each element pushed/popped at most once.
    Space Complexity: O(n) — for stack and result.

    Examples:
        >>> next_greater_element([4, 5, 2, 10, 8])
        [5, 10, 10, -1, -1]
        >>> next_greater_element([1, 2, 3, 4])
        [2, 3, 4, -1]
        >>> next_greater_element([4, 3, 2, 1])
        [-1, -1, -1, -1]
    """
    n = len(nums)
    result = [-1] * n
    stack: List[int] = []  # Stores indices with decreasing values

    for i in range(n):
        # While current element > stack top's element, we found NGE
        while stack and nums[i] > nums[stack[-1]]:
            idx = stack.pop()
            result[idx] = nums[i]
        stack.append(i)

    return result


def next_greater_element_circular(nums: List[int]) -> List[int]:
    """Next greater element in a circular array (can wrap around).

    Traverses the array twice to handle circularity.

    Args:
        nums: List of integers.

    Returns:
        List where result[i] = next greater element (can wrap around),
        or -1 if none exists.

    Time Complexity: O(n)
    Space Complexity: O(n)

    Examples:
        >>> next_greater_element_circular([1, 2, 1])
        [2, -1, 2]
    """
    n = len(nums)
    result = [-1] * n
    stack: List[int] = []

    for i in range(2 * n):
        idx = i % n
        while stack and nums[idx] > nums[stack[-1]]:
            prev_idx = stack.pop()
            result[prev_idx] = nums[idx]
        if i < n:
            stack.append(idx)

    return result


# ─── 2. Largest Rectangle in Histogram ───────────────────────────────────────


def largest_rectangle_area(heights: List[int]) -> int:
    """Find the area of the largest rectangle in a histogram.

    Uses a monotonic increasing stack. For each bar, we find the maximum
    rectangle that uses that bar's height as the limiting height.

    Args:
        heights: List of bar heights.

    Returns:
        Maximum rectangular area.

    Time Complexity: O(n)
    Space Complexity: O(n)

    Examples:
        >>> largest_rectangle_area([2, 1, 5, 6, 2, 3])
        10
        >>> largest_rectangle_area([2, 4])
        4
    """
    # Append 0 to flush remaining bars at the end
    heights = heights + [0]
    stack: List[int] = []  # Stores indices with increasing heights
    max_area = 0

    for i, h in enumerate(heights):
        # While current bar is shorter than stack top, pop and calculate
        while stack and h < heights[stack[-1]]:
            height = heights[stack.pop()]
            # Width = distance from i back to the previous smaller bar
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)

    return max_area


# ─── 3. Sliding Window Maximum ───────────────────────────────────────────────


def sliding_window_maximum(nums: List[int], k: int) -> List[int]:
    """Find the maximum value in each sliding window of size k.

    Uses a monotonic decreasing deque. The front of the deque always
    holds the index of the maximum element in the current window.

    Args:
        nums: List of integers.
        k: Window size.

    Returns:
        List of maximums, one per window position.

    Raises:
        ValueError: If k <= 0 or k > len(nums).

    Time Complexity: O(n) — each element added/removed at most once.
    Space Complexity: O(k) — deque stores at most k indices.

    Examples:
        >>> sliding_window_maximum([1, 3, -1, -3, 5, 3, 6, 7], 3)
        [3, 3, 5, 5, 6, 7]
        >>> sliding_window_maximum([1, -1], 1)
        [1, -1]
    """
    n = len(nums)
    if k <= 0 or k > n:
        raise ValueError(f"k={k} must be in range [1, {n}]")

    dq = deque()  # type: deque[int]  # Stores indices, values decreasing
    result: List[int] = []

    for i in range(n):
        # Remove indices outside the current window
        if dq and dq[0] <= i - k:
            dq.popleft()

        # Maintain decreasing order: remove smaller elements from back
        while dq and nums[i] >= nums[dq[-1]]:
            dq.pop()

        dq.append(i)

        # Window is full (i >= k - 1), record max (front of deque)
        if i >= k - 1:
            result.append(nums[dq[0]])

    return result


# ─── 4. MonotonicStack class ──────────────────────────────────────────────────


class MonotonicStack:
    """A stack that maintains monotonic order (increasing or decreasing).

    Useful as a building block for problems like daily temperatures,
    stock span, etc.

    The stack stores (value, metadata) pairs where metadata can track
    additional info like count of popped elements.

    Examples:
        >>> ms = MonotonicStack(increasing=False)  # Decreasing stack
        >>> ms.push(5)
        >>> ms.push(3)
        >>> ms.push(4)  # Pops 3, then pushes 4
        >>> ms.peek()
        4
        >>> ms.size()
        2
    """

    def __init__(self, increasing: bool = True):
        """Initialize monotonic stack.

        Args:
            increasing: If True, stack is strictly increasing bottom→top.
                        If False, stack is strictly decreasing bottom→top.
        """
        self._increasing = increasing
        self._stack: List[Tuple[Any, int]] = []  # (value, count_popped)

    def push(self, value: Any) -> int:
        """Push value, popping elements that violate monotonic order.

        Args:
            value: Value to push.

        Returns:
            Number of elements popped to maintain monotonicity.

        Time Complexity: O(1) amortized
        """
        popped_count = 0
        # For increasing stack, pop while value <= top (pop larger or equal)
        # For decreasing stack, pop while value >= top (pop smaller or equal)
        if self._increasing:
            cmp = lambda a, b: a <= b
        else:
            cmp = lambda a, b: a >= b
        while self._stack and cmp(value, self._stack[-1][0]):
            popped_count += 1 + self._stack.pop()[1]
        self._stack.append((value, popped_count))
        return popped_count

    def pop(self) -> Tuple[Any, int]:
        """Pop the top element.

        Returns:
            Tuple of (value, count_popped_when_pushed).

        Raises:
            IndexError: If stack is empty.

        Time Complexity: O(1)
        """
        if not self._stack:
            raise IndexError("pop from empty MonotonicStack")
        return self._stack.pop()

    def peek(self) -> Any:
        """Return top value without removing.

        Returns:
            Top value.

        Raises:
            IndexError: If empty.

        Time Complexity: O(1)
        """
        if not self._stack:
            raise IndexError("peek from empty MonotonicStack")
        return self._stack[-1][0]

    def is_empty(self) -> bool:
        """Check if stack is empty."""
        return len(self._stack) == 0

    def size(self) -> int:
        """Return number of elements."""
        return len(self._stack)

    def __len__(self) -> int:
        """Support len()."""
        return len(self._stack)

    def __str__(self) -> str:
        """Return string representation."""
        return str([v for v, _ in self._stack])


# ─── 5. MonotonicQueue class ──────────────────────────────────────────────────


class MonotonicQueue:
    """A queue that maintains monotonic order (increasing or decreasing).

    Elements are added at the back (maintaining monotonic order) and
    the front holds the extremum (min for increasing, max for decreasing).

    Used for sliding window problems.

    Examples:
        >>> mq = MonotonicQueue(increasing=False)  # Decreasing: front = max
        >>> mq.push(1)
        >>> mq.push(3)
        >>> mq.push(2)
        >>> mq.max()
        3
        >>> mq.pop(1)
        >>> mq.max()
        3
    """

    def __init__(self, increasing: bool = True):
        """Initialize monotonic queue.

        Args:
            increasing: If True, queue is non-decreasing (front = min).
                        If False, queue is non-increasing (front = max).
        """
        self._increasing = increasing
        self._dq = deque()  # type: deque[int] — could store values or indices
        self._data = deque()  # type: deque[Any] — actual elements for pop tracking

    def push(self, value: Any) -> None:
        """Push value, maintaining monotonic order from back.

        Args:
            value: Value to add.

        Time Complexity: O(1) amortized
        """
        self._data.append(value)
        cmps = [
            lambda a, b: a < b,  # increasing: pop back while back > value
            lambda a, b: a > b,  # decreasing: pop back while back < value
        ]
        cmp = cmps[0] if self._increasing else cmps[1]
        while self._dq and cmp(value, self._dq[-1]):
            self._dq.pop()
        self._dq.append(value)

    def pop(self, value: Any) -> None:
        """Remove `value` from the front if it matches.

        Used to slide the window: pop the element leaving the window.

        Args:
            value: The element to potentially remove.

        Time Complexity: O(1)
        """
        if self._data:
            self._data.popleft()
        if self._dq and self._dq[0] == value:
            self._dq.popleft()

    def min(self) -> Any:
        """Return minimum element (valid for increasing queue).

        Returns:
            Minimum value.

        Raises:
            IndexError: If queue is empty.

        Time Complexity: O(1)
        """
        if not self._dq:
            raise IndexError("min from empty queue")
        return self._dq[0] if self._increasing else self._dq[-1]

    def max(self) -> Any:
        """Return maximum element (valid for decreasing queue).

        Returns:
            Maximum value.

        Raises:
            IndexError: If queue is empty.

        Time Complexity: O(1)
        """
        if not self._dq:
            raise IndexError("max from empty queue")
        return self._dq[0] if not self._increasing else self._dq[-1]

    def is_empty(self) -> bool:
        """Check if empty."""
        return len(self._dq) == 0

    def size(self) -> int:
        """Return number of elements."""
        return len(self._dq)

    def __len__(self) -> int:
        """Support len()."""
        return len(self._dq)


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

    # ── Next Greater Element ──────────────────────────────────────────────────
    print("Next Greater Element:")
    check("basic", next_greater_element([4, 5, 2, 10, 8]) == [5, 10, 10, -1, -1])
    check("increasing", next_greater_element([1, 2, 3, 4]) == [2, 3, 4, -1])
    check("decreasing", next_greater_element([4, 3, 2, 1]) == [-1, -1, -1, -1])
    check("single", next_greater_element([5]) == [-1])
    check("circular", next_greater_element_circular([1, 2, 1]) == [2, -1, 2])
    check("circular all same", next_greater_element_circular([2, 2, 2]) == [-1, -1, -1])

    # ── Largest Rectangle ─────────────────────────────────────────────────────
    print("\nLargest Rectangle in Histogram:")
    check("classic", largest_rectangle_area([2, 1, 5, 6, 2, 3]) == 10)
    check("two bars", largest_rectangle_area([2, 4]) == 4)
    check("single", largest_rectangle_area([5]) == 5)
    check("all same", largest_rectangle_area([2, 2, 2]) == 6)
    check("increasing", largest_rectangle_area([1, 2, 3, 4]) == 6)
    check("empty", largest_rectangle_area([]) == 0)

    # ── Sliding Window Maximum ────────────────────────────────────────────────
    print("\nSliding Window Maximum:")
    check("basic", sliding_window_maximum([1, 3, -1, -3, 5, 3, 6, 7], 3) ==
          [3, 3, 5, 5, 6, 7])
    check("k=1", sliding_window_maximum([1, -1], 1) == [1, -1])
    check("k=n", sliding_window_maximum([1, 3, 2], 3) == [3])
    check("all same", sliding_window_maximum([2, 2, 2, 2], 2) == [2, 2, 2])

    try:
        sliding_window_maximum([1, 2], 0)
        check("k=0 raises", False)
    except ValueError:
        check("k=0 raises", True)

    try:
        sliding_window_maximum([1, 2], 3)
        check("k>n raises", False)
    except ValueError:
        check("k>n raises", True)

    # ── MonotonicStack ────────────────────────────────────────────────────────
    print("\nMonotonicStack:")
    ms_inc = MonotonicStack(increasing=True)
    ms_inc.push(1)
    ms_inc.push(3)
    check("increasing push(3) ok (1<3)", ms_inc.size() == 2)
    popped = ms_inc.push(2)
    check("increasing push(2) pops 1 element", popped == 1)
    check("increasing size after push(2) -> [1,2]", ms_inc.size() == 2)

    ms_dec = MonotonicStack(increasing=False)
    ms_dec.push(5)
    ms_dec.push(3)
    check("decreasing push(3) ok (5>3)", ms_dec.size() == 2)
    popped = ms_dec.push(4)
    check("decreasing push(4) pops 1 element", popped == 1)
    check("decreasing stack now [5,4]", ms_dec.peek() == 4)

    try:
        MonotonicStack().pop()
        check("pop empty raises", False)
    except IndexError:
        check("pop empty raises", True)

    # ── MonotonicQueue ────────────────────────────────────────────────────────
    print("\nMonotonicQueue:")
    mq_dec = MonotonicQueue(increasing=False)  # Decreasing: front=MAX
    mq_dec.push(1)
    mq_dec.push(3)
    mq_dec.push(2)
    check("decreasing queue max == 3", mq_dec.max() == 3)
    mq_dec.pop(1)
    check("after pop(1) max still 3", mq_dec.max() == 3)
    mq_dec.pop(3)
    check("after pop(3) max == 2", mq_dec.max() == 2)

    mq_inc = MonotonicQueue(increasing=True)  # Increasing: front=MIN
    mq_inc.push(3)
    mq_inc.push(1)
    mq_inc.push(2)
    check("increasing queue min == 1", mq_inc.min() == 1)

    # ── Summary ───────────────────────────────────────────────────────────────
    total = passed + failed
    print(f"\n{'='*50}")
    print(f"Results: {passed}/{total} passed, {failed}/{total} failed")
    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    _run_tests()
