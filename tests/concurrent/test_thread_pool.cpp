#include "algorithm_x/concurrent/thread_pool.h"

#include <algorithm>
#include <chrono>
#include <cstddef>
#include <future>
#include <thread>
#include <vector>

#include "gtest/gtest.h"

using namespace algorithm_x::concurrent;

namespace {

TEST(ThreadPool, SingleTask) {
    ThreadPool pool(4);
    auto fut = pool.submit([] { return 42; });
    EXPECT_EQ(fut.get(), 42);
}

TEST(ThreadPool, MultipleTasks) {
    ThreadPool pool(4);
    std::vector<std::future<int>> futures;
    for (int i = 0; i < 100; ++i) {
        futures.push_back(pool.submit([i] { return i * i; }));
    }
    for (int i = 0; i < 100; ++i) {
        EXPECT_EQ(futures[static_cast<std::size_t>(i)].get(), i * i);
    }
}

TEST(ThreadPool, WorkerCount) {
    ThreadPool pool(8);
    EXPECT_EQ(pool.worker_count(), 8);
}

TEST(ThreadPool, SleepTasks) {
    ThreadPool pool(4);
    std::vector<std::future<bool>> futures;
    for (int i = 0; i < 10; ++i) {
        futures.push_back(pool.submit([] {
            std::this_thread::sleep_for(std::chrono::milliseconds(10));
            return true;
        }));
    }
    for (auto& f : futures) {
        EXPECT_TRUE(f.get());
    }
}

TEST(ThreadPool, LambdaWithCaptures) {
    ThreadPool pool(2);
    int x = 10, y = 20;
    auto fut = pool.submit([x, y] { return x + y; });
    EXPECT_EQ(fut.get(), 30);
}

TEST(ThreadPool, VoidTask) {
    ThreadPool pool(2);
    int counter = 0;
    {
        auto fut = pool.submit([&counter] { ++counter; });
        fut.get();
    }
    EXPECT_EQ(counter, 1);
}

}  // namespace
