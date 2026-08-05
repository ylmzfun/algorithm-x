"""
3. Longest Substring Without Repeating Characters
https://leetcode.com/problems/longest-substring-without-repeating-characters/

Given a string s, find the length of the longest substring without repeating
characters.
"""

from __future__ import annotations


# ──────────────────────────────────────────────────────────────────────────────
# Approach: Sliding Window with HashSet / HashMap
# Maintain a window [left, right] with all unique characters.
# When a duplicate is found at `right`, shrink `left` until the duplicate is
# removed.
# Time: O(N) — each character visited at most twice (left + right).
# Space: O(min(N, 26)) — at most 26 lowercase English letters.
# ──────────────────────────────────────────────────────────────────────────────
def length_of_longest_substring(s: str) -> int:
    """Sliding window — move left past the duplicate's previous position."""
    last_seen: dict[str, int] = {}
    left = 0
    max_len = 0

    for right, ch in enumerate(s):
        if ch in last_seen and last_seen[ch] >= left:
            left = last_seen[ch] + 1
        last_seen[ch] = right
        max_len = max(max_len, right - left + 1)

    return max_len


# ──────────────────────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    def test(label: str, s: str, expected: int):
        result = length_of_longest_substring(s)
        ok = result == expected
        print(f"[{label}] {'✓' if ok else '✗'} (got {result}, expected {expected})")

    test("Example 1", "abcabcbb", 3)  # "abc"
    test("Example 2", "bbbbb", 1)  # "b"
    test("Example 3", "pwwkew", 3)  # "wke"
    test("Empty", "", 0)
    print("\nAll longest substring tests completed.")
