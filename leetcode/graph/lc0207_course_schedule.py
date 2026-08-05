"""
207. Course Schedule
https://leetcode.com/problems/course-schedule/

There are a total of `numCourses` courses labeled from 0 to numCourses-1.
You are given an array `prerequisites` where prerequisites[i] = [a_i, b_i]
indicates that you must take course b_i first if you want to take course a_i.

Return true if you can finish all courses (graph is a DAG), otherwise false.
"""

from __future__ import annotations
from collections import defaultdict, deque


# ──────────────────────────────────────────────────────────────────────────────
# Approach 1: Kahn's Algorithm (BFS Topological Sort)
# Time: O(V + E) — build graph then process each vertex/edge once.
# Space: O(V + E) — adjacency list and in-degree array.
# ──────────────────────────────────────────────────────────────────────────────
def can_finish_bfs(num_courses: int, prerequisites: list[list[int]]) -> bool:
    """Kahn's algorithm – remove nodes with in-degree 0 iteratively."""
    adj: dict[int, list[int]] = defaultdict(list)
    indegree = [0] * num_courses

    for a, b in prerequisites:
        adj[b].append(a)
        indegree[a] += 1

    q: deque[int] = deque(i for i in range(num_courses) if indegree[i] == 0)
    taken = 0

    while q:
        course = q.popleft()
        taken += 1
        for nxt in adj[course]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                q.append(nxt)

    return taken == num_courses


# ──────────────────────────────────────────────────────────────────────────────
# Approach 2: DFS Cycle Detection (3-colour)
# Time: O(V + E)
# Space: O(V + E)
# ──────────────────────────────────────────────────────────────────────────────
def can_finish_dfs(num_courses: int, prerequisites: list[list[int]]) -> bool:
    """DFS with three states: 0=unvisited, 1=visiting, 2=done."""
    adj: dict[int, list[int]] = defaultdict(list)
    for a, b in prerequisites:
        adj[b].append(a)

    WHITE, GRAY, BLACK = 0, 1, 2
    state = [WHITE] * num_courses

    def has_cycle(course: int) -> bool:
        if state[course] == GRAY:
            return True
        if state[course] == BLACK:
            return False
        state[course] = GRAY
        for nxt in adj[course]:
            if has_cycle(nxt):
                return True
        state[course] = BLACK
        return False

    for c in range(num_courses):
        if state[c] == WHITE and has_cycle(c):
            return False
    return True


# ──────────────────────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    def test(label: str, n: int, prereqs: list[list[int]], expected: bool):
        methods = [
            ("Kahn BFS", can_finish_bfs),
            ("DFS", can_finish_dfs),
        ]
        for name, fn in methods:
            result = fn(n, prereqs)
            ok = result == expected
            print(f"[{label}] {name}: {'✓' if ok else '✗'} (got {result}, expected {expected})")

    test("Example 1", 2, [[1, 0]], True)
    test("Example 2", 2, [[1, 0], [0, 1]], False)
    test("No prereqs", 3, [], True)
    print("\nAll course schedule tests completed.")
