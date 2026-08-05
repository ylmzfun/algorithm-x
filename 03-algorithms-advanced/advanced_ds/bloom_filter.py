"""
Bloom Filter — a space-efficient probabilistic data structure.

Supports:
- add: Insert an element.
- contains: Test set membership (no false negatives, configurable false positive rate).

Uses multiple hash functions via the double-hashing technique to simulate
k independent hash functions from two base hashes.
"""

import math
import hashlib
from typing import Any


class BloomFilter:
    """
    Bloom Filter with configurable false positive rate.

    Given an expected number of elements `n` and a desired false positive
    rate `p`, the optimal bit-array size `m` and number of hash functions
    `k` are:

        m = -n * ln(p) / (ln(2))^2
        k = (m / n) * ln(2)
    """

    def __init__(self, expected_items: int, false_positive_rate: float) -> None:
        """
        Initialize a Bloom filter.

        Args:
            expected_items: Expected number of elements to insert.
            false_positive_rate: Desired false positive probability, e.g. 0.01.

        Time: O(m) for bit array allocation
        """
        if expected_items <= 0:
            raise ValueError("expected_items must be positive")
        if not (0 < false_positive_rate < 1):
            raise ValueError("false_positive_rate must be in (0, 1)")

        self.n = expected_items
        self.p = false_positive_rate

        # Optimal size: m = -n * ln(p) / (ln(2))^2
        self.m = max(1, int(-expected_items * math.log(false_positive_rate) / (math.log(2) ** 2)))
        # Optimal number of hash functions: k = (m / n) * ln(2)
        self.k = max(1, int((self.m / expected_items) * math.log(2)))

        # Bit array (using a bytearray, 8 bits per byte)
        byte_len = (self.m + 7) // 8
        self.bits = bytearray(byte_len)

        self._item_count = 0

    # ------------------------------------------------------------------
    # Hash helpers (double-hashing technique)
    # ------------------------------------------------------------------

    def _get_hashes(self, item: Any) -> tuple:
        """
        Compute two base hashes of an item using SHA-256.

        Returns (h1, h2) used to simulate k hash functions via:
            hash_i(x) = (h1 + i * h2) % m

        Args:
            item: The item to hash (converted to bytes via str representation).

        Returns:
            (h1, h2) as integers.
        """
        data = str(item).encode("utf-8")
        digest = hashlib.sha256(data).digest()
        # Use two halves of the SHA-256 digest as two 64-bit integers
        h1 = int.from_bytes(digest[:16], "big")
        h2 = int.from_bytes(digest[16:], "big")
        return h1, h2

    def _bit_positions(self, item: Any) -> list:
        """
        Compute the k bit positions for the given item.

        Uses the double-hashing technique:  pos_i = (h1 + i * h2) % m

        Args:
            item: The item to hash.

        Returns:
            List of k bit positions.
        """
        h1, h2 = self._get_hashes(item)
        positions = []
        for i in range(self.k):
            pos = (h1 + i * h2) % self.m
            positions.append(pos)
        return positions

    # ------------------------------------------------------------------
    # Add
    # ------------------------------------------------------------------

    def add(self, item: Any) -> None:
        """
        Insert an item into the Bloom filter.

        Args:
            item: The item to add.

        Time: O(k)
        """
        for pos in self._bit_positions(item):
            byte_idx = pos // 8
            bit_idx = pos % 8
            self.bits[byte_idx] |= (1 << bit_idx)
        self._item_count += 1

    # ------------------------------------------------------------------
    # Contains
    # ------------------------------------------------------------------

    def contains(self, item: Any) -> bool:
        """
        Test whether an item is possibly in the set.

        There are NO false negatives — if the item was added, this always
        returns True.  There may be false positives with probability p.

        Args:
            item: The item to test.

        Returns:
            True if the item might be present, False if definitely absent.

        Time: O(k)
        """
        for pos in self._bit_positions(item):
            byte_idx = pos // 8
            bit_idx = pos % 8
            if not (self.bits[byte_idx] & (1 << bit_idx)):
                return False
        return True

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def item_count(self) -> int:
        """Number of items inserted so far."""
        return self._item_count

    @property
    def bit_size(self) -> int:
        """Size of the bit array."""
        return self.m

    @property
    def hash_count(self) -> int:
        """Number of hash functions."""
        return self.k

    def __contains__(self, item: Any) -> bool:
        return self.contains(item)

    def __len__(self) -> int:
        return self._item_count


# ======================================================================
# Tests
# ======================================================================

if __name__ == "__main__":
    import sys

    all_pass = True

    # Create Bloom filter expecting 1000 items with 1% false positive rate
    bf = BloomFilter(expected_items=1000, false_positive_rate=0.01)

    if bf.bit_size == 0 or bf.hash_count == 0:
        print("FAIL: invalid dimensions")
        all_pass = False

    # Add some items
    for i in range(100):
        bf.add(f"item_{i}")

    # Check contains for added items (no false negatives)
    for i in range(100):
        if not bf.contains(f"item_{i}"):
            print(f"FAIL: false negative for item_{i}")
            all_pass = False
            break

    # Check contains for non-added items (may have false positives, but
    # should have mostly correct negatives)
    false_positives = 0
    for i in range(100, 1100):
        if bf.contains(f"item_{i}"):
            false_positives += 1

    # With 100 items and m optimized for 1000, the actual FPR should be very low
    # We just check that it's not absurdly high (< 50%)
    fpr = false_positives / 1000
    if fpr > 0.3:
        print(f"FAIL: false positive rate too high: {fpr:.3f}")
        all_pass = False

    # --- Edge cases ---
    # Very small Bloom filter
    bf2 = BloomFilter(expected_items=10, false_positive_rate=0.1)
    bf2.add("test")
    if not bf2.contains("test"):
        print("FAIL: small bloom filter")
        all_pass = False

    # Contains returns False for empty filter
    bf3 = BloomFilter(expected_items=5, false_positive_rate=0.01)
    if bf3.contains("anything"):
        print("FAIL: empty filter should not contain anything")
        all_pass = False

    if all_pass:
        print("All Bloom Filter tests PASSED")
    sys.exit(0 if all_pass else 1)
