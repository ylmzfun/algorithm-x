"""
Classic Greedy Algorithms
==========================

Greedy algorithms build a solution piece by piece, always choosing the
next piece that offers the most immediate benefit.

Functions:
- activity_selection     : Maximum number of non-overlapping activities.
- fractional_knapsack    : Maximum value with fractional item selection.
- huffman_coding         : Build optimal prefix code (encoding/decoding).
- job_sequencing         : Maximise profit with unit-time jobs and deadlines.
- coin_change_greedy     : Min coins for canonical coin systems.
"""

import heapq
from typing import List, Tuple, Dict, Optional


# ---------------------------------------------------------------------------
# Activity Selection
# ---------------------------------------------------------------------------

def activity_selection(activities: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    Select the maximum number of non-overlapping activities.

    The classic greedy choice: always pick the activity that finishes
    earliest and does not overlap with the last selected activity.

    Parameters
    ----------
    activities : List[Tuple[int, int]]
        List of (start_time, end_time) pairs.

    Returns
    -------
    List[Tuple[int, int]]
        Selected activities sorted by end time.

    Time  : O(n log n) — dominated by sorting.
    Space : O(n) for output.
    """
    if not activities:
        return []

    # Sort by finish time
    sorted_acts = sorted(activities, key=lambda x: x[1])
    selected = [sorted_acts[0]]
    last_end = sorted_acts[0][1]

    for start, end in sorted_acts[1:]:
        if start >= last_end:
            selected.append((start, end))
            last_end = end
    return selected


# ---------------------------------------------------------------------------
# Fractional Knapsack
# ---------------------------------------------------------------------------

def fractional_knapsack(
    items: List[Tuple[int, int]], capacity: int
) -> Tuple[float, List[float]]:
    """
    Maximise the total value by taking fractional amounts of items.

    Items can be broken; the greedy choice is to take as much as possible
    of the item with the highest value-to-weight ratio.

    Parameters
    ----------
    items : List[Tuple[int, int]]
        Each (value, weight).
    capacity : int
        Knapsack capacity.

    Returns
    -------
    Tuple[float, List[float]]
        (total_value, fractions_taken), where fractions_taken[i] is the
        fraction (0-1) of item i taken.

    Time  : O(n log n)
    Space : O(n)
    """
    n = len(items)
    # (ratio, value, weight, original_index)
    indexed = [(v / w, v, w, i) for i, (v, w) in enumerate(items)]
    indexed.sort(reverse=True, key=lambda x: x[0])

    total_value = 0.0
    fractions = [0.0] * n
    remaining = capacity

    for ratio, val, wt, idx in indexed:
        if remaining <= 0:
            break
        take = min(wt, remaining)
        fractions[idx] = take / wt
        total_value += take * ratio
        remaining -= take

    return total_value, fractions


# ---------------------------------------------------------------------------
# Huffman Coding
# ---------------------------------------------------------------------------

class HuffmanNode:
    """Node in the Huffman tree."""
    def __init__(self, char: Optional[str], freq: int,
                 left: Optional["HuffmanNode"] = None,
                 right: Optional["HuffmanNode"] = None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other: "HuffmanNode") -> bool:
        return self.freq < other.freq


def _build_codes(node: HuffmanNode, prefix: str, codebook: Dict[str, str]) -> None:
    if node.char is not None:
        codebook[node.char] = prefix if prefix else "0"  # single-char case
    else:
        if node.left:
            _build_codes(node.left, prefix + "0", codebook)
        if node.right:
            _build_codes(node.right, prefix + "1", codebook)


def huffman_coding(text: str) -> Tuple[Dict[str, str], HuffmanNode, str, str]:
    """
    Build a Huffman tree, generate prefix codes, encode and decode.

    Parameters
    ----------
    text : str
        Input text to compress.

    Returns
    -------
    Tuple[Dict[str, str], HuffmanNode, str, str]
        (codebook, tree_root, encoded_string, decoded_string).
        decoded_string should equal the original text.

    Time  : O(n + k log k) where k = number of distinct characters.
    Space : O(k)
    """
    from collections import Counter
    freq = Counter(text)

    # Build priority queue of leaf nodes
    heap: List[HuffmanNode] = []
    for ch, f in freq.items():
        heapq.heappush(heap, HuffmanNode(ch, f))

    if not heap:
        return {}, HuffmanNode(None, 0), "", ""

    # Handle single character
    if len(heap) == 1:
        node = heap[0]
        codebook = {node.char: "0"}
        encoded = "0" * len(text)
        return codebook, node, encoded, text

    # Build Huffman tree
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(None, left.freq + right.freq, left, right)
        heapq.heappush(heap, merged)

    root = heap[0]
    codebook: Dict[str, str] = {}
    _build_codes(root, "", codebook)

    # Encode
    encoded = "".join(codebook[ch] for ch in text)

    # Decode
    decoded = ""
    cur = root
    for bit in encoded:
        cur = cur.left if bit == "0" else cur.right  # type: ignore[assignment]
        if cur and cur.char is not None:
            decoded += cur.char
            cur = root

    return codebook, root, encoded, decoded


# ---------------------------------------------------------------------------
# Job Sequencing with Deadlines
# ---------------------------------------------------------------------------

def job_sequencing(
    jobs: List[Tuple[int, int, int]]
) -> Tuple[int, List[int]]:
    """
    Schedule jobs to maximise profit, where each job takes 1 unit of time
    and has a deadline.

    Greedy approach: sort by profit descending, then schedule each job at
    the latest possible time slot before its deadline.

    Parameters
    ----------
    jobs : List[Tuple[int, int, int]]
        List of (job_id, deadline, profit).  Deadline is the last time slot
        (1-indexed) the job can be scheduled.

    Returns
    -------
    Tuple[int, List[int]]
        (total_profit, sequence_of_job_ids).

    Time  : O(n²) with simple implementation; O(n log n) with Union-Find.
    Space : O(max_deadline)
    """
    if not jobs:
        return 0, []

    # Sort by profit descending
    sorted_jobs = sorted(jobs, key=lambda x: x[2], reverse=True)
    max_deadline = max(d for _, d, _ in sorted_jobs)

    # slot[i] = job_id assigned to time slot i (0-indexed), -1 if free
    slot: List[int] = [-1] * max_deadline
    total_profit = 0
    sequence: List[int] = []

    for job_id, deadline, profit in sorted_jobs:
        # Find latest free slot from deadline-1 down to 0
        for t in range(min(deadline, max_deadline) - 1, -1, -1):
            if slot[t] == -1:
                slot[t] = job_id
                total_profit += profit
                break

    # Collect scheduled jobs in time order
    for job_id in slot:
        if job_id != -1:
            sequence.append(job_id)

    return total_profit, sequence


# ---------------------------------------------------------------------------
# Coin Change (Greedy — for canonical coin systems)
# ---------------------------------------------------------------------------

def coin_change_greedy(coins: List[int], amount: int) -> Optional[List[int]]:
    """
    Minimum number of coins to make ``amount`` using a greedy approach.

    **Only guaranteed to work for canonical coin systems** (e.g., US
    currency: 1, 5, 10, 25).  For arbitrary coin systems, use DP.

    Parameters
    ----------
    coins : List[int]
        Coin denominations (must be sorted descending for greedy).
    amount : int
        Target amount.

    Returns
    -------
    Optional[List[int]]
        List of coins used, or None if impossible.

    Time  : O(k) where k = number of denominations.
    Space : O(amount / min_coin).
    """
    if amount == 0:
        return []
    coins_sorted = sorted(coins, reverse=True)
    result: List[int] = []
    remaining = amount
    for coin in coins_sorted:
        while remaining >= coin:
            remaining -= coin
            result.append(coin)
    return result if remaining == 0 else None


# ===========================================================================
# Tests
# ===========================================================================

if __name__ == "__main__":
    print("=== Greedy Algorithms Tests ===\n")

    # activity_selection
    acts = [(1, 3), (2, 5), (3, 9), (6, 8), (5, 7), (8, 9)]
    sel = activity_selection(acts)
    assert len(sel) == 3 and sel[0] == (1, 3)  # maximum is 3: (1,3),(5,7),(8,9) or (1,3),(6,8),(8,9)
    assert activity_selection([]) == []
    print("  PASS activity_selection")

    # fractional_knapsack
    items = [(60, 10), (100, 20), (120, 30)]  # (value, weight)
    val, fracs = fractional_knapsack(items, 50)
    assert abs(val - 240.0) < 1e-9, f"Expected 240, got {val}"
    print("  PASS fractional_knapsack")

    # huffman_coding
    text = "aabacccddddee"
    codebook, tree, encoded, decoded = huffman_coding(text)
    assert decoded == text, f"Decoded '{decoded}' != '{text}'"
    # Single char
    _, _, enc2, dec2 = huffman_coding("aaaa")
    assert dec2 == "aaaa"
    # Empty
    _, _, enc3, dec3 = huffman_coding("")
    assert enc3 == "" and dec3 == ""
    print("  PASS huffman_coding")

    # job_sequencing
    jobs = [
        ("A", 2, 100),
        ("B", 1, 19),
        ("C", 2, 27),
        ("D", 1, 25),
        ("E", 3, 15),
    ]
    profit, seq = job_sequencing(jobs)
    assert profit == 142, f"Expected profit 142, got {profit}"
    print("  PASS job_sequencing")

    # coin_change_greedy
    us_coins = [1, 5, 10, 25]
    res = coin_change_greedy(us_coins, 63)
    assert res is not None and sum(res) == 63
    # Should use minimal coins: 25+25+10+1+1+1 = 6 coins
    assert len(res) == 6
    print("  PASS coin_change_greedy")

    print("\nAll greedy algorithm tests completed!")
