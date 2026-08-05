"""
76. Minimum Window Substring
https://leetcode.com/problems/minimum-window-substring/

Given two strings s and t of lengths m and n respectively, return the minimum
window substring of s such that every character in t (including duplicates)
is included in the window. If there is no such substring, return "".
"""

from __future__ import annotations
from collections import Counter


# ──────────────────────────────────────────────────────────────────────────────
# Approach: Sliding Window with character frequency counters
# Maintain `needed` = frequency of chars in t, and `window` counts.
# Expand right until valid, then contract left to minimize.
# Time: O(M + N) — each char of s processed at most twice.
# Space: O(1) — at most 52 keys (upper/lowercase English letters).
# ──────────────────────────────────────────────────────────────────────────────
def min_window(s: str, t: str) -> str:
    """Sliding window: expand right, contract left when valid."""
    if not s or not t:
        return ""

    need = Counter(t)
    required = len(need)
    window: dict[str, int] = {}
    formed = 0

    left = 0
    min_len = float("inf")
    min_start = 0

    for right, ch in enumerate(s):
        window[ch] = window.get(ch, 0) + 1
        if ch in need and window[ch] == need[ch]:
            formed += 1

        # Contract from left while the window is valid
        while formed == required:
            cur_len = right - left + 1
            if cur_len < min_len:
                min_len = cur_len
                min_start = left

            left_ch = s[left]
            window[left_ch] -= 1
            if left_ch in need and window[left_ch] < need[left_ch]:
                formed -= 1
            left += 1

    return s[min_start:min_start + min_len] if min_len != float("inf") else ""


# ──────────────────────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    def test(label: str, s: str, t: str, expected: str):
        result = min_window(s, t)
        ok = result == expected
        print(f"[{label}] {'✓' if ok else '✗'} (got '{result}', expected '{expected}')")

    test("Example 1", "ADOBECODEBANC", "ABC", "BANC")
    test("Example 2", "a", "a", "a")
    test("Example 3", "a", "aa", "")
    print("\nAll minimum window substring tests completed.")
