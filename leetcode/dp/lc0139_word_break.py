"""
LeetCode 139: Word Break

Given a string s and a dictionary of strings wordDict, return true if
s can be segmented into a space-separated sequence of one or more
dictionary words.

Note that the same word in the dictionary may be reused multiple times
in the segmentation.

Constraints:
- 1 <= s.length <= 300
- 1 <= wordDict.length <= 1000
- 1 <= wordDict[i].length <= 20
- s and wordDict[i] consist of only lowercase English letters.
- All the strings of wordDict are unique.
"""

from typing import List


class Solution:
    # ── DP with Set O(n·L²) or O(n·m·L) ────────────────────────────────────
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        """
        dp[i] = can s[:i] be segmented?
        dp[0] = True (empty string)
        dp[i] = any(dp[j] and s[j:i] in wordSet for j < i)
        """
        word_set = set(wordDict)
        n = len(s)
        dp = [False] * (n + 1)
        dp[0] = True

        max_len = max((len(w) for w in wordDict), default=0)

        for i in range(1, n + 1):
            # Only check last max_len characters
            start = max(0, i - max_len)
            for j in range(start, i):
                if dp[j] and s[j:i] in word_set:
                    dp[i] = True
                    break

        return dp[n]

    # ── DP with Trie (prefix tree) O(n·L) ─────────────────────────────────
    def wordBreak_trie(self, s: str, wordDict: List[str]) -> bool:
        """Use a Trie for efficient prefix lookups."""

        class TrieNode:
            __slots__ = ('children', 'is_word')
            def __init__(self):
                self.children = {}
                self.is_word = False

        root = TrieNode()
        for word in wordDict:
            node = root
            for ch in word:
                if ch not in node.children:
                    node.children[ch] = TrieNode()
                node = node.children[ch]
            node.is_word = True

        n = len(s)
        dp = [False] * (n + 1)
        dp[0] = True

        for i in range(n):
            if not dp[i]:
                continue
            node = root
            for j in range(i, n):
                ch = s[j]
                if ch not in node.children:
                    break
                node = node.children[ch]
                if node.is_word:
                    dp[j + 1] = True

        return dp[n]


if __name__ == "__main__":
    sol = Solution()
    tests = [
        ("leetcode", ["leet", "code"], True),
        ("applepenapple", ["apple", "pen"], True),
        ("catsandog", ["cats", "dog", "sand", "and", "cat"], False),
        ("aaaaaaa", ["aaaa", "aaa"], True),
        ("a", ["a"], True),
        ("ab", ["a", "b"], True),
    ]

    for s, wordDict, expected in tests:
        r1 = sol.wordBreak(s, wordDict)
        r2 = sol.wordBreak_trie(s, wordDict)
        ok = r1 == r2 == expected
        print(f"{s!r} {wordDict} → Set={r1}, Trie={r2} | {'✓' if ok else '✗'}")
