"""
22. Generate Parentheses
https://leetcode.com/problems/generate-parentheses/

Given n pairs of parentheses, write a function to generate all combinations
of well-formed parentheses.
"""

from __future__ import annotations


# ──────────────────────────────────────────────────────────────────────────────
# Approach: Backtracking with pruning
# Track open and close counts. Only add '(' if open < n;
# only add ')' if close < open.
# Time: O(Catalan(n)) ≈ O(4^n / sqrt(n)) — nth Catalan number.
# Space: O(n) recursion depth.
# ──────────────────────────────────────────────────────────────────────────────
def generate_parenthesis(n: int) -> list[str]:
    """Backtrack with open/close counters for valid sequences."""
    result: list[str] = []

    def backtrack(open_cnt: int, close_cnt: int, current: list[str]) -> None:
        if len(current) == 2 * n:
            result.append("".join(current))
            return
        if open_cnt < n:
            current.append("(")
            backtrack(open_cnt + 1, close_cnt, current)
            current.pop()
        if close_cnt < open_cnt:
            current.append(")")
            backtrack(open_cnt, close_cnt + 1, current)
            current.pop()

    backtrack(0, 0, [])
    return result


# ──────────────────────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    def test(label: str, n: int, expected: list[str]):
        result = generate_parenthesis(n)
        ok = sorted(result) == sorted(expected)
        print(f"[{label}] {'✓' if ok else '✗'} (got {result})")

    test("n=1", 1, ["()"])
    test("n=2", 2, ["()()", "(())"])
    test("n=3", 3,
         ["((()))", "(()())", "(())()", "()(())", "()()()"])
    print("\nAll generate parentheses tests completed.")
