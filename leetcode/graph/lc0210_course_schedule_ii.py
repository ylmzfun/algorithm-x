"""
210. Course Schedule II
https://leetcode.com/problems/course-schedule-ii/

Return the ordering of courses you should take to finish all courses.
If there are many valid orderings, return any of them.
If it is impossible to finish all courses, return an empty array.
"""

from __future__ import annotations
from collections import defaultdict, deque


# ──────────────────────────────────────────────────────────────────────────────
# Approach 1: Kahn's Algorithm (BFS)
# Time: O(V + E)
# Space: O(V + E)
# ──────────────────────────────────────────────────────────────────────────────
def find_order_bfs(num_courses: int, prerequisites: list[list[int]]) -> list[int]:
    """Kahn's algorithm – produces one valid topological order."""
    adj: dict[int, list[int]] = defaultdict(list)
    indegree = [0] * num_courses

    for a, b in prerequisites:
        adj[b].append(a)
        indegree[a] += 1

    q: deque[int] = deque(i for i in range(num_courses) if indegree[i] == 0)
    order: list[int] = []

    while q:
        course = q.popleft()
        order.append(course)
        for nxt in adj[course]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                q.append(nxt)

    return order if len(order) == num_courses else []


# ──────────────────────────────────────────────────────────────────────────────
# Approach 2: DFS Post-order
# Time: O(V + E)
# Space: O(V + E)
# ──────────────────────────────────────────────────────────────────────────────
def find_order_dfs(num_courses: int, prerequisites: list[list[int]]) -> list[int]:
    """DFS post-order reverse yields a topological order."""
    adj: dict[int, list[int]] = defaultdict(list)
    for a, b in prerequisites:
        adj[b].append(a)

    WHITE, GRAY, BLACK = 0, 1, 2
    state = [WHITE] * num_courses
    order: list[int] = []

    def dfs(course: int) -> bool:
        """Return True if a cycle is detected."""
        if state[course] == GRAY:
            return True
        if state[course] == BLACK:
            return False
        state[course] = GRAY
        for nxt in adj[course]:
            if dfs(nxt):
                return True
        state[course] = BLACK
        order.append(course)
        return False

    for c in range(num_courses):
        if state[c] == WHITE and dfs(c):
            return []

    order.reverse()
    return order


# ──────────────────────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    def is_valid_order(n: int, prereqs: list[list[int]], order: list[int]) -> bool:
        if len(order) != n:
            return False
        pos = {c: i for i, c in enumerate(order)}
        for a, b in prereqs:
            if pos[b] > pos[a]:  # b must come before a
                return False
        return True

    def test(label: str, n: int, prereqs: list[list[int]], possible: bool):
        methods = [
            ("Kahn BFS", find_order_bfs),
            ("DFS", find_order_dfs),
        ]
        for name, fn in methods:
            result = fn(n, prereqs)
            if possible:
                ok = is_valid_order(n, prereqs, result)
            else:
                ok = (result == [])
            print(f"[{label}] {name}: {'✓' if ok else '✗'} (got {result})")

    test("Example 1", 2, [[1, 0]], True)
    test("Example 2", 4, [[1, 0], [2, 0], [3, 1], [3, 2]], True)
    test("Example 3 (impossible)", 2, [[1, 0], [0, 1]], False)
    print("\nAll course schedule II tests completed.")
