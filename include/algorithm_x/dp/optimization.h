#pragma once

#include <cstddef>
#include <deque>
#include <vector>

namespace algorithm_x {
namespace dp {

// 单调队列优化 — 滑动窗口最大值 O(n)。
// 用于 DP 中形如 dp[i] = max_{j∈[i-k, i-1]} dp[j] + ... 的转移。
// 返回每个位置对应窗口内的最大值。
template <typename T>
std::vector<T> sliding_window_max(const std::vector<T>& arr, std::size_t k) {
    std::vector<T> result;
    std::deque<std::size_t> dq;
    for (std::size_t i = 0; i < arr.size(); ++i) {
        while (!dq.empty() && dq.front() + k <= i) dq.pop_front();
        while (!dq.empty() && arr[dq.back()] <= arr[i]) dq.pop_back();
        dq.push_back(i);
        if (i >= k - 1) result.push_back(arr[dq.front()]);
    }
    return result;
}

// 滑动窗口最小值。
template <typename T>
std::vector<T> sliding_window_min(const std::vector<T>& arr, std::size_t k) {
    std::vector<T> result;
    std::deque<std::size_t> dq;
    for (std::size_t i = 0; i < arr.size(); ++i) {
        while (!dq.empty() && dq.front() + k <= i) dq.pop_front();
        while (!dq.empty() && arr[dq.back()] >= arr[i]) dq.pop_back();
        dq.push_back(i);
        if (i >= k - 1) result.push_back(arr[dq.front()]);
    }
    return result;
}

}  // namespace dp
}  // namespace algorithm_x
