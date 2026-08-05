"""
399. Evaluate Division
https://leetcode.com/problems/evaluate-division/

You are given an array of variable pairs `equations` and an array of real
numbers `values`, where equations[i] = [A_i, B_i] and values[i] represent
the equation A_i / B_i = values[i].

Also given `queries` where queries[j] = [C_j, D_j]; return the answer for
each query C_j / D_j, or -1.0 if the answer cannot be determined.
"""

from __future__ import annotations
from collections import defaultdict


# ──────────────────────────────────────────────────────────────────────────────
# Approach 1: Graph + DFS with path product
# Time: O(Q × (V + E)) — for each query, DFS may traverse all nodes/edges.
# Space: O(V + E)
# ──────────────────────────────────────────────────────────────────────────────
def calc_equation_dfs(
    equations: list[list[str]],
    values: list[float],
    queries: list[list[str]],
) -> list[float]:
    """Build weighted graph, DFS for each query multiplying edge weights."""
    graph: dict[str, dict[str, float]] = defaultdict(dict)

    for (a, b), v in zip(equations, values):
        graph[a][b] = v
        graph[b][a] = 1.0 / v

    def dfs(src: str, dst: str, visited: set[str]) -> float:
        if src not in graph or dst not in graph:
            return -1.0
        if src == dst:
            return 1.0
        visited.add(src)
        for nxt, weight in graph[src].items():
            if nxt not in visited:
                result = dfs(nxt, dst, visited)
                if result != -1.0:
                    return weight * result
        return -1.0

    return [dfs(a, b, set()) for a, b in queries]


# ──────────────────────────────────────────────────────────────────────────────
# Approach 2: Union-Find with weights
# Time: O((E + Q) × α(N)) ≈ O(E + Q)
# Space: O(N)
# ──────────────────────────────────────────────────────────────────────────────
def calc_equation_uf(
    equations: list[list[str]],
    values: list[float],
    queries: list[list[str]],
) -> list[float]:
    """Union-Find with ratio tracking per component."""

    class WeightedUF:
        def __init__(self) -> None:
            self.parent: dict[str, str] = {}
            self.ratio: dict[str, float] = {}

        def find(self, x: str) -> str:
            if x not in self.parent:
                self.parent[x] = x
                self.ratio[x] = 1.0
            if self.parent[x] != x:
                orig_parent = self.parent[x]
                self.parent[x] = self.find(self.parent[x])
                self.ratio[x] *= self.ratio[orig_parent]
            return self.parent[x]

        def union(self, a: str, b: str, value: float) -> None:
            ra, rb = self.find(a), self.find(b)
            if ra == rb:
                return
            self.parent[ra] = rb
            self.ratio[ra] = value * self.ratio[b] / self.ratio[a]

        def query(self, a: str, b: str) -> float:
            if a not in self.parent or b not in self.parent:
                return -1.0
            ra, rb = self.find(a), self.find(b)
            if ra != rb:
                return -1.0
            return self.ratio[a] / self.ratio[b]

    uf = WeightedUF()
    for (a, b), v in zip(equations, values):
        uf.union(a, b, v)

    return [uf.query(a, b) for a, b in queries]


# ──────────────────────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    def test(
        label: str,
        eqs: list[list[str]],
        vals: list[float],
        qs: list[list[str]],
        expected: list[float],
    ):
        methods = [
            ("DFS", calc_equation_dfs),
            ("UF", calc_equation_uf),
        ]
        for name, fn in methods:
            result = fn(eqs, vals, qs)
            ok = all(abs(r - e) < 1e-5 for r, e in zip(result, expected))
            print(f"[{label}] {name}: {'✓' if ok else '✗'} (got {result})")

    test(
        "Example 1",
        [["a", "b"], ["b", "c"]],
        [2.0, 3.0],
        [["a", "c"], ["b", "a"], ["a", "e"], ["a", "a"], ["x", "x"]],
        [6.0, 0.5, -1.0, 1.0, -1.0],
    )

    test(
        "Example 2",
        [["a", "b"], ["b", "c"], ["bc", "cd"]],
        [1.5, 2.5, 5.0],
        [["a", "c"], ["c", "b"], ["bc", "cd"], ["cd", "bc"]],
        [3.75, 0.4, 5.0, 0.2],
    )

    test("Disconnected", [["a", "b"]], [0.5], [["a", "c"]], [-1.0])
    print("\nAll evaluate division tests completed.")
