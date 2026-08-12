#pragma once

#include <cstddef>
#include <stdexcept>
#include <utility>
#include "dynamic_array.h"

namespace algorithm_x {
namespace ds {

template <typename T>
class Stack {
public:
    void push(const T& value) { data_.push_back(value); }
    void push(T&& value) { data_.push_back(std::move(value)); }

    void pop() {
        if (data_.empty()) {
            throw std::out_of_range("Stack::pop: empty stack");
        }
        data_.pop_back();
    }

    T& top() {
        if (data_.empty()) {
            throw std::out_of_range("Stack::top: empty stack");
        }
        return data_.back();
    }

    const T& top() const {
        if (data_.empty()) {
            throw std::out_of_range("Stack::top: empty stack");
        }
        return data_.back();
    }

    std::size_t size() const { return data_.size(); }
    bool empty() const { return data_.empty(); }

private:
    DynamicArray<T> data_;
};

// MonotonicStack — 单调栈
// // Maintains elements in strictly increasing (Cmp = std::less) or decreasing
// (Cmp = std::greater) order. When pushing an element, all elements that
// violate monotonicity are popped first.
template <typename T, typename Cmp = std::less<T>>
class MonotonicStack {
public:
    // Push value; returns number of elements popped to maintain monotonicity.
    std::size_t push(const T& value) {
        std::size_t popped = 0;
        while (!data_.empty() && cmp_(value, data_.top())) {
            data_.pop();
            ++popped;
        }
        data_.push(value);
        return popped;
    }

    void pop() {
        if (data_.empty()) {
            throw std::out_of_range("MonotonicStack::pop: empty stack");
        }
        data_.pop();
    }

    T& top() { return data_.top(); }
    const T& top() const { return data_.top(); }
    std::size_t size() const { return data_.size(); }
    bool empty() const { return data_.empty(); }

private:
    Stack<T> data_;
    Cmp cmp_;
};

}  // namespace ds
}  // namespace algorithm_x
