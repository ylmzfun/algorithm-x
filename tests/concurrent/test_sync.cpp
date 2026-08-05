#include "algorithm_x/concurrent/sync.h"
#include <atomic>
#include <thread>
#include <vector>
#include "gtest/gtest.h"
using namespace algorithm_x::concurrent;
namespace {
TEST(Semaphore, Basic) {
    Semaphore sem(2); sem.acquire(); sem.acquire();
    std::atomic<int> cnt{0};
    std::thread t([&]() { sem.acquire(); ++cnt; sem.release(); });
    std::this_thread::sleep_for(std::chrono::milliseconds(10));
    EXPECT_EQ(cnt.load(), 0);
    sem.release(); t.join();
    EXPECT_EQ(cnt.load(), 1);
}
TEST(Barrier, Basic) {
    const int N = 3; Barrier bar(N); std::atomic<int> cnt{0};
    std::vector<std::thread> threads;
    for (int i = 0; i < N; ++i) threads.emplace_back([&]() { ++cnt; bar.wait(); });
    for (auto& t : threads) t.join();
    EXPECT_EQ(cnt.load(), N);
}
}  // namespace
