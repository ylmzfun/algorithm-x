#pragma once

#include <cmath>
#include <cstddef>
#include <vector>

namespace algorithm_x {
namespace math {

// 行列式 — 高斯消元法 O(n³)。
// 返回 double，奇异矩阵返回 0。
inline double determinant(std::vector<std::vector<double>> a) {
    std::size_t n = a.size();
    double det = 1.0;
    const double eps = 1e-9;

    for (std::size_t i = 0; i < n; ++i) {
        // 选主元
        std::size_t pivot = i;
        for (std::size_t j = i + 1; j < n; ++j) {
            if (std::abs(a[j][i]) > std::abs(a[pivot][i])) {
                pivot = j;
            }
        }
        if (std::abs(a[pivot][i]) < eps) return 0.0;

        if (pivot != i) {
            std::swap(a[i], a[pivot]);
            det = -det;
        }

        det *= a[i][i];
        for (std::size_t j = i + 1; j < n; ++j) {
            double factor = a[j][i] / a[i][i];
            for (std::size_t k = i; k < n; ++k) {
                a[j][k] -= factor * a[i][k];
            }
        }
    }
    return det;
}

}  // namespace math
}  // namespace algorithm_x
