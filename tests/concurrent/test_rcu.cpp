#include "concurrent/rcu.h"

#include <atomic>
#include <mutex>
#include <thread>
#include <vector>

#include "gtest/gtest.h"

using namespace algorithm_x::concurrent;

namespace {

TEST(Rcu, BasicReadUpdate) {
    RcuValue<int> rcu(0);
    EXPECT_EQ(rcu.read(), 0);
    rcu.update(42);
    EXPECT_EQ(rcu.read(), 42);
    rcu.update(-1);
    EXPECT_EQ(rcu.read(), -1);
}

// 并发验证：4 个读者 + 1 个写者。
// 写者依次发布 0..kRounds；读者反复读取快照（用互斥收集观察值）。
// 断言：所有观察值都属于已发布集合，且写者结束后 read() 等于最后发布的值。
// 只断言最终一致状态，不依赖线程调度时序，避免 flaky。
TEST(Rcu, ConcurrentReaders) {
    RcuValue<int> rcu(0);
    constexpr int kRounds = 200;
    std::atomic<bool> stop{false};
    std::vector<int> observed;
    std::mutex observed_mutex;

    std::vector<std::thread> readers;
    for (int i = 0; i < 4; ++i) {
        readers.emplace_back([&] {
            while (!stop.load(std::memory_order_acquire)) {
                int v = rcu.read();
                {
                    std::lock_guard<std::mutex> lock(observed_mutex);
                    observed.push_back(v);
                }
            }
        });
    }

    std::thread writer([&] {
        for (int i = 0; i <= kRounds; ++i) {
            rcu.update(i);
        }
    });
    writer.join();
    stop.store(true, std::memory_order_release);
    for (auto& t : readers) {
        t.join();
    }

    {
        std::lock_guard<std::mutex> lock(observed_mutex);
        for (int v : observed) {
            EXPECT_GE(v, 0);
            EXPECT_LE(v, kRounds);
        }
    }
    EXPECT_EQ(rcu.read(), kRounds);
}

}  // namespace
