#pragma once

#include <atomic>
#include <cstddef>
#include <memory>
#include <mutex>
#include <vector>

namespace algorithm_x {
namespace concurrent {

// SPSC 无锁队列（单生产者单消费者）— 基于环形缓冲区。
template <typename T>
class LockFreeQueue {
public:
    explicit LockFreeQueue(std::size_t capacity)
        : capacity_(capacity + 1),  // +1 to distinguish full/empty
          buffer_(new T[capacity + 1]),
          head_(0), tail_(0) {}

    ~LockFreeQueue() { delete[] buffer_; }

    // 禁止拷贝
    LockFreeQueue(const LockFreeQueue&) = delete;
    LockFreeQueue& operator=(const LockFreeQueue&) = delete;

    bool push(const T& item) {
        std::size_t tail = tail_.load(std::memory_order_relaxed);
        std::size_t next = (tail + 1) % capacity_;
        if (next == head_.load(std::memory_order_acquire)) {
            return false;  // 队列满
        }
        buffer_[tail] = item;
        tail_.store(next, std::memory_order_release);
        return true;
    }

    bool pop(T& item) {
        std::size_t head = head_.load(std::memory_order_relaxed);
        if (head == tail_.load(std::memory_order_acquire)) {
            return false;  // 队列空
        }
        item = buffer_[head];
        head_.store((head + 1) % capacity_, std::memory_order_release);
        return true;
    }

    bool empty() const {
        return head_.load(std::memory_order_acquire) ==
               tail_.load(std::memory_order_acquire);
    }

private:
    std::size_t capacity_;
    T* buffer_;
    std::atomic<std::size_t> head_;
    std::atomic<std::size_t> tail_;
};

// 线程安全单例（Double-Checked Locking + std::call_once）。
template <typename T>
class Singleton {
public:
    static T& instance() {
        static T inst;
        return inst;
    }

protected:
    Singleton() = default;
    ~Singleton() = default;
    Singleton(const Singleton&) = delete;
    Singleton& operator=(const Singleton&) = delete;
};

// 简单的读写锁（写优先）。
class ReadWriteLock {
public:
    void lock_read() {
        std::unique_lock<std::mutex> lock(mutex_);
        read_cv_.wait(lock, [this] { return writers_waiting_ == 0; });
        ++readers_;
    }

    void unlock_read() {
        std::unique_lock<std::mutex> lock(mutex_);
        if (--readers_ == 0 && writers_waiting_ > 0) {
            write_cv_.notify_one();
        }
    }

    void lock_write() {
        std::unique_lock<std::mutex> lock(mutex_);
        ++writers_waiting_;
        write_cv_.wait(lock, [this] { return readers_ == 0 && !writing_; });
        --writers_waiting_;
        writing_ = true;
    }

    void unlock_write() {
        std::unique_lock<std::mutex> lock(mutex_);
        writing_ = false;
        if (writers_waiting_ > 0) {
            write_cv_.notify_one();
        } else {
            read_cv_.notify_all();
        }
    }

private:
    std::mutex mutex_;
    std::condition_variable read_cv_;
    std::condition_variable write_cv_;
    int readers_ = 0;
    int writers_waiting_ = 0;
    bool writing_ = false;
};

}  // namespace concurrent
}  // namespace algorithm_x
