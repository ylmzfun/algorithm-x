"""
847. Shortest Path Visiting All Nodes
https://leetcode.com/problems/shortest-path-visiting-all-nodes/

You have an undirected, connected graph of n nodes labeled from 0 to n-1.
You are given an array `graph` where graph[i] is a list of all the nodes
connected with node i by an edge.

Return the length of the shortest path that visits every node.
You may start and stop at any node, revisit nodes multiple times, and
reuse edges.
"""

from __future__ import annotations
from collections import deque


# ──────────────────────────────────────────────────────────────────────────────
# Approach: BFS on State Space (node, visited_bitmask)
# State = (current_node, bitmask_of_visited_nodes).
# The problem reduces to finding the shortest path from any start state
# (i, 1 << i) to any state where bitmask == (1 << n) - 1.
# Time: O(N² × 2^N) — N nodes × 2^N masks, each edge explored once per mask.
# Space: O(N × 2^N)
# ──────────────────────────────────────────────────────────────────────────────
def shortest_path_length(graph: list[list[int]]) -> int:
    """BFS on (node, bitmask) state space."""
    n = len(graph)
    if n == 1:
        return 0

    full_mask = (1 << n) - 1
    # visited[node][mask]
    visited = [[False] * (1 << n) for _ in range(n)]

    q: deque[tuple[int, int, int]] = deque()  # (node, mask, dist)

    # Start from every node
    for i in range(n):
        mask = 1 << i
        q.append((i, mask, 0))
        visited[i][mask] = True

    while q:
        node, mask, dist = q.popleft()
        if mask == full_mask:
            return dist

        for nxt in graph[node]:
            new_mask = mask | (1 << nxt)
            if not visited[nxt][new_mask]:
                visited[nxt][new_mask] = True
                q.append((nxt, new_mask, dist + 1))

    return -1  # unreachable


# ──────────────────────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    def test(label: str, graph: list[list[int]], expected: int):
        result = shortest_path_length(graph)
        ok = result == expected
        print(f"[{label}] {'✓' if ok else '✗'} (got {result}, expected {expected})")

    test("Example 1", [[1, 2, 3], [0], [0], [0]], 4)
    test("Example 2", [[1], [0, 2, 4], [1, 3, 4], [2], [1, 2]], 4)
    test("Single node", [[0]], 0)
    print("\nAll shortest path visiting all nodes tests completed.")
