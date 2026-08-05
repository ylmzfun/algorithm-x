"""
79. Word Search
https://leetcode.com/problems/word-search/

Given an m x n grid of characters board and a string word, return true if
word exists in the grid.

The word can be constructed from letters of sequentially adjacent cells,
where adjacent cells are horizontally or vertically neighboring. The same
letter cell may not be used more than once.
"""

from __future__ import annotations


# ──────────────────────────────────────────────────────────────────────────────
# Approach: DFS Backtracking on Grid
# For each cell matching word[0], DFS in four directions marking visited.
# Time: O(M × N × 4^L) worst, where L = len(word); pruned by early mismatch.
# Space: O(L) recursion depth.
# ──────────────────────────────────────────────────────────────────────────────
def exist(board: list[list[str]], word: str) -> bool:
    """DFS with in-place visited marking."""
    if not board or not board[0]:
        return False

    rows, cols = len(board), len(board[0])
    dirs = ((1, 0), (-1, 0), (0, 1), (0, -1))

    def dfs(r: int, c: int, idx: int) -> bool:
        if idx == len(word):
            return True
        if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != word[idx]:
            return False

        # Mark visited in-place by temporarily changing the cell
        temp = board[r][c]
        board[r][c] = "#"

        for dr, dc in dirs:
            if dfs(r + dr, c + dc, idx + 1):
                board[r][c] = temp  # restore before returning
                return True

        board[r][c] = temp
        return False

    for r in range(rows):
        for c in range(cols):
            if board[r][c] == word[0] and dfs(r, c, 0):
                return True

    return False


# ──────────────────────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    def test(label: str, board: list[list[str]], word: str, expected: bool):
        import copy
        result = exist(copy.deepcopy(board), word)
        ok = result == expected
        print(f"[{label}] {'✓' if ok else '✗'} (got {result}, expected {expected})")

    test("Example 1", [
        ["A", "B", "C", "E"],
        ["S", "F", "C", "S"],
        ["A", "D", "E", "E"],
    ], "ABCCED", True)

    test("Example 2", [
        ["A", "B", "C", "E"],
        ["S", "F", "C", "S"],
        ["A", "D", "E", "E"],
    ], "SEE", True)

    test("Example 3", [
        ["A", "B", "C", "E"],
        ["S", "F", "C", "S"],
        ["A", "D", "E", "E"],
    ], "ABCB", False)

    test("Single cell", [["a"]], "a", True)
    print("\nAll word search tests completed.")
