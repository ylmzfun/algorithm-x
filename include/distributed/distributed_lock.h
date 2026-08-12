#pragma once

#include <atomic>
#include <cstddef>
#include <thread>
#include <vector>

namespace algorithm_x {
namespace distributed {

// 简易分布式锁（Lamport 风格模拟）— 单机多线程模拟。
class DistributedLock {
public:
    explicit DistributedLock(std::size_t num_nodes) : locked_(num_nodes) {
        for (auto& flag : locked_) {
            flag.store(false);
        }
    }

    // 尝试获取锁。
    bool acquire(std::size_t node_id) {
        bool expected = false;
        if (locked_[node_id].compare_exchange_strong(expected, true)) {
            return true;
        }
        return false;
    }

    // 释放锁。
    void release(std::size_t node_id) {
        locked_[node_id].store(false);
    }

    bool is_locked(std::size_t node_id) const {
        return locked_[node_id].load();
    }

private:
    std::vector<std::atomic<bool>> locked_;
};

}  // namespace distributed
}  // namespace algorithm_x
