"""
17. Letter Combinations of a Phone Number
https://leetcode.com/problems/letter-combinations-of-a-phone-number/

Given a string containing digits from 2-9 inclusive, return all possible
letter combinations that the number could represent. Return the answer in
any order.
"""

from __future__ import annotations


# ──────────────────────────────────────────────────────────────────────────────
# Approach: Backtracking
# For each digit, iterate over its mapped letters and recurse.
# Time: O(4^N) — at most 4 letters per digit, N = len(digits).
# Space: O(N) recursion depth + O(4^N) for output.
# ──────────────────────────────────────────────────────────────────────────────
KEYPAD: dict[str, str] = {
    "2": "abc", "3": "def", "4": "ghi", "5": "jkl",
    "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz",
}


def letter_combinations(digits: str) -> list[str]:
    """Backtrack through digit-to-letter mappings."""
    if not digits:
        return []

    result: list[str] = []

    def backtrack(idx: int, current: list[str]) -> None:
        if idx == len(digits):
            result.append("".join(current))
            return
        for ch in KEYPAD[digits[idx]]:
            current.append(ch)
            backtrack(idx + 1, current)
            current.pop()

    backtrack(0, [])
    return result


# ──────────────────────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    def test(label: str, digits: str, expected: list[str]):
        result = letter_combinations(digits)
        ok = sorted(result) == sorted(expected)
        print(f"[{label}] {'✓' if ok else '✗'} (got {result})")

    test("Example 1", "23",
         ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"])
    test("Example 2", "", [])
    test("Example 3", "2", ["a", "b", "c"])
    print("\nAll letter combinations tests completed.")
