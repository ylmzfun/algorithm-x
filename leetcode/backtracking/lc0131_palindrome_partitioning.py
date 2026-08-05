"""
131. Palindrome Partitioning
https://leetcode.com/problems/palindrome-partitioning/

Given a string s, partition s such that every substring of the partition is
a palindrome. Return all possible palindrome partitioning of s.
"""

from __future__ import annotations


# ──────────────────────────────────────────────────────────────────────────────
# Approach: Backtracking with palindrome check
# At each position, try every possible substring starting from `start`.
# If the substring is a palindrome, recurse on the remainder.
# Time: O(N × 2^N) — each character can start a partition; palindrome check
#       is O(N) per candidate.
# Space: O(N) recursion depth.
# ──────────────────────────────────────────────────────────────────────────────
def partition(s: str) -> list[list[str]]:
    """Backtrack: at each index, try all palindrome prefixes."""
    result: list[list[str]] = []

    def is_palindrome(left: int, right: int) -> bool:
        while left < right:
            if s[left] != s[right]:
                return False
            left += 1
            right -= 1
        return True

    def backtrack(start: int, current: list[str]) -> None:
        if start == len(s):
            result.append(current[:])
            return
        for end in range(start, len(s)):
            if is_palindrome(start, end):
                current.append(s[start:end + 1])
                backtrack(end + 1, current)
                current.pop()

    backtrack(0, [])
    return result


# ──────────────────────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    def test(label: str, s: str, expected: list[list[str]]):
        result = partition(s)
        result_set = {tuple(p) for p in result}
        expected_set = {tuple(p) for p in expected}
        ok = result_set == expected_set and len(result) == len(expected)
        print(f"[{label}] {'✓' if ok else '✗'} (got {len(result)} partitions)")

    test("Example 1", "aab", [["a", "a", "b"], ["aa", "b"]])
    test("Example 2", "a", [["a"]])
    test("Example 3", "racecar",
         [["r", "a", "c", "e", "c", "a", "r"],
          ["r", "a", "cec", "a", "r"],
          ["r", "aceca", "r"],
          ["racecar"]])
    print("\nAll palindrome partitioning tests completed.")
