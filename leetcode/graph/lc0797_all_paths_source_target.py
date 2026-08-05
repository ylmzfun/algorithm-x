"""
797. All Paths From Source to Target
https://leetcode.com/problems/all-paths-from-source-to-target/

Given a directed acyclic graph (DAG) of n nodes labeled from 0 to n-1,
find all possible paths from node 0 to node n-1 and return them in any order.

The graph is given as graph[i] is a list of all nodes you can visit from node
i (i.e., there is a directed edge from node i to node graph[i][j]).
"""

from __future__ import annotations


# ──────────────────────────────────────────────────────────────────────────────
# Approach: DFS Backtracking
# Since the graph is a DAG, we don't need cycle detection.
# Time: O(2^V × V) worst case — number of paths can be exponential.
# Space: O(V) recursion depth + O(V) per path.
# ──────────────────────────────────────────────────────────────────────────────
def all_paths_source_target(graph: list[list[int]]) -> list[list[int]]:
    """DFS backtracking to find all paths from 0 to n-1."""
    n = len(graph)
    result: list[list[int]] = []

    def dfs(node: int, path: list[int]) -> None:
        if node == n - 1:
            result.append(path[:])
            return
        for nxt in graph[node]:
            path.append(nxt)
            dfs(nxt, path)
            path.pop()

    dfs(0, [0])
    return result


# ──────────────────────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    def test(label: str, graph: list[list[int]], expected: list[list[int]]):
        result = all_paths_source_target(graph)
        result_sorted = sorted([tuple(p) for p in result])
        expected_sorted = sorted([tuple(p) for p in expected])
        ok = result_sorted == expected_sorted
        print(f"[{label}] {'✓' if ok else '✗'} (got {result})")

    test("Example 1", [[1, 2], [3], [3], []], [[0, 1, 3], [0, 2, 3]])
    test("Example 2", [[4, 3, 1], [3, 2, 4], [3], [4], []],
         [[0, 4], [0, 3, 4], [0, 1, 3, 4], [0, 1, 2, 3, 4], [0, 1, 4]])

    test("Single path", [[1], [2], []], [[0, 1, 2]])
    print("\nAll all paths source target tests completed.")
