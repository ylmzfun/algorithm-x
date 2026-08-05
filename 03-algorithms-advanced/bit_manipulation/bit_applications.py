"""
Bit manipulation applications.

Contains:
- Subset generation using bitmask
- Gray code generation
- Bit DP: Traveling Salesman Problem (TSP)
- Bit DP: Assignment problem (tasks to workers)
- Bitset for subset sum
"""

from typing import List, Optional, Tuple


# ======================================================================
# Subset generation
# ======================================================================

def generate_subsets(arr: List[int]) -> List[List[int]]:
    """
    Generate all subsets of a given list using bitmask enumeration.

    For an array of size n there are 2^n subsets.

    Args:
        arr: Input list of elements.

    Returns:
        List of all subsets.

    Time:  O(n * 2^n)
    Space: O(n * 2^n)

    Example:
        generate_subsets([1, 2]) → [[], [1], [2], [1, 2]]
    """
    n = len(arr)
    result: List[List[int]] = []

    for mask in range(1 << n):
        subset = [arr[i] for i in range(n) if (mask >> i) & 1]
        result.append(subset)

    return result


# ======================================================================
# Gray code
# ======================================================================

def gray_code(n: int) -> List[int]:
    """
    Generate the n-bit Gray code sequence (0 to 2^n - 1).

    In Gray code, consecutive numbers differ by exactly one bit.

    Formula: gray(i) = i ^ (i >> 1)

    Args:
        n: Number of bits.

    Returns:
        List of 2^n integers in Gray code order.

    Time:  O(2^n)
    Space: O(2^n)

    Example:
        gray_code(2) → [0, 1, 3, 2]
          i=0: 00 ⊕ 00 = 00 (0)
          i=1: 01 ⊕ 00 = 01 (1)
          i=2: 10 ⊕ 01 = 11 (3)
          i=3: 11 ⊕ 01 = 10 (2)
    """
    result = []
    for i in range(1 << n):
        result.append(i ^ (i >> 1))
    return result


# ======================================================================
# Bit DP: Traveling Salesman Problem (TSP)
# ======================================================================

def tsp_bit_dp(dist: List[List[int]]) -> Tuple[int, List[int]]:
    """
    Solve the Traveling Salesman Problem (TSP) using bit DP (Held-Karp).

    Finds the shortest Hamiltonian cycle starting and ending at city 0.

    dp[mask][i] = minimum cost to visit all cities in `mask` ending at city i.

    Args:
        dist: n × n distance matrix (dist[i][j] = distance from i to j).
              Can be asymmetric.

    Returns:
        (min_cost, tour) where tour is a list of city indices starting
        and ending at 0.

    Time:  O(n^2 * 2^n)
    Space: O(n * 2^n)
    """
    n = len(dist)
    if n == 0:
        return 0, []
    if n == 1:
        return 0, [0]

    INF = 10**18
    total_masks = 1 << n

    # dp[mask][i]: min cost to visit cities in mask, ending at i
    dp = [[INF] * n for _ in range(total_masks)]
    parent = [[-1] * n for _ in range(total_masks)]

    dp[1][0] = 0  # start at city 0, mask = {0}

    for mask in range(1, total_masks):
        for i in range(n):
            if not (mask >> i) & 1:
                continue
            if dp[mask][i] == INF:
                continue
            for j in range(n):
                if (mask >> j) & 1:
                    continue  # already visited
                new_mask = mask | (1 << j)
                nd = dp[mask][i] + dist[i][j]
                if nd < dp[new_mask][j]:
                    dp[new_mask][j] = nd
                    parent[new_mask][j] = i

    # Find the best return to city 0
    full_mask = (1 << n) - 1
    best = INF
    last = -1
    for i in range(n):
        nd = dp[full_mask][i] + dist[i][0]
        if nd < best:
            best = nd
            last = i

    # Reconstruct tour
    tour = [0]
    mask = full_mask
    cur = last
    while cur != 0:
        tour.append(cur)
        prev = parent[mask][cur]
        mask ^= (1 << cur)
        cur = prev
    tour.append(0)
    tour.reverse()

    return best, tour


# ======================================================================
# Bit DP: Assignment problem (assign tasks to workers)
# ======================================================================

def assign_tasks_bit_dp(cost: List[List[int]]) -> Tuple[int, List[int]]:
    """
    Solve the assignment problem: assign n tasks to n workers to minimize
    total cost, each worker gets exactly one task.

    Uses bit DP: dp[mask] = minimum cost to assign the first k tasks
    where k = popcount(mask) and mask indicates which workers are used.

    Args:
        cost: n × n cost matrix; cost[i][j] = cost for worker i to do task j.

    Returns:
        (min_total_cost, assignment) where assignment[i] = task assigned
        to worker i.

    Time:  O(n * 2^n)
    Space: O(2^n)
    """
    n = len(cost)
    if n == 0:
        return 0, []

    total_masks = 1 << n
    INF = 10**18
    dp = [INF] * total_masks
    choice = [-1] * total_masks  # which task was assigned in the last step

    dp[0] = 0

    for mask in range(total_masks):
        k = bin(mask).count("1")  # number of tasks assigned so far
        if k >= n:
            continue
        for j in range(n):  # j = worker index
            if (mask >> j) & 1:
                continue  # worker j already assigned
            new_mask = mask | (1 << j)
            nd = dp[mask] + cost[j][k]
            if nd < dp[new_mask]:
                dp[new_mask] = nd
                choice[new_mask] = j

    # Reconstruct assignment
    assignment = [-1] * n  # assignment[worker] = task
    mask = total_masks - 1
    task = n - 1
    while mask:
        j = choice[mask]
        assignment[j] = task
        mask ^= (1 << j)
        task -= 1

    return dp[-1], assignment


# ======================================================================
# Bitset for subset sum
# ======================================================================

def subset_sum_bitset(arr: List[int], target: int) -> bool:
    """
    Determine whether a subset of arr sums to the given target using
    a bitset (bit-level DP).

    Bitset approach: maintain a bitmask where bit i is set if sum i is
    achievable.  For each element x, shift the bitset left by x and OR
    with the original.

    Args:
        arr: List of positive integers.
        target: Target sum.

    Returns:
        True if a subset sums to target, False otherwise.

    Time:  O(n * target / wordsize) ≈ O(n * target / 64)
    Space: O(target / 8) bytes

    Example:
        subset_sum_bitset([3, 34, 4, 12, 5, 2], 9) → True  (4 + 5)
    """
    if target < 0:
        return False

    # Use Python's arbitrary-precision integers as an infinite bitset
    bitset = 1  # bit 0 = sum 0 is achievable

    for x in arr:
        bitset |= bitset << x

    return (bitset >> target) & 1 == 1


# ======================================================================
# Tests
# ======================================================================

if __name__ == "__main__":
    import sys

    all_pass = True

    # --- Subset generation ---
    subsets = generate_subsets([1, 2])
    expected = [[], [1], [2], [1, 2]]
    if sorted([sorted(s) for s in subsets]) != sorted([sorted(s) for s in expected]):
        print(f"FAIL subsets: {sorted(subsets)}")
        all_pass = False

    # --- Gray code ---
    gc = gray_code(2)
    if gc != [0, 1, 3, 2]:
        print(f"FAIL gray_code(2): {gc}")
        all_pass = False

    gc3 = gray_code(3)
    # Check: consecutive elements differ by exactly 1 bit
    for i in range(len(gc3) - 1):
        diff = gc3[i] ^ gc3[i + 1]
        if diff & (diff - 1) != 0:  # more than 1 bit difference
            print(f"FAIL gray_code(3) adj: {gc3[i]} vs {gc3[i+1]}")
            all_pass = False

    # --- TSP ---
    dist = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0],
    ]
    min_cost, tour = tsp_bit_dp(dist)
    # Optimal: 0→1→3→2→0: 10+25+30+15=80
    if min_cost != 80:
        print(f"FAIL TSP cost: {min_cost}")
        all_pass = False
    if tour[0] != 0 or tour[-1] != 0:
        print(f"FAIL TSP tour endpoints: {tour}")
        all_pass = False

    # --- Assignment ---
    cost_matrix = [
        [9, 2, 7, 8],
        [6, 4, 3, 7],
        [5, 8, 1, 8],
        [7, 6, 9, 4],
    ]
    total, assignment = assign_tasks_bit_dp(cost_matrix)
    # Optimal: w0→t1(2), w1→t0(6), w2→t2(1), w3→t3(4) = 13
    if total != 13:
        print(f"FAIL assignment cost: {total}")
        all_pass = False
    if sorted(assignment) != [0, 1, 2, 3]:
        print(f"FAIL assignment perms: {assignment}")
        all_pass = False

    # --- Subset sum bitset ---
    if not subset_sum_bitset([3, 34, 4, 12, 5, 2], 9):
        print("FAIL subset_sum 9")
        all_pass = False
    if subset_sum_bitset([3, 34, 4, 12, 5, 2], 13):
        print("FAIL subset_sum 13 (should be false)")
        all_pass = False
    if not subset_sum_bitset([1, 2, 3], 6):
        print("FAIL subset_sum 6")
        all_pass = False
    if subset_sum_bitset([1, 2, 3], 7):
        print("FAIL subset_sum 7")
        all_pass = False

    if all_pass:
        print("All bit applications tests PASSED")
    sys.exit(0 if all_pass else 1)
