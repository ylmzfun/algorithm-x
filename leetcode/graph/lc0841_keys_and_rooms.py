"""
841. Keys and Rooms
https://leetcode.com/problems/keys-and-rooms/

There are n rooms labeled from 0 to n-1 and all the rooms are locked except
for room 0. Each room may contain a set of distinct keys, and each key has a
number on it, denoting which room it unlocks.

You can move freely between rooms once you have unlocked them.
Return true if you can visit all the rooms, or false otherwise.
"""

from __future__ import annotations
from collections import deque


# ──────────────────────────────────────────────────────────────────────────────
# Approach 1: DFS
# Time: O(V + E) — visit each room and process each key once.
# Space: O(V) — visited set + recursion stack.
# ──────────────────────────────────────────────────────────────────────────────
def can_visit_all_rooms_dfs(rooms: list[list[int]]) -> bool:
    """DFS traversal from room 0, collecting keys."""
    n = len(rooms)
    visited = [False] * n

    def dfs(room: int) -> None:
        visited[room] = True
        for key in rooms[room]:
            if not visited[key]:
                dfs(key)

    dfs(0)
    return all(visited)


# ──────────────────────────────────────────────────────────────────────────────
# Approach 2: BFS
# Time: O(V + E)
# Space: O(V)
# ──────────────────────────────────────────────────────────────────────────────
def can_visit_all_rooms_bfs(rooms: list[list[int]]) -> bool:
    """BFS traversal from room 0, collecting keys."""
    n = len(rooms)
    visited = [False] * n
    visited[0] = True
    q: deque[int] = deque([0])
    count = 1

    while q:
        room = q.popleft()
        for key in rooms[room]:
            if not visited[key]:
                visited[key] = True
                count += 1
                q.append(key)

    return count == n


# ──────────────────────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    def test(label: str, rooms: list[list[int]], expected: bool):
        methods = [
            ("DFS", can_visit_all_rooms_dfs),
            ("BFS", can_visit_all_rooms_bfs),
        ]
        for name, fn in methods:
            result = fn(rooms)
            ok = result == expected
            print(f"[{label}] {name}: {'✓' if ok else '✗'} (got {result}, expected {expected})")

    test("Example 1", [[1], [2], [3], []], True)
    test("Example 2", [[1, 3], [3, 0, 1], [2], [0]], False)
    test("Single room", [[]], True)
    print("\nAll keys and rooms tests completed.")
