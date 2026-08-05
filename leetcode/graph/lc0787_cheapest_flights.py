"""
787. Cheapest Flights Within K Stops
https://leetcode.com/problems/cheapest-flights-within-k-stops/

There are n cities connected by some number of flights. Given flights[i] =
[from_i, to_i, price_i], find the cheapest price from src to dst with at most
k stops. If there is no such route, return -1.
"""

from __future__ import annotations
import heapq
from collections import defaultdict, deque


# ──────────────────────────────────────────────────────────────────────────────
# Approach 1: Bellman-Ford (DP)
# Time: O(K × E)
# Space: O(N)
# Key: After k stops, you've made at most k+1 flights.
# ──────────────────────────────────────────────────────────────────────────────
def find_cheapest_price_bf(
    n: int, flights: list[list[int]], src: int, dst: int, k: int
) -> int:
    """Bellman-Ford: relax edges up to k+1 times."""
    INF = float("inf")
    prev = [INF] * n
    prev[src] = 0

    for _ in range(k + 1):  # at most k stops = k+1 flights
        cur = prev[:]  # copy to prevent using updated values in same iteration
        for u, v, w in flights:
            if prev[u] < INF and prev[u] + w < cur[v]:
                cur[v] = prev[u] + w
        prev = cur

    return int(prev[dst]) if prev[dst] < INF else -1


# ──────────────────────────────────────────────────────────────────────────────
# Approach 2: Dijkstra variant (min-heap with stops count)
# Time: O(E log V) worst, but pruning on stops helps.
# Space: O(V + E)
# ──────────────────────────────────────────────────────────────────────────────
def find_cheapest_price_dijkstra(
    n: int, flights: list[list[int]], src: int, dst: int, k: int
) -> int:
    """Dijkstra tracking (cost, node, stops)."""
    adj: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for u, v, w in flights:
        adj[u].append((v, w))

    # min-heap: (cost, node, stops_used)
    heap: list[tuple[int, int, int]] = [(0, src, 0)]
    # Minimum stops to reach each node (pruning)
    best_stops: dict[int, int] = {}

    while heap:
        cost, node, stops = heapq.heappop(heap)
        if node == dst:
            return cost
        if stops > k:
            continue
        if node in best_stops and best_stops[node] <= stops:
            continue
        best_stops[node] = stops

        for nxt, w in adj[node]:
            heapq.heappush(heap, (cost + w, nxt, stops + 1))

    return -1


# ──────────────────────────────────────────────────────────────────────────────
# Approach 3: BFS with pruning
# Time: O(K × E)
# Space: O(N)
# ──────────────────────────────────────────────────────────────────────────────
def find_cheapest_price_bfs(
    n: int, flights: list[list[int]], src: int, dst: int, k: int
) -> int:
    """BFS level by level (stops), tracking minimum cost per node."""
    adj: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for u, v, w in flights:
        adj[u].append((v, w))

    INF = float("inf")
    costs = [INF] * n
    costs[src] = 0

    q: deque[tuple[int, int, int]] = deque([(src, 0, 0)])  # node, cost, stops

    while q:
        node, cost, stops = q.popleft()
        if stops > k:
            continue
        for nxt, w in adj[node]:
            new_cost = cost + w
            if new_cost < costs[nxt]:
                costs[nxt] = new_cost
                q.append((nxt, new_cost, stops + 1))

    return int(costs[dst]) if costs[dst] < INF else -1


# ──────────────────────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    def test(
        label: str, n: int, flights: list[list[int]],
        src: int, dst: int, k: int, expected: int,
    ):
        methods = [
            ("Bellman-Ford", find_cheapest_price_bf),
            ("Dijkstra", find_cheapest_price_dijkstra),
            ("BFS", find_cheapest_price_bfs),
        ]
        for name, fn in methods:
            result = fn(n, flights, src, dst, k)
            ok = result == expected
            print(f"[{label}] {name}: {'✓' if ok else '✗'} (got {result}, expected {expected})")

    test("Example 1", 4, [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]], 0, 3, 1, 700)
    test("Example 2", 3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 1, 200)
    test("Example 3", 3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 0, 500)
    test("No route", 3, [[0, 1, 100]], 0, 2, 1, -1)
    print("\nAll cheapest flights tests completed.")
