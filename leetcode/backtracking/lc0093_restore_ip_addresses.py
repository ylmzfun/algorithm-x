"""
93. Restore IP Addresses
https://leetcode.com/problems/restore-ip-addresses/

A valid IP address consists of exactly four integers separated by single dots.
Each integer is between 0 and 255 (inclusive) and cannot have leading zeros.

Given a string s containing only digits, return all possible valid IP
addresses that can be formed by inserting dots into s.
"""

from __future__ import annotations


# ──────────────────────────────────────────────────────────────────────────────
# Approach: Backtracking with segment validation
# Build up to 4 segments. For each segment, try substrings of length 1-3.
# Validate: 0-255 range, no leading zeros (except "0" itself).
# Time: O(1) — at most 3^4 = 81 combinations.
# Space: O(1)
# ──────────────────────────────────────────────────────────────────────────────
def restore_ip_addresses(s: str) -> list[str]:
    """Backtracking: build 4 segments, each 1-3 chars, validate range."""
    result: list[str] = []

    def is_valid_segment(seg: str) -> bool:
        if len(seg) > 1 and seg[0] == "0":
            return False
        return 0 <= int(seg) <= 255

    def backtrack(start: int, segments: list[str]) -> None:
        if len(segments) == 4:
            if start == len(s):
                result.append(".".join(segments))
            return
        # Try segments of length 1, 2, 3
        for length in range(1, 4):
            if start + length > len(s):
                break
            seg = s[start:start + length]
            if is_valid_segment(seg):
                segments.append(seg)
                backtrack(start + length, segments)
                segments.pop()

    backtrack(0, [])
    return result


# ──────────────────────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    def test(label: str, s: str, expected: list[str]):
        result = restore_ip_addresses(s)
        ok = sorted(result) == sorted(expected)
        print(f"[{label}] {'✓' if ok else '✗'} (got {result})")

    test("Example 1", "25525511135", ["255.255.11.135", "255.255.111.35"])
    test("Example 2", "0000", ["0.0.0.0"])
    test("Example 3", "101023",
         ["1.0.10.23", "1.0.102.3", "10.1.0.23", "10.10.2.3", "101.0.2.3"])
    print("\nAll restore IP addresses tests completed.")
