"""
Aho-Corasick Automaton
=======================

An efficient string matching algorithm that finds all occurrences of a set
of patterns in a text simultaneously.

The algorithm:
    1. Builds a trie from the patterns.
    2. Adds failure links (like KMP's partial match table) to each node,
       pointing to the longest proper suffix that is also a prefix in the trie.
    3. Traverses the text, following failure links when a character mismatch
       occurs, and reports all pattern matches.

Time Complexity:
    - Build: O(sum of pattern lengths)
    - Search: O(text length + number of matches)

Space Complexity: O(sum of pattern lengths * alphabet_size)

Examples:
    >>> ac = AhoCorasick(["he", "she", "his", "hers"])
    >>> ac.search("ushers")
    {'she': [1], 'he': [2], 'hers': [2]}
"""

from typing import Dict, List, Set
from collections import deque


class AhoCorasick:
    """Aho-Corasick automaton for multi-pattern string matching.

    Builds a trie with failure links and output links, then searches
    text in a single pass.

    Examples:
        >>> ac = AhoCorasick(["a", "ab", "bab", "bc", "bca", "c", "caa"])
        >>> ac.search("abccab")
        {'a': [0, 4], 'ab': [0], 'c': [2, 3], 'bc': [1], 'bca': [1]}
    """

    class _Node:
        """A node in the Aho-Corasick automaton."""
        __slots__ = ("children", "fail", "output")

        def __init__(self) -> None:
            self.children: Dict[str, "AhoCorasick._Node"] = {}
            self.fail: "AhoCorasick._Node | None" = None
            self.output: List[str] = []  # Patterns ending at this node

    def __init__(self, patterns: List[str]) -> None:
        """Build automaton from a list of patterns.

        Args:
            patterns: List of strings to search for.
        """
        self._patterns = patterns
        self._root = self._Node()

        # Phase 1: Build trie
        for pattern in patterns:
            self._insert(pattern)

        # Phase 2: Build failure links (BFS)
        self._build_failure_links()

    def _insert(self, pattern: str) -> None:
        """Insert a pattern into the trie."""
        node = self._root
        for ch in pattern:
            if ch not in node.children:
                node.children[ch] = self._Node()
            node = node.children[ch]
        node.output.append(pattern)

    def _build_failure_links(self) -> None:
        """Build failure links using BFS.

        For each node, its failure link points to the longest proper suffix
        that is also a prefix of some pattern.

        Time Complexity: O(total pattern length * alphabet size)
        """
        queue = deque()

        # Initialize failure links for depth-1 nodes
        for ch, child in self._root.children.items():
            child.fail = self._root
            queue.append(child)

        # BFS
        while queue:
            current = queue.popleft()

            for ch, child in current.children.items():
                # Find failure link for child
                fail = current.fail
                while fail is not None and ch not in fail.children:
                    fail = fail.fail
                child.fail = fail.children[ch] if fail else self._root

                # Merge outputs: child inherits output from its failure node
                child.output.extend(child.fail.output)

                queue.append(child)

    def search(self, text: str) -> Dict[str, List[int]]:
        """Search for all pattern occurrences in `text`.

        Args:
            text: The text to search in.

        Returns:
            Dict mapping each pattern to a list of starting indices
            where it occurs in the text. Patterns that don't appear
            are not included in the result.

        Time Complexity: O(|text| + number_of_matches)
        """
        result: Dict[str, List[int]] = {}
        node = self._root

        for i, ch in enumerate(text):
            # Follow failure links while character mismatch
            while node is not self._root and ch not in node.children:
                node = node.fail  # type: ignore[assignment]

            # If match found, advance
            if ch in node.children:
                node = node.children[ch]
            else:
                # Stay at root (implicit, since node is already root)
                pass

            # Report all matches at this node
            for pattern in node.output:
                start = i - len(pattern) + 1
                if pattern not in result:
                    result[pattern] = []
                result[pattern].append(start)

        return result

    def search_unique_patterns(self, text: str) -> Dict[str, int]:
        """Search for the first occurrence of each pattern.

        Returns:
            Dict mapping pattern → first starting index, or -1 if not found.

        Time Complexity: O(|text| + number_of_matches)
        """
        result: Dict[str, int] = {p: -1 for p in self._patterns}
        node = self._root

        for i, ch in enumerate(text):
            while node is not self._root and ch not in node.children:
                node = node.fail  # type: ignore[assignment]

            if ch in node.children:
                node = node.children[ch]

            for pattern in node.output:
                if result[pattern] == -1:
                    result[pattern] = i - len(pattern) + 1

        return result

    def __repr__(self) -> str:
        return f"AhoCorasick(patterns={len(self._patterns)})"


# ─── Tests ────────────────────────────────────────────────────────────────────


def _run_tests() -> None:
    """Run all tests and report results."""
    import sys

    passed = 0
    failed = 0

    def check(description: str, condition: bool) -> None:
        nonlocal passed, failed
        if condition:
            passed += 1
            print(f"  ✓ {description}")
        else:
            failed += 1
            print(f"  ✗ {description}", file=sys.stderr)

    # ── Basic ─────────────────────────────────────────────────────────────────
    print("Basic search:")
    ac = AhoCorasick(["he", "she", "his", "hers"])
    result = ac.search("ushers")
    check("'she' at [1]", result.get("she") == [1])
    check("'he' at [2]", result.get("he") == [2])
    check("'hers' at [2]", result.get("hers") == [2])
    check("'his' not found", "his" not in result)

    # ── Overlapping patterns ─────────────────────────────────────────────────
    print("\nOverlapping patterns:")
    ac2 = AhoCorasick(["a", "ab", "bab", "bc", "bca", "c", "caa"])
    result2 = ac2.search("abccab")
    check("'a' at [0, 4]", result2.get("a") == [0, 4])
    check("'ab' at [0,4]", result2.get("ab") == [0, 4])
    check("'c' at [2, 3]", result2.get("c") == [2, 3])
    check("'bc' at [1]", result2.get("bc") == [1])
    check("'bca' not found", "bca" not in result2)

    # ── No matches ───────────────────────────────────────────────────────────
    print("\nNo matches:")
    ac3 = AhoCorasick(["xyz", "abc"])
    result3 = ac3.search("hello world")
    check("no matches empty dict", result3 == {})

    # ── Single pattern ───────────────────────────────────────────────────────
    print("\nSingle pattern:")
    ac4 = AhoCorasick(["test"])
    result4 = ac4.search("this is a test and another test")
    check("single pattern occurrences", result4["test"] == [10, 27])

    # ── Unique patterns ──────────────────────────────────────────────────────
    print("\nUnique patterns (first occurrence):")
    ac5 = AhoCorasick(["a", "b", "c"])
    result5 = ac5.search_unique_patterns("bac")
    check("first 'a' at 1", result5["a"] == 1)
    check("first 'b' at 0", result5["b"] == 0)
    check("first 'c' at 2", result5["c"] == 2)

    # ── Edge cases ───────────────────────────────────────────────────────────
    print("\nEdge cases:")
    ac6 = AhoCorasick(["", "a"])
    result6 = ac6.search("a")
    check("empty pattern", result6.get("a") == [0])

    # ── Summary ───────────────────────────────────────────────────────────────
    total = passed + failed
    print(f"\n{'='*50}")
    print(f"Results: {passed}/{total} passed, {failed}/{total} failed")
    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    _run_tests()
