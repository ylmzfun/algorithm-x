#pragma once

#include <cmath>
#include <cstddef>
#include <cstdint>
#include <vector>

namespace algorithm_x {
namespace math {

// ---- Matrix Multiplication ----

// 矩阵乘法 — C = A × B, A 为 n×m，B 为 m×p。
// 返回 n×p 矩阵。
template <typename T>
std::vector<std::vector<T>> matrix_mul(
    const std::vector<std::vector<T>>& A,
    const std::vector<std::vector<T>>& B) {
    std::size_t n = A.size(), m = A[0].size(), p = B[0].size();
    std::vector<std::vector<T>> C(n, std::vector<T>(p, T{}));
    for (std::size_t i = 0; i < n; ++i)
        for (std::size_t k = 0; k < m; ++k)
            if (A[i][k] != T{})
                for (std::size_t j = 0; j < p; ++j)
                    C[i][j] += A[i][k] * B[k][j];
    return C;
}

// 矩阵快速幂 — A^n，A 为方阵。
template <typename T>
std::vector<std::vector<T>> matrix_pow(std::vector<std::vector<T>> A,
                                        int64_t n) {
    std::size_t sz = A.size();
    std::vector<std::vector<T>> R(sz, std::vector<T>(sz, T{}));
    for (std::size_t i = 0; i < sz; ++i) R[i][i] = T{1};

    while (n) {
        if (n & 1) R = matrix_mul(R, A);
        A = matrix_mul(A, A);
        n >>= 1;
    }
    return R;
}

// ---- Fibonacci ----

// 斐波那契数列第 n 项（矩阵快速幂 O(log n)）。
// fib(0)=0, fib(1)=1。
template <typename T>
T fibonacci(int64_t n) {
    if (n == 0) return T{0};
    std::vector<std::vector<T>> F = {{T{1}, T{1}}, {T{1}, T{0}}};
    auto R = matrix_pow(F, n - 1);
    return R[0][0];
}

// ---- Gaussian Elimination ----

// 高斯消元 — 解 Ax = b，返回解的向量。无解 / 无穷解返回空。
// A 为 n×n 方阵，b 为 n×1，使用 double。
inline std::vector<double> gaussian_elimination(
    std::vector<std::vector<double>> A, std::vector<double> b) {
    std::size_t n = A.size();
    const double eps = 1e-9;

    for (std::size_t col = 0; col < n; ++col) {
        // 选主元
        std::size_t pivot = col;
        for (std::size_t row = col + 1; row < n; ++row)
            if (std::abs(A[row][col]) > std::abs(A[pivot][col]))
                pivot = row;
        if (std::abs(A[pivot][col]) < eps) return {};
        std::swap(A[col], A[pivot]);
        std::swap(b[col], b[pivot]);

        // 消元
        double div = A[col][col];
        for (std::size_t j = col; j < n; ++j) A[col][j] /= div;
        b[col] /= div;

        for (std::size_t row = 0; row < n; ++row) {
            if (row == col) continue;
            double factor = A[row][col];
            for (std::size_t j = col; j < n; ++j) A[row][j] -= factor * A[col][j];
            b[row] -= factor * b[col];
        }
    }
    return b;
}

}  // namespace math
}  // namespace algorithm_x
