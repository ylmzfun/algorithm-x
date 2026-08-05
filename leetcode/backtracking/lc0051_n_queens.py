"""
51. N-Queens
https://leetcode.com/problems/n-queens/

The n-queens puzzle is the problem of placing n queens on an n x n chessboard
such that no two queens attack each other.

Given an integer n, return all distinct solutions to the n-queens puzzle.
Each solution contains a distinct board configuration of the n-queens'
placement, where 'Q' and '.' both indicate a queen and an empty space,
respectively.
"""

from __future__ import annotations


# ──────────────────────────────────────────────────────────────────────────────
# Approach: Backtracking with boolean arrays for column/diagonal tracking
# Track attacks via:
#   - cols[c]: column c is occupied
#   - diag1[r+c]: main diagonal (top-left to bottom-right)
#   - diag2[r-c+n-1]: anti diagonal (top-right to bottom-left)
# Time: O(N!) — first row has N choices, second N-2, etc.
# Space: O(N)
# ──────────────────────────────────────────────────────────────────────────────
def solve_n_queens(n: int) -> list[list[str]]:
    """Find all N-Queens solutions using column/diagonal tracking."""
    result: list[list[str]] = []
    cols = [False] * n
    diag1 = [False] * (2 * n - 1)  # r + c
    diag2 = [False] * (2 * n - 1)  # r - c + n - 1
    board = [["."] * n for _ in range(n)]

    def backtrack(row: int) -> None:
        if row == n:
            result.append(["".join(r) for r in board])
            return
        for col in range(n):
            d1 = row + col
            d2 = row - col + n - 1
            if cols[col] or diag1[d1] or diag2[d2]:
                continue
            cols[col] = diag1[d1] = diag2[d2] = True
            board[row][col] = "Q"
            backtrack(row + 1)
            board[row][col] = "."
            cols[col] = diag1[d1] = diag2[d2] = False

    backtrack(0)
    return result


# ──────────────────────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    def test(label: str, n: int, expected_count: int):
        result = solve_n_queens(n)
        ok = len(result) == expected_count
        print(f"[{label}] {'✓' if ok else '✗'} (got {len(result)} solutions, expected {expected_count})")

    test("n=1", 1, 1)
    test("n=4", 4, 2)
    test("n=5", 5, 10)
    print("\nAll N-Queens tests completed.")
