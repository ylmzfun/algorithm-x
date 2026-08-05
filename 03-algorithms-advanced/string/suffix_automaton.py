"""
Suffix Automaton (SAM) — a compact representation of all substrings of a string.

A Suffix Automaton for a string S of length n has:
- At most 2n - 1 states
- At most 3n - 4 transitions
- Can be built in O(n) time

Applications:
- Check if a string is a substring
- Count distinct substrings
- Find longest common substring of two strings
- Find the lexicographically k-th substring
"""

from typing import Dict, List, Optional


class SAMState:
    """A single state in the Suffix Automaton."""

    __slots__ = ("length", "link", "next")

    def __init__(self) -> None:
        self.length = 0          # Longest length of substring ending here
        self.link = -1           # Suffix link (to the longest suffix in another class)
        self.next: Dict[str, int] = {}  # Transitions: char → state index


class SuffixAutomaton:
    """
    Suffix Automaton (SAM) for a string.

    Builds the automaton online (character by character) in O(n) time.

    Usage:
        sam = SuffixAutomaton("abcabc")
        sam.contains("bca")       # True
        sam.count_distinct_substrings()  # 15
    """

    def __init__(self, s: str = "") -> None:
        """
        Build the suffix automaton for the given string.

        Args:
            s: The string to build the SAM for.

        Time: O(n) where n = len(s)
        """
        self.states: List[SAMState] = []
        self.s = s

        if s:
            self._build(s)

    def _build(self, s: str) -> None:
        """Build the automaton character by character."""
        # Create initial state
        self.states.append(SAMState())
        last = 0  # index of the state corresponding to the whole string so far

        for ch in s:
            cur = len(self.states)
            self.states.append(SAMState())
            self.states[cur].length = self.states[last].length + 1

            # Add transitions from states reachable via suffix links
            p = last
            while p != -1 and ch not in self.states[p].next:
                self.states[p].next[ch] = cur
                p = self.states[p].link

            if p == -1:
                self.states[cur].link = 0
            else:
                q = self.states[p].next[ch]
                if self.states[p].length + 1 == self.states[q].length:
                    self.states[cur].link = q
                else:
                    # Clone state q
                    clone = len(self.states)
                    self.states.append(SAMState())
                    self.states[clone].length = self.states[p].length + 1
                    self.states[clone].next = self.states[q].next.copy()
                    self.states[clone].link = self.states[q].link

                    while p != -1 and self.states[p].next.get(ch) == q:
                        self.states[p].next[ch] = clone
                        p = self.states[p].link

                    self.states[q].link = clone
                    self.states[cur].link = clone

            last = cur

    def contains(self, pattern: str) -> bool:
        """
        Check if pattern is a substring of the original string.

        Args:
            pattern: The string to check.

        Returns:
            True if pattern is a substring.

        Time: O(len(pattern))
        """
        cur = 0
        for ch in pattern:
            if ch not in self.states[cur].next:
                return False
            cur = self.states[cur].next[ch]
        return True

    def count_distinct_substrings(self) -> int:
        """
        Count the number of distinct substrings in the original string.

        For each state, it contributes (length - link.length) distinct
        substrings that end at this state for the first time.

        Returns:
            Number of distinct substrings.

        Time: O(number of states)
        """
        total = 0
        for state in self.states:
            if state.link != -1:
                total += state.length - self.states[state.link].length
        return total

    def longest_common_substring(self, t: str) -> str:
        """
        Find the longest common substring between the original string and t.

        Args:
            t: The other string.

        Returns:
            The longest common substring, or empty string if none.

        Time: O(len(t))
        """
        v = 0      # current state
        l = 0      # current match length
        best = 0
        best_pos = 0

        for i, ch in enumerate(t):
            while v != 0 and ch not in self.states[v].next:
                v = self.states[v].link
                l = self.states[v].length

            if ch in self.states[v].next:
                v = self.states[v].next[ch]
                l += 1

            if l > best:
                best = l
                best_pos = i - l + 1

        return t[best_pos : best_pos + best]

    def kth_substring(self, k: int) -> Optional[str]:
        """
        Find the lexicographically k-th distinct substring (1-indexed).

        Uses DP on the DAG of the SAM to count paths.

        Args:
            k: 1-based index of the desired substring.

        Returns:
            The k-th distinct substring, or None if k is out of range.

        Time: O(number of states * alphabet size) for DP + O(answer length)
        """
        # Topological order (states are already in increasing order of length)
        n_states = len(self.states)

        # dp[i] = number of distinct substrings starting from state i
        dp = [0] * n_states

        # Process states in reverse order of length (which is a topological order)
        order = sorted(range(n_states), key=lambda i: self.states[i].length, reverse=True)

        for v in order:
            dp[v] = 1  # empty path from this state
            for _, nxt in self.states[v].next.items():
                dp[v] += dp[nxt]

        if k <= 0 or k > dp[0] - 1:
            return None

        # Walk the DAG to find the k-th substring
        result: List[str] = []
        v = 0
        k -= 1  # exclude the empty substring

        while k > 0:
            for ch in sorted(self.states[v].next.keys()):
                nxt = self.states[v].next[ch]
                if k <= dp[nxt]:
                    result.append(ch)
                    v = nxt
                    k -= 1  # for the character we just added
                    break
                else:
                    k -= dp[nxt]

        return "".join(result)

    def all_occurrences(self, pattern: str) -> List[int]:
        """
        Find all starting positions of pattern in the original string.

        Uses endpos sets: after locating the state corresponding to the
        pattern, we collect all end positions stored in its subtree.

        Args:
            pattern: The pattern to find.

        Returns:
            List of starting indices (0-based).

        Time:  O(len(pattern) + number of occurrences)
        Space: O(number of states)
        """
        # First, locate the state for the pattern
        v = 0
        for ch in pattern:
            if ch not in self.states[v].next:
                return []
            v = self.states[v].next[ch]

        # We need endpos information.  During construction we can track
        # which states are terminal (end at some position).  Here we do a
        # simplified version: compute for each state a list of end positions
        # by propagating from terminal states via suffix links in reverse.

        # Mark terminal states (the states that end at some prefix)
        n_states = len(self.states)
        is_terminal = [False] * n_states
        # The state 'last' after processing each prefix is terminal
        end_positions: List[List[int]] = [[] for _ in range(n_states)]

        last = 0
        for i, ch in enumerate(self.s):
            last = self.states[last].next[ch]
            is_terminal[last] = True
            end_positions[last].append(i)

        # Propagate end positions via suffix links (in reverse length order)
        order = sorted(range(n_states), key=lambda i: self.states[i].length, reverse=True)

        for state_idx in order:
            link = self.states[state_idx].link
            if link != -1:
                end_positions[link].extend(end_positions[state_idx])

        # Convert end positions to start positions
        m = len(pattern)
        return sorted(set(pos - m + 1 for pos in end_positions[v]))


# ======================================================================
# Tests
# ======================================================================

if __name__ == "__main__":
    import sys

    all_pass = True

    # --- Build and Contains ---
    sam = SuffixAutomaton("abcabc")
    if not sam.contains("bca"):
        print("FAIL contains 'bca'")
        all_pass = False
    if not sam.contains("abc"):
        print("FAIL contains 'abc'")
        all_pass = False
    if sam.contains("abd"):
        print("FAIL contains 'abd' (should be False)")
        all_pass = False
    if not sam.contains(""):
        print("FAIL contains empty string")
        all_pass = False
    if not sam.contains("c"):
        print("FAIL contains 'c'")
        all_pass = False

    # --- Count distinct substrings ---
    # "abcabc": distinct substrings:
    # a,b,c,ab,bc,ca,abc,bca,cab,abca,bcab,abcab,bcabc,abcabc → 15
    cnt = sam.count_distinct_substrings()
    if cnt != 15:
        print(f"FAIL distinct substrings 'abcabc': expected 15, got {cnt}")
        all_pass = False

    sam2 = SuffixAutomaton("aaaa")
    cnt2 = sam2.count_distinct_substrings()
    if cnt2 != 4:  # a, aa, aaa, aaaa
        print(f"FAIL distinct substrings 'aaaa': expected 4, got {cnt2}")
        all_pass = False

    # --- Longest common substring ---
    sam3 = SuffixAutomaton("abcdef")
    lcs = sam3.longest_common_substring("xbcdyz")
    if lcs != "bcd":
        print(f"FAIL longest common substring: '{lcs}'")
        all_pass = False

    lcs2 = sam3.longest_common_substring("xyz")
    if lcs2 != "":
        print(f"FAIL longest common substring empty: '{lcs2}'")
        all_pass = False

    # --- All occurrences ---
    sam4 = SuffixAutomaton("ababa")
    occ = sam4.all_occurrences("aba")
    if sorted(occ) != [0, 2]:
        print(f"FAIL all_occurrences 'aba' in 'ababa': {occ}")
        all_pass = False

    occ2 = sam4.all_occurrences("ba")
    if sorted(occ2) != [1, 3]:
        print(f"FAIL all_occurrences 'ba': {occ2}")
        all_pass = False

    occ3 = sam4.all_occurrences("xyz")
    if occ3 != []:
        print(f"FAIL all_occurrences 'xyz': {occ3}")
        all_pass = False

    if all_pass:
        print("All Suffix Automaton tests PASSED")
    sys.exit(0 if all_pass else 1)
