#pragma once

#include <cmath>
#include <complex>
#include <cstddef>
#include <vector>

namespace algorithm_x {
namespace math {

using cd = std::complex<double>;
const double PI = std::acos(-1.0);

// Cooley-Tukey FFT
inline void fft(std::vector<cd>& a, bool invert) {
    int n = static_cast<int>(a.size());
    for (int i = 1, j = 0; i < n; ++i) {
        int bit = n >> 1;
        for (; j & bit; bit >>= 1) j ^= bit;
        j ^= bit;
        if (i < j) std::swap(a[i], a[j]);
    }
    for (int len = 2; len <= n; len <<= 1) {
        double ang = 2.0 * PI / static_cast<double>(len) * (invert ? -1.0 : 1.0);
        cd wlen(std::cos(ang), std::sin(ang));
        for (int i = 0; i < n; i += len) {
            cd w(1.0);
            for (int j = 0; j < len / 2; ++j) {
                cd u = a[i + j];
                cd v = a[i + j + len / 2] * w;
                a[i + j] = u + v;
                a[i + j + len / 2] = u - v;
                w *= wlen;
            }
        }
    }
    if (invert) {
        for (auto& x : a) x /= static_cast<double>(n);
    }
}

// 多项式乘法
inline std::vector<int> fft_multiply(const std::vector<int>& a,
                                      const std::vector<int>& b) {
    int n = 1;
    while (n < static_cast<int>(a.size() + b.size())) n <<= 1;
    std::vector<cd> fa(a.begin(), a.end()), fb(b.begin(), b.end());
    fa.resize(n);
    fb.resize(n);
    fft(fa, false);
    fft(fb, false);
    for (int i = 0; i < n; ++i) fa[i] *= fb[i];
    fft(fa, true);
    std::vector<int> result(static_cast<std::size_t>(n));
    for (int i = 0; i < n; ++i) {
        result[static_cast<std::size_t>(i)] =
            static_cast<int>(std::round(fa[static_cast<std::size_t>(i)].real()));
    }
    // 去掉尾部零
    while (!result.empty() && result.back() == 0) result.pop_back();
    return result;
}

}  // namespace math
}  // namespace algorithm_x
