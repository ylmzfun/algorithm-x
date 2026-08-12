#pragma once

#include <condition_variable>
#include <cstddef>
#include <mutex>

namespace algorithm_x {
namespace concurrent {

// 计数信号量。
class Semaphore {
public:
    explicit Semaphore(int count = 0) : count_(count) {}

    void acquire() {
        std::unique_lock<std::mutex> lock(mutex_);
        cv_.wait(lock, [this] { return count_ > 0; });
        --count_;
    }

    void release() {
        {
            std::lock_guard<std::mutex> lock(mutex_);
            ++count_;
        }
        cv_.notify_one();
    }

    int available() const {
        std::lock_guard<std::mutex> lock(mutex_);
        return count_;
    }

private:
    mutable std::mutex mutex_;
    std::condition_variable cv_;
    int count_;
};

// 可复用屏障。
class Barrier {
public:
    explicit Barrier(std::size_t count) : threshold_(count), count_(count) {}

    void wait() {
        std::unique_lock<std::mutex> lock(mutex_);
        if (--count_ == 0) {
            ++generation_;
            count_ = threshold_;
            cv_.notify_all();
        } else {
            std::size_t gen = generation_;
            cv_.wait(lock, [this, gen] { return gen != generation_; });
        }
    }

private:
    std::mutex mutex_;
    std::condition_variable cv_;
    std::size_t threshold_;
    std::size_t count_;
    std::size_t generation_ = 0;
};

}  // namespace concurrent
}  // namespace algorithm_x
