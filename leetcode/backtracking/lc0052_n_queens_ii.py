"""
52. N-Queens II
https://leetcode.com/problems/n-queens-ii/

The n-queens puzzle is the problem of placing n queens on an n x n chessboard
such that no two queens attack each other.

Given an integer n, return the number of distinct solutions to the n-queens
puzzle.
"""

from __future__ import annotations


# ──────────────────────────────────────────────────────────────────────────────
# Approach: Backtracking with boolean arrays (count only)
# Same logic as N-Queens I, but increment counter instead of building board.
# Time: O(N!)
# Space: O(N)
# ──────────────────────────────────────────────────────────────────────────────
def total_n_queens(n: int) -> int:
    """Count N-Queens solutions using column/diagonal tracking."""
    cols = [False] * n
    diag1 = [False] * (2 * n - 1)  # r + c
    diag2 = [False] * (2 * n - 1)  # r - c + n - 1
    count = 0

    def backtrack(row: int) -> None:
        nonlocal count
        if row == n:
            count += 1
            return
        for col in range(n):
            d1 = row + col
            d2 = row - col + n - 1
            if cols[col] or diag1[d1] or diag2[d2]:
                continue
            cols[col] = diag1[d1] = diag2[d2] = True
            backtrack(row + 1)
            cols[col] = diag1[d1] = diag2[d2] = False

    backtrack(0)
    return count


# ──────────────────────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    def test(label: str, n: int, expected: int):
        result = total_n_queens(n)
        ok = result == expected
        print(f"[{label}] {'✓' if ok else '✗'} (got {result}, expected {expected})")

    test("n=1", 1, 1)
    test("n=4", 4, 2)
    test("n=8", 8, 92)
    print("\nAll N-Queens II tests completed.")
