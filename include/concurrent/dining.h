#pragma once

#include <atomic>
#include <chrono>
#include <cstddef>
#include <mutex>
#include <thread>
#include <vector>

namespace algorithm_x {
namespace concurrent {

// 哲学家就餐 — 资源分级法，编号小的筷子先拿。
class DiningPhilosophers {
public:
    DiningPhilosophers(int num = 5) : num_(num), forks_(static_cast<std::size_t>(num)) {
        for (int i = 0; i < num_; ++i) {
            forks_[static_cast<std::size_t>(i)] = new std::mutex();
        }
    }

    ~DiningPhilosophers() {
        for (int i = 0; i < num_; ++i) {
            delete forks_[static_cast<std::size_t>(i)];
        }
    }

    // 哲学家 id 执行一次吃饭-思考循环。
    void philosopher(int id) {
        int left = id;
        int right = (id + 1) % num_;
        // 资源分级：先拿编号小的，再拿编号大的，避免死锁
        int first = std::min(left, right);
        int second = std::max(left, right);

        // 思考
        std::this_thread::sleep_for(std::chrono::milliseconds(1));

        // 拿叉子
        forks_[static_cast<std::size_t>(first)]->lock();
        forks_[static_cast<std::size_t>(second)]->lock();

        // 吃饭
        eat_count_.fetch_add(1);

        // 放叉子
        forks_[static_cast<std::size_t>(second)]->unlock();
        forks_[static_cast<std::size_t>(first)]->unlock();
    }

    // 启动所有哲学家并发执行 n 轮。
    void run(int rounds = 1) {
        eat_count_.store(0);
        std::vector<std::thread> threads;
        for (int r = 0; r < rounds; ++r) {
            for (int i = 0; i < num_; ++i) {
                threads.emplace_back(&DiningPhilosophers::philosopher, this, i);
            }
            for (auto& t : threads) t.join();
            threads.clear();
        }
    }

    int eat_count() const { return eat_count_.load(); }

private:
    int num_;
    std::vector<std::mutex*> forks_;
    std::atomic<int> eat_count_{0};
};

}  // namespace concurrent
}  // namespace algorithm_x
