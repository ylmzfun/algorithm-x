#include "concurrent/lock_free_stack.h"
#include <thread>
#include <vector>
#include "gtest/gtest.h"
using namespace algorithm_x::concurrent;
namespace {
TEST(LockFreeStack, PushPop) {
    LockFreeStack<int> s; s.push(1); s.push(2);
    int v; EXPECT_TRUE(s.pop(v)); EXPECT_EQ(v, 2);
    EXPECT_TRUE(s.pop(v)); EXPECT_EQ(v, 1);
    EXPECT_FALSE(s.pop(v));
}
TEST(LockFreeStack, Empty) { LockFreeStack<int> s; EXPECT_TRUE(s.empty()); s.push(1); EXPECT_FALSE(s.empty()); }
TEST(LockFreeStack, Concurrent) {
    LockFreeStack<int> s; std::vector<std::thread> ts;
    for (int i = 0; i < 4; ++i) ts.emplace_back([&s, i]() { for (int j = 0; j < 100; ++j) s.push(i*100+j); });
    for (auto& t : ts) t.join();
    int cnt = 0, v; while (s.pop(v)) ++cnt;
    EXPECT_EQ(cnt, 400);
}
}  // namespace
