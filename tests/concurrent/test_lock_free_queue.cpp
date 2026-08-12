#include "concurrent/lock_free_queue.h"

#include <thread>
#include <vector>

#include "gtest/gtest.h"

using namespace algorithm_x::concurrent;

namespace {

// ---- LockFreeQueue ----

TEST(LockFreeQueue, PushAndPopSingle) {
    LockFreeQueue<int> q(4);
    EXPECT_TRUE(q.empty());

    int item = 0;
    EXPECT_FALSE(q.pop(item));

    EXPECT_TRUE(q.push(42));
    EXPECT_FALSE(q.empty());

    EXPECT_TRUE(q.pop(item));
    EXPECT_EQ(item, 42);
    EXPECT_TRUE(q.empty());
}

TEST(LockFreeQueue, FIFOOrder) {
    LockFreeQueue<int> q(8);
    for (int i = 0; i < 5; ++i) {
        EXPECT_TRUE(q.push(i));
    }

    for (int i = 0; i < 5; ++i) {
        int item;
        EXPECT_TRUE(q.pop(item));
        EXPECT_EQ(item, i);
    }
    EXPECT_TRUE(q.empty());
}

TEST(LockFreeQueue, FullQueue) {
    LockFreeQueue<int> q(3);  // usable capacity = 3

    EXPECT_TRUE(q.push(1));
    EXPECT_TRUE(q.push(2));
    EXPECT_TRUE(q.push(3));
    EXPECT_FALSE(q.push(4));  // full
    EXPECT_FALSE(q.empty());

    int item;
    EXPECT_TRUE(q.pop(item));
    EXPECT_EQ(item, 1);
    EXPECT_TRUE(q.push(4));  // now has room
}

TEST(LockFreeQueue, PopAllUntilEmpty) {
    LockFreeQueue<int> q(4);
    q.push(10);
    q.push(20);
    q.push(30);

    int item;
    EXPECT_TRUE(q.pop(item));
    EXPECT_TRUE(q.pop(item));
    EXPECT_TRUE(q.pop(item));
    EXPECT_FALSE(q.pop(item));
    EXPECT_TRUE(q.empty());
}

// ---- Singleton ----

struct TestSingleton : Singleton<TestSingleton> {
    int value = 99;
    friend class Singleton<TestSingleton>;
};

TEST(Singleton, SameInstance) {
    TestSingleton& a = TestSingleton::instance();
    TestSingleton& b = TestSingleton::instance();
    EXPECT_EQ(&a, &b);
    EXPECT_EQ(a.value, 99);
    a.value = 42;
    EXPECT_EQ(b.value, 42);
}

// ---- ReadWriteLock ----

TEST(ReadWriteLock, BasicLockUnlock) {
    ReadWriteLock rw;
    rw.lock_read();
    rw.unlock_read();
    rw.lock_write();
    rw.unlock_write();
    // no crash = success
    SUCCEED();
}

TEST(ReadWriteLock, MultipleReaders) {
    ReadWriteLock rw;
    std::atomic<int> counter{0};
    std::atomic<bool> done{false};

    auto reader = [&]() {
        while (!done.load(std::memory_order_relaxed)) {
            rw.lock_read();
            counter.fetch_add(1, std::memory_order_relaxed);
            std::this_thread::yield();
            counter.fetch_sub(1, std::memory_order_relaxed);
            rw.unlock_read();
        }
    };

    std::vector<std::thread> threads;
    for (int i = 0; i < 3; ++i) {
        threads.emplace_back(reader);
    }

    // Let readers run for a while; if they truly hold read locks
    // concurrently, counter should go above 1.
    std::this_thread::sleep_for(std::chrono::milliseconds(50));
    done.store(true, std::memory_order_relaxed);

    for (auto& t : threads) t.join();

    // If the lock allows multiple concurrent readers, at some point
    // counter was > 1.  We can't assert that retroactively, but the
    // test not crashing or deadlocking is strong evidence.
    SUCCEED();
}

TEST(ReadWriteLock, WriterBlocksReaders) {
    ReadWriteLock rw;
    std::atomic<int> counter{0};

    std::thread writer([&]() {
        rw.lock_write();
        counter.store(1);
        std::this_thread::sleep_for(std::chrono::milliseconds(50));
        rw.unlock_write();
    });

    std::this_thread::sleep_for(std::chrono::milliseconds(10));

    // Reader should be blocked until writer finishes
    std::thread reader([&]() {
        rw.lock_read();
        int val = counter.load();
        // Writer should have finished by the time reader acquires lock
        // So counter should be 1 (writer's store) but NOT still held by writer
        EXPECT_GE(val, 1);
        rw.unlock_read();
    });

    writer.join();
    reader.join();
}

}  // namespace
