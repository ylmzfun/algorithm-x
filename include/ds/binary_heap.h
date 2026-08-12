#pragma once

#include <cstddef>
#include <functional>
#include <stdexcept>
#include <utility>
#include "dynamic_array.h"

namespace algorithm_x {
namespace ds {

// BinaryHeap — 暴露底层数组的二叉堆，支持 O(n) 建堆（heapify）。
// 同样用 Cmp 控制：std::less → 大顶堆，std::greater → 小顶堆。
template <typename T, typename Cmp = std::less<T>>
class BinaryHeap {
public:
    BinaryHeap() = default;
    explicit BinaryHeap(const Cmp& cmp) : cmp_(cmp) {}

    // O(n) 建堆
    explicit BinaryHeap(const DynamicArray<T>& arr, const Cmp& cmp = Cmp())
        : data_(arr), cmp_(cmp) {
        heapify();
    }

    void push(const T& value) {
        data_.push_back(value);
        sift_up(data_.size() - 1);
    }

    void pop() {
        if (data_.empty()) throw std::out_of_range("BinaryHeap::pop: empty");
        data_[0] = std::move(data_.back());
        data_.pop_back();
        if (!data_.empty()) sift_down(0);
    }

    const T& top() const {
        if (data_.empty()) throw std::out_of_range("BinaryHeap::top: empty");
        return data_[0];
    }

    std::size_t size() const { return data_.size(); }
    bool empty() const { return data_.empty(); }

private:
    void heapify() {
        if (data_.size() <= 1) return;
        for (std::size_t i = data_.size() / 2; i-- > 0;) {
            sift_down(i);
        }
    }

    void sift_up(std::size_t i) {
        while (i > 0) {
            std::size_t p = (i - 1) / 2;
            if (cmp_(data_[p], data_[i])) {
                std::swap(data_[p], data_[i]);
                i = p;
            } else break;
        }
    }

    void sift_down(std::size_t i) {
        std::size_t n = data_.size();
        while (true) {
            std::size_t best = i;
            std::size_t l = 2 * i + 1, r = 2 * i + 2;
            if (l < n && cmp_(data_[best], data_[l])) best = l;
            if (r < n && cmp_(data_[best], data_[r])) best = r;
            if (best == i) break;
            std::swap(data_[i], data_[best]);
            i = best;
        }
    }

    DynamicArray<T> data_;
    Cmp cmp_;
};

}  // namespace ds
}  // namespace algorithm_x
