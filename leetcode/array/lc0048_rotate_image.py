"""
LeetCode #48: Rotate Image
https://leetcode.com/problems/rotate-image/

You are given an n x n 2D matrix representing an image, rotate the image by 90
degrees (clockwise). You have to rotate the image in-place, which means you have to
modify the input 2D matrix directly. DO NOT allocate another 2D matrix.

Constraints:
- n == matrix.length == matrix[i].length
- 1 <= n <= 20
- -1000 <= matrix[i][j] <= 1000

Approach 1: Transpose + Reverse Rows
    Step 1: Transpose the matrix (swap matrix[i][j] with matrix[j][i]).
    Step 2: Reverse each row.
    O(n^2) time, O(1) space.

Approach 2: Layer-by-layer Rotation
    Rotate four elements at a time for each layer. O(n^2) time, O(1) space.
"""

from typing import List


def rotate_transpose_reverse(matrix: List[List[int]]) -> None:
    """Transpose + reverse rows: O(n^2) time, O(1) space."""
    n = len(matrix)

    # Step 1: Transpose (swap across diagonal)
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

    # Step 2: Reverse each row
    for i in range(n):
        matrix[i].reverse()


def rotate_layer(matrix: List[List[int]]) -> None:
    """Layer-by-layer rotation: O(n^2) time, O(1) space."""
    n = len(matrix)

    for layer in range(n // 2):
        first, last = layer, n - 1 - layer
        for i in range(first, last):
            offset = i - first
            # Save top
            top = matrix[first][i]
            # Left → Top
            matrix[first][i] = matrix[last - offset][first]
            # Bottom → Left
            matrix[last - offset][first] = matrix[last][last - offset]
            # Right → Bottom
            matrix[last][last - offset] = matrix[i][last]
            # Top (saved) → Right
            matrix[i][last] = top


# ── Default export ──
rotate = rotate_transpose_reverse


# ── Tests ──
if __name__ == "__main__":
    test_cases = [
        ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [[7, 4, 1], [8, 5, 2], [9, 6, 3]]),
        ([[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]],
         [[15, 13, 2, 5], [14, 3, 4, 1], [12, 6, 8, 9], [16, 7, 10, 11]]),
        ([[1]], [[1]]),
        ([[1, 2], [3, 4]], [[3, 1], [4, 2]]),
    ]

    all_pass = True
    for mat, expected in test_cases:
        mat_copy = [row[:] for row in mat]
        rotate_transpose_reverse(mat_copy)
        pass_flag = mat_copy == expected
        all_pass &= pass_flag
        status = "✓ PASS" if pass_flag else "✗ FAIL"
        print(f"{status} | input={mat} => {mat_copy} (expected {expected})")

    print("\nAll tests passed!" if all_pass else "\nSome tests FAILED!")
