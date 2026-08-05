"""
49. Group Anagrams
https://leetcode.com/problems/group-anagrams/

Given an array of strings strs, group the anagrams together.
You can return the answer in any order.

An anagram is a word or phrase formed by rearranging the letters of a
different word or phrase, typically using all the original letters exactly
once.
"""

from __future__ import annotations
from collections import defaultdict


# ──────────────────────────────────────────────────────────────────────────────
# Approach 1: Sort each string as key
# Time: O(N × K log K) where N = len(strs), K = max string length.
# Space: O(N × K)
# ──────────────────────────────────────────────────────────────────────────────
def group_anagrams_sort(strs: list[str]) -> list[list[str]]:
    """Sort each word to derive anagram key."""
    groups: dict[str, list[str]] = defaultdict(list)
    for s in strs:
        key = "".join(sorted(s))
        groups[key].append(s)
    return list(groups.values())


# ──────────────────────────────────────────────────────────────────────────────
# Approach 2: Character count as key
# Time: O(N × K)
# Space: O(N × K)
# ──────────────────────────────────────────────────────────────────────────────
def group_anagrams_count(strs: list[str]) -> list[list[str]]:
    """Character frequency tuple as anagram key."""
    groups: dict[tuple[int, ...], list[str]] = defaultdict(list)
    for s in strs:
        count = [0] * 26
        for ch in s:
            count[ord(ch) - ord("a")] += 1
        groups[tuple(count)].append(s)
    return list(groups.values())


# ──────────────────────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    def normalize(result: list[list[str]]) -> set[frozenset[str]]:
        return {frozenset(g) for g in result}

    def test(label: str, strs: list[str], expected: list[list[str]]):
        methods = [
            ("Sort", group_anagrams_sort),
            ("Count", group_anagrams_count),
        ]
        for name, fn in methods:
            result = fn(strs)
            ok = normalize(result) == normalize(expected)
            print(f"[{label}] {name}: {'✓' if ok else '✗'} (got {result})")

    test("Example 1",
         ["eat", "tea", "tan", "ate", "nat", "bat"],
         [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]])

    test("Example 2", [""], [[""]])
    test("Example 3", ["a"], [["a"]])
    print("\nAll group anagrams tests completed.")
