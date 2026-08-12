#pragma once

#include <cstddef>
#include <functional>
#include <stdexcept>
#include <utility>
#include "dynamic_array.h"

namespace algorithm_x {
namespace ds {

// PriorityQueue — 二叉堆实现，默认大顶堆。
// 模板参数 Cmp 控制堆序：std::less<T> → 大顶堆，std::greater<T> → 小顶堆。
template <typename T, typename Cmp = std::less<T>>
class PriorityQueue {
public:
    PriorityQueue() = default;

    explicit PriorityQueue(const Cmp& cmp) : cmp_(cmp) {}

    void push(const T& value) {
        data_.push_back(value);
        sift_up(data_.size() - 1);
    }

    void push(T&& value) {
        data_.push_back(std::move(value));
        sift_up(data_.size() - 1);
    }

    void pop() {
        if (data_.empty()) {
            throw std::out_of_range("PriorityQueue::pop: empty heap");
        }
        data_[0] = std::move(data_.back());
        data_.pop_back();
        if (!data_.empty()) {
            sift_down(0);
        }
    }

    const T& top() const {
        if (data_.empty()) {
            throw std::out_of_range("PriorityQueue::top: empty heap");
        }
        return data_[0];
    }

    std::size_t size() const { return data_.size(); }
    bool empty() const { return data_.empty(); }

private:
    void sift_up(std::size_t i) {
        while (i > 0) {
            std::size_t parent = (i - 1) / 2;
            if (cmp_(data_[parent], data_[i])) {
                std::swap(data_[parent], data_[i]);
                i = parent;
            } else {
                break;
            }
        }
    }

    void sift_down(std::size_t i) {
        std::size_t n = data_.size();
        while (true) {
            std::size_t best = i;
            std::size_t left = 2 * i + 1;
            std::size_t right = 2 * i + 2;
            if (left < n && cmp_(data_[best], data_[left])) {
                best = left;
            }
            if (right < n && cmp_(data_[best], data_[right])) {
                best = right;
            }
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
