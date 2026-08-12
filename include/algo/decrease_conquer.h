#pragma once

#include <cstddef>
#include <utility>
#include <vector>

namespace algorithm_x {
namespace algo {

// quickselect_kth — 快速选择：返回 nums 中第 k 小（0 基）的值，期望 O(n)。
// 减治思想：与快速排序的划分一样，每次用 pivot 把数组分成左右两部分，
// 但只进入包含第 k 小元素的那一侧，另一侧直接丢弃；
// 于是每轮问题规模按几何级数衰减，期望复杂度 O(n)（区别于快速排序要处理两侧）。
// 取第一个元素为 pivot（Lomuto 划分）。k 越界（k >= n）返回 -1。
inline int quickselect_kth(std::vector<int> nums, std::size_t k) {
    const std::size_t n = nums.size();
    if (k >= n) {
        return -1;  // k 越界（0 基，k >= n 不合法）
    }
    std::size_t lo = 0;
    std::size_t hi = n;  // 处理区间 [lo, hi)
    while (lo < hi) {
        const int pivot = nums[lo];
        std::size_t i = lo;
        for (std::size_t j = lo + 1; j < hi; ++j) {
            if (nums[j] < pivot) {
                ++i;
                std::swap(nums[i], nums[j]);
            }
        }
        std::swap(nums[lo], nums[i]);
        if (i == k) {
            return nums[i];
        }
        if (i > k) {
            hi = i;  // 目标在左侧 [lo, i)
        } else {
            lo = i + 1;  // 目标在右侧 (i, hi)
        }
    }
    return -1;  // 不可达
}

// josephus — 约瑟夫问题：n 个人围成一圈（编号 0..n-1），从 0 开始报数，
// 报到 k 的人出列，问最后幸存者的编号（0 基）。
// 减治思想：第一轮报数后第 k-1 号（0 基）出列，剩下 n-1 人从 k 号重新编号，
// 构成一个规模为 n-1 的同构子问题。记 j(m) 为规模 m 时的幸存者编号，则有
//   j(1) = 0，j(n) = (j(n-1) + k) % n
// 从 1 到 n 递推即可把原问题逐级"减去"一个人，复杂度 O(n)。
// n 必须 >= 1，否则返回 -1 表示非法输入。
inline int josephus(int n, int k) {
    if (n <= 0) {
        return -1;
    }
    int survivor = 0;
    for (int i = 2; i <= n; ++i) {
        survivor = static_cast<int>((static_cast<long long>(survivor) + k) % i);
    }
    return survivor;
}

}  // namespace algo
}  // namespace algorithm_x
