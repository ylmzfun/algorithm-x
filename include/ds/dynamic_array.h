#pragma once

#include <algorithm>
#include <cstddef>
#include <initializer_list>
#include <stdexcept>
#include <utility>

namespace algorithm_x {
namespace ds {

template <typename T>
class DynamicArray {
public:
    DynamicArray() = default;

    DynamicArray(std::initializer_list<T> init) {
        reserve(init.size());
        for (const auto& v : init) {
            push_back(v);
        }
    }

    DynamicArray(const DynamicArray& other) { copy_from(other); }

    DynamicArray& operator=(const DynamicArray& other) {
        if (this != &other) {
            delete[] data_;
            copy_from(other);
        }
        return *this;
    }

    DynamicArray(DynamicArray&& other) noexcept
        : data_(other.data_), size_(other.size_), capacity_(other.capacity_) {
        other.data_ = nullptr;
        other.size_ = 0;
        other.capacity_ = 0;
    }

    DynamicArray& operator=(DynamicArray&& other) noexcept {
        if (this != &other) {
            delete[] data_;
            data_ = other.data_;
            size_ = other.size_;
            capacity_ = other.capacity_;
            other.data_ = nullptr;
            other.size_ = 0;
            other.capacity_ = 0;
        }
        return *this;
    }

    ~DynamicArray() { delete[] data_; }

    void push_back(const T& value) {
        ensure_capacity(size_ + 1);
        data_[size_++] = value;
    }

    void push_back(T&& value) {
        ensure_capacity(size_ + 1);
        data_[size_++] = std::move(value);
    }

    void pop_back() {
        if (size_ == 0) {
            throw std::out_of_range("DynamicArray::pop_back: empty array");
        }
        --size_;
    }

    void insert(std::size_t index, const T& value) {
        if (index > size_) {
            throw std::out_of_range("DynamicArray::insert: index out of range");
        }
        ensure_capacity(size_ + 1);
        for (std::size_t i = size_; i > index; --i) {
            data_[i] = std::move(data_[i - 1]);
        }
        data_[index] = value;
        ++size_;
    }

    void erase(std::size_t index) {
        if (index >= size_) {
            throw std::out_of_range("DynamicArray::erase: index out of range");
        }
        for (std::size_t i = index; i + 1 < size_; ++i) {
            data_[i] = std::move(data_[i + 1]);
        }
        --size_;
    }

    void reserve(std::size_t new_capacity) {
        if (new_capacity > capacity_) {
            reallocate(new_capacity);
        }
    }

    void clear() { size_ = 0; }

    T& operator[](std::size_t index) { return data_[index]; }
    const T& operator[](std::size_t index) const { return data_[index]; }

    T& at(std::size_t index) {
        if (index >= size_) {
            throw std::out_of_range("DynamicArray::at: index out of range");
        }
        return data_[index];
    }

    const T& at(std::size_t index) const {
        if (index >= size_) {
            throw std::out_of_range("DynamicArray::at: index out of range");
        }
        return data_[index];
    }

    T& front() { return data_[0]; }
    const T& front() const { return data_[0]; }
    T& back() { return data_[size_ - 1]; }
    const T& back() const { return data_[size_ - 1]; }

    T* data() { return data_; }
    const T* data() const { return data_; }

    std::size_t size() const { return size_; }
    std::size_t capacity() const { return capacity_; }
    bool empty() const { return size_ == 0; }

    T* begin() { return data_; }
    const T* begin() const { return data_; }
    T* end() { return data_ + size_; }
    const T* end() const { return data_ + size_; }

private:
    void ensure_capacity(std::size_t required) {
        if (required > capacity_) {
            std::size_t new_cap = capacity_ == 0 ? 4 : capacity_ * 2;
            if (new_cap < required) {
                new_cap = required;
            }
            reallocate(new_cap);
        }
    }

    void reallocate(std::size_t new_capacity) {
        T* new_data = new T[new_capacity];
        for (std::size_t i = 0; i < size_; ++i) {
            new_data[i] = std::move(data_[i]);
        }
        delete[] data_;
        data_ = new_data;
        capacity_ = new_capacity;
    }

    void copy_from(const DynamicArray& other) {
        size_ = other.size_;
        capacity_ = other.capacity_;
        data_ = new T[capacity_];
        for (std::size_t i = 0; i < size_; ++i) {
            data_[i] = other.data_[i];
        }
    }

    T* data_ = nullptr;
    std::size_t size_ = 0;
    std::size_t capacity_ = 0;
};

}  // namespace ds
}  // namespace algorithm_x
