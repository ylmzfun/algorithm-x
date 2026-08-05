#pragma once

#include <algorithm>
#include <cstddef>
#include <string>
#include <vector>

namespace algorithm_x {
namespace string {

// 后缀数组 — O(n log² n)，Doubling + 基数排序。
class SuffixArray {
public:
    explicit SuffixArray(const std::string& s) : s_(s), n_(s.size()) {
        build();
        build_lcp();
    }

    // sa_[i] = 字典序第 i 小的后缀的起始下标。
    const std::vector<std::size_t>& sa() const { return sa_; }

    // rank_[i] = 后缀 i 的字典序排名。
    const std::vector<std::size_t>& rank() const { return rank_; }

    // lcp_[i] = sa[i-1] 和 sa[i] 的最长公共前缀长度（lcp_[0] = 0）。
    const std::vector<std::size_t>& lcp() const { return lcp_; }

    std::size_t size() const { return n_; }

private:
    void build() {
        sa_.resize(n_);
        rank_.resize(n_);
        std::vector<std::size_t> tmp(n_);

        // 初始：按第一个字符排序
        for (std::size_t i = 0; i < n_; ++i) {
            sa_[i] = i;
            rank_[i] = static_cast<std::size_t>(s_[i]);
        }

        auto cmp = [&](std::size_t i, std::size_t j) {
            if (rank_[i] != rank_[j]) return rank_[i] < rank_[j];
            std::size_t ri = i + k_ < n_ ? rank_[i + k_] : 0;
            std::size_t rj = j + k_ < n_ ? rank_[j + k_] : 0;
            return ri < rj;
        };

        for (k_ = 1; k_ < n_; k_ <<= 1) {
            std::sort(sa_.begin(), sa_.end(), cmp);
            tmp[sa_[0]] = 0;
            for (std::size_t i = 1; i < n_; ++i) {
                tmp[sa_[i]] = tmp[sa_[i - 1]] + (cmp(sa_[i - 1], sa_[i]) ? 1 : 0);
            }
            rank_.swap(tmp);
            if (rank_[sa_[n_ - 1]] == n_ - 1) break;
        }
    }

    void build_lcp() {
        lcp_.resize(n_, 0);
        std::size_t h = 0;
        for (std::size_t i = 0; i < n_; ++i) {
            if (rank_[i] == 0) continue;
            std::size_t j = sa_[rank_[i] - 1];
            while (i + h < n_ && j + h < n_ && s_[i + h] == s_[j + h]) {
                ++h;
            }
            lcp_[rank_[i]] = h;
            if (h > 0) --h;
        }
    }

    std::string s_;
    std::size_t n_;
    std::size_t k_;
    std::vector<std::size_t> sa_;
    std::vector<std::size_t> rank_;
    std::vector<std::size_t> lcp_;
};

}  // namespace string
}  // namespace algorithm_x
