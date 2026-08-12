#pragma once

#include <algorithm>
#include <cmath>
#include <cstddef>
#include <vector>

namespace algorithm_x {
namespace advanced {

// 莫队算法 — 区间众数 / 不同元素个数查询。
// queries: 每个查询为 {l, r, idx}（闭区间）。
// arr: 原数组。
// 返回每个查询区间内不同元素的个数。
struct MoQuery {
    std::size_t l, r, idx;
};

inline std::vector<int> mo_algorithm(const std::vector<int>& arr,
                                      std::vector<MoQuery> queries) {
    std::size_t n = arr.size();
    int block_size = std::max(1, static_cast<int>(std::sqrt(n)));

    std::sort(queries.begin(), queries.end(),
              [&](const MoQuery& a, const MoQuery& b) {
                  int ba = static_cast<int>(a.l) / block_size;
                  int bb = static_cast<int>(b.l) / block_size;
                  if (ba != bb) return ba < bb;
                  return (ba % 2 == 0) ? (a.r < b.r) : (a.r > b.r);
              });

    // 离散化
    std::vector<int> sorted = arr;
    std::sort(sorted.begin(), sorted.end());
    sorted.erase(std::unique(sorted.begin(), sorted.end()), sorted.end());
    int max_val = static_cast<int>(sorted.size());

    std::vector<int> freq(static_cast<std::size_t>(max_val + 1), 0);

    auto compressed = [&](int x) {
        return static_cast<int>(
            std::lower_bound(sorted.begin(), sorted.end(), x) -
            sorted.begin());
    };

    std::vector<int> result(queries.size());
    int cur_l = 0, cur_r = -1, distinct = 0;

    auto add = [&](int pos) {
        int c = compressed(arr[static_cast<std::size_t>(pos)]);
        if (freq[static_cast<std::size_t>(c)]++ == 0) ++distinct;
    };
    auto remove = [&](int pos) {
        int c = compressed(arr[static_cast<std::size_t>(pos)]);
        if (--freq[static_cast<std::size_t>(c)] == 0) --distinct;
    };

    for (auto& q : queries) {
        int ql = static_cast<int>(q.l), qr = static_cast<int>(q.r);
        while (cur_l > ql) add(--cur_l);
        while (cur_r < qr) add(++cur_r);
        while (cur_l < ql) remove(cur_l++);
        while (cur_r > qr) remove(cur_r--);
        result[q.idx] = distinct;
    }
    return result;
}

}  // namespace advanced
}  // namespace algorithm_x
