"""
743. Network Delay Time
https://leetcode.com/problems/network-delay-time/

You are given a network of n nodes, labeled from 1 to n. You are also given
`times`, a list of travel times as directed edges times[i] = (u_i, v_i, w_i),
where u_i is the source node, v_i is the target node, and w_i is the travel
time.

Send a signal from node k. Return the minimum time it takes for all the n
nodes to receive the signal. If it is impossible, return -1.
"""

from __future__ import annotations
import heapq
from collections import defaultdict


# ──────────────────────────────────────────────────────────────────────────────
# Approach: Dijkstra's Algorithm (Min-Heap)
# Time: O((V + E) log V) — each edge relaxed at most once.
# Space: O(V + E)
# ──────────────────────────────────────────────────────────────────────────────
def network_delay_time(times: list[list[int]], n: int, k: int) -> int:
    """Dijkstra's algorithm to find shortest path to all nodes from k."""
    adj: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for u, v, w in times:
        adj[u].append((v, w))

    # dist[node] = shortest distance from k to node
    dist: dict[int, float] = {i: float("inf") for i in range(1, n + 1)}
    dist[k] = 0

    heap: list[tuple[int, int]] = [(0, k)]  # (distance, node)

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))

    max_dist = max(dist.values())
    return int(max_dist) if max_dist < float("inf") else -1


# ──────────────────────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    def test(label: str, times: list[list[int]], n: int, k: int, expected: int):
        result = network_delay_time(times, n, k)
        ok = result == expected
        print(f"[{label}] {'✓' if ok else '✗'} (got {result}, expected {expected})")

    test("Example 1", [[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2, 2)
    test("Example 2 (unreachable)", [[1, 2, 1]], 2, 1, 1)
    test("Unreachable", [[1, 2, 1]], 2, 2, -1)
    print("\nAll network delay time tests completed.")
