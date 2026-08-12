#pragma once

#include <algorithm>
#include <cmath>
#include <cstddef>
#include <cstdint>
#include <vector>

namespace algorithm_x {
namespace advanced {

// 树套树与分块
// ============
// 两种"以空间换时间"的结构化查询思想：
// 1) 分块（SqrtDecomp）：把数组切成约 sqrt(n) 大小的块，额外维护每块的
//    "块信息"（这里是块和）。区间求和时，完整的块直接取块和 O(1)，
//    只有两端不足一块的部分需要逐个元素累加，单次查询 O(sqrt(n))，
//    单点修改只需更新所在块，O(1)。
// 2) 树套树（FenwickOfSets）：外层是一棵 Fenwick（树状数组），内层每个
//    BIT 节点挂一个有序集合（排好序的 std::vector）。BIT 的每个节点
//    恰好覆盖一段连续下标区间，于是"前缀中的二维偏序计数"可拆成
//    O(log n) 个有序集合上的二分，单次查询 O(log^2 n)。
class SqrtDecomp {
public:
    // 用 data 建块，块大小为 sqrt(n)，并预计算每块的块和。
    explicit SqrtDecomp(const std::vector<int64_t>& data)
        : data_(data),
          block_size_(std::max<std::size_t>(
              1, static_cast<std::size_t>(std::sqrt(data.size())))) {
        block_sum_.assign((data_.size() + block_size_ - 1) / block_size_, 0);
        for (std::size_t i = 0; i < data_.size(); ++i) {
            block_sum_[i / block_size_] += data_[i];
        }
    }

    // 单点加：data[pos] += delta，并同步更新 pos 所在块的块和。
    void point_update(std::size_t pos, int64_t delta) {
        data_[pos] += delta;
        block_sum_[pos / block_size_] += delta;
    }

    // 闭区间 [l, r] 求和：完整块直接取块和，两端零散部分逐个累加。
    int64_t range_sum(std::size_t l, std::size_t r) const {
        if (data_.empty() || l > r || r >= data_.size()) return 0;
        int64_t sum = 0;
        std::size_t bl = l / block_size_;
        std::size_t br = r / block_size_;
        if (bl == br) {
            for (std::size_t i = l; i <= r; ++i) sum += data_[i];
            return sum;
        }
        for (std::size_t i = l; i < (bl + 1) * block_size_; ++i) sum += data_[i];
        for (std::size_t b = bl + 1; b < br; ++b) sum += block_sum_[b];
        for (std::size_t i = br * block_size_; i <= r; ++i) sum += data_[i];
        return sum;
    }

private:
    std::vector<int64_t> data_;        // 原数组（支持单点修改）
    std::size_t block_size_;           // 每块大小
    std::vector<int64_t> block_sum_;   // 每块的块和
};

// Fenwick 套有序集合：外层树状数组，内层每个 BIT 节点保存其覆盖区间内
// 所有元素排序后的值。用于静态数组上的"前 r+1 个元素中 ≤ x 的个数"
// （经典二维偏序计数，树套树思想）。
class FenwickOfSets {
public:
    // 建树：对每个元素，沿 BIT 自下而上累加到所有覆盖它的节点。
    explicit FenwickOfSets(const std::vector<int>& values)
        : n_(values.size()), trees_(values.size() + 1) {
        for (std::size_t i = 0; i < values.size(); ++i) {
            for (std::size_t j = i + 1; j <= values.size();
                 j += j & (~j + 1)) {  // 沿 lowbit 向上
                trees_[j].push_back(values[i]);
            }
        }
        for (auto& t : trees_) {
            std::sort(t.begin(), t.end());
        }
    }

    // 前 r+1 个元素（下标 0..r）中 ≤ x 的个数。
    // 前缀 [0..r] 在 BIT 上分解为 O(log n) 个节点，每个节点用
    // upper_bound 在有序集合中二分计数。
    std::size_t count_less_equal(std::size_t r, int x) const {
        if (n_ == 0 || r >= n_) return 0;
        std::size_t cnt = 0;
        for (std::size_t j = r + 1; j > 0; j -= j & (~j + 1)) {
            cnt += static_cast<std::size_t>(
                std::upper_bound(trees_[j].begin(), trees_[j].end(), x) -
                trees_[j].begin());
        }
        return cnt;
    }

private:
    std::size_t n_;
    std::vector<std::vector<int>> trees_;  // trees_[j] 覆盖 (j-lowbit(j), j]
};

}  // namespace advanced
}  // namespace algorithm_x
