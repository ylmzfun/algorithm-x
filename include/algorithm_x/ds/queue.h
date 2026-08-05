#pragma once

#include <cstddef>
#include <stdexcept>
#include <utility>
#include "linked_list.h"

namespace algorithm_x {
namespace ds {

template <typename T>
class Queue {
public:
    void push(const T& value) { list_.push_back(value); }
    void push(T&& value) { list_.push_back(std::move(value)); }

    void pop() {
        if (list_.empty()) {
            throw std::out_of_range("Queue::pop: empty queue");
        }
        list_.pop_front();
    }

    T& front() { return list_.front(); }
    const T& front() const { return list_.front(); }
    T& back() { return list_.back(); }
    const T& back() const { return list_.back(); }

    std::size_t size() const { return list_.size(); }
    bool empty() const { return list_.empty(); }

private:
    DoublyLinkedList<T> list_;
};

// Deque — 双端队列 (circular buffer implementation)
template <typename T>
class Deque {
public:
    Deque() : data_(new T[4]), capacity_(4) {}

    ~Deque() { delete[] data_; }

    Deque(const Deque& other) { copy_from(other); }

    Deque& operator=(const Deque& other) {
        if (this != &other) {
            delete[] data_;
            copy_from(other);
        }
        return *this;
    }

    Deque(Deque&& other) noexcept
        : data_(other.data_), head_(other.head_), tail_(other.tail_),
          size_(other.size_), capacity_(other.capacity_) {
        other.data_ = nullptr;
        other.size_ = 0;
        other.capacity_ = 0;
    }

    Deque& operator=(Deque&& other) noexcept {
        if (this != &other) {
            delete[] data_;
            data_ = other.data_;
            head_ = other.head_;
            tail_ = other.tail_;
            size_ = other.size_;
            capacity_ = other.capacity_;
            other.data_ = nullptr;
            other.size_ = 0;
            other.capacity_ = 0;
        }
        return *this;
    }

    void push_front(const T& value) {
        ensure_capacity();
        head_ = (head_ - 1 + capacity_) % capacity_;
        data_[head_] = value;
        ++size_;
    }

    void push_back(const T& value) {
        ensure_capacity();
        data_[tail_] = value;
        tail_ = (tail_ + 1) % capacity_;
        ++size_;
    }

    void pop_front() {
        if (size_ == 0) {
            throw std::out_of_range("Deque::pop_front: empty deque");
        }
        head_ = (head_ + 1) % capacity_;
        --size_;
    }

    void pop_back() {
        if (size_ == 0) {
            throw std::out_of_range("Deque::pop_back: empty deque");
        }
        tail_ = (tail_ - 1 + capacity_) % capacity_;
        --size_;
    }

    T& front() {
        if (size_ == 0) {
            throw std::out_of_range("Deque::front: empty deque");
        }
        return data_[head_];
    }

    const T& front() const {
        if (size_ == 0) {
            throw std::out_of_range("Deque::front: empty deque");
        }
        return data_[head_];
    }

    T& back() {
        if (size_ == 0) {
            throw std::out_of_range("Deque::back: empty deque");
        }
        return data_[(tail_ - 1 + capacity_) % capacity_];
    }

    const T& back() const {
        if (size_ == 0) {
            throw std::out_of_range("Deque::back: empty deque");
        }
        return data_[(tail_ - 1 + capacity_) % capacity_];
    }

    T& operator[](std::size_t i) { return data_[(head_ + i) % capacity_]; }
    const T& operator[](std::size_t i) const { return data_[(head_ + i) % capacity_]; }

    std::size_t size() const { return size_; }
    bool empty() const { return size_ == 0; }

private:
    void ensure_capacity() {
        if (size_ + 1 > capacity_) {
            std::size_t new_cap = capacity_ * 2;
            T* new_data = new T[new_cap];
            for (std::size_t i = 0; i < size_; ++i) {
                new_data[i] = std::move(data_[(head_ + i) % capacity_]);
            }
            delete[] data_;
            data_ = new_data;
            head_ = 0;
            tail_ = size_;
            capacity_ = new_cap;
        }
    }

    void copy_from(const Deque& other) {
        capacity_ = other.capacity_;
        data_ = new T[capacity_];
        head_ = 0;
        tail_ = other.size_;
        size_ = other.size_;
        for (std::size_t i = 0; i < size_; ++i) {
            data_[i] = other[i];
        }
    }

    T* data_;
    std::size_t head_ = 0;
    std::size_t tail_ = 0;
    std::size_t size_ = 0;
    std::size_t capacity_ = 0;
};

}  // namespace ds
}  // namespace algorithm_x
