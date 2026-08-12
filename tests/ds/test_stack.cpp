#include <gtest/gtest.h>
#include <stdexcept>
#include "ds/stack.h"

using namespace algorithm_x::ds;

// ==================== Stack ====================

TEST(Stack, PushPop) {
    Stack<int> s;
    s.push(1);
    s.push(2);
    s.push(3);
    EXPECT_EQ(s.top(), 3);
    s.pop();
    EXPECT_EQ(s.top(), 2);
    s.pop();
    EXPECT_EQ(s.top(), 1);
    s.pop();
    EXPECT_TRUE(s.empty());
}

TEST(Stack, TopConstNonConst) {
    Stack<int> s;
    s.push(42);
    EXPECT_EQ(s.top(), 42);
    s.top() = 99;
    EXPECT_EQ(s.top(), 99);

    const Stack<int>& cs = s;
    EXPECT_EQ(cs.top(), 99);
}

TEST(Stack, EmptyPopThrows) {
    Stack<int> s;
    EXPECT_THROW(s.pop(), std::out_of_range);
    EXPECT_THROW(s.top(), std::out_of_range);
}

TEST(Stack, SizeAndEmpty) {
    Stack<int> s;
    EXPECT_TRUE(s.empty());
    EXPECT_EQ(s.size(), 0u);
    s.push(1);
    EXPECT_FALSE(s.empty());
    EXPECT_EQ(s.size(), 1u);
    s.push(2);
    EXPECT_EQ(s.size(), 2u);
    s.pop();
    EXPECT_EQ(s.size(), 1u);
}

TEST(Stack, LifoOrder) {
    Stack<int> s;
    for (int i = 0; i < 5; ++i) s.push(i);
    for (int i = 4; i >= 0; --i) {
        EXPECT_EQ(s.top(), i);
        s.pop();
    }
}

// ==================== MonotonicStack ====================

TEST(MonotonicStack, IncreasingOrder) {
    // std::less: pops while new value < top → stack increases bottom→top
    MonotonicStack<int, std::less<int>> ms;
    ms.push(1);
    EXPECT_EQ(ms.top(), 1);
    ms.push(3);  // 3 < 1? No → keep 1
    EXPECT_EQ(ms.top(), 3);
    ms.push(2);  // 2 < 3? Yes → pop 3; 2 < 1? No → keep 1
    EXPECT_EQ(ms.top(), 2);
    ms.push(4);  // 4 < 2? No → keep all
    EXPECT_EQ(ms.top(), 4);
    // Stack from bottom to top: 1, 2, 4 (increasing order)
    ms.pop();
    EXPECT_EQ(ms.top(), 2);
    ms.pop();
    EXPECT_EQ(ms.top(), 1);
}

TEST(MonotonicStack, DecreasingOrder) {
    // std::greater: pops while new value > top → stack decreases bottom→top
    MonotonicStack<int, std::greater<int>> ms;
    ms.push(5);
    EXPECT_EQ(ms.top(), 5);
    ms.push(3);  // 3 > 5? No → keep 5
    EXPECT_EQ(ms.top(), 3);
    ms.push(4);  // 4 > 3? Yes → pop 3; 4 > 5? No → keep 5
    EXPECT_EQ(ms.top(), 4);
    ms.push(1);  // 1 > 4? No → keep all
    EXPECT_EQ(ms.top(), 1);
    // Stack from bottom to top: 5, 4, 1 (decreasing order)
    ms.pop();
    EXPECT_EQ(ms.top(), 4);
    ms.pop();
    EXPECT_EQ(ms.top(), 5);
}

TEST(MonotonicStack, PushReturnsPoppedCount) {
    MonotonicStack<int, std::less<int>> ms;
    ms.push(1);
    ms.push(4);
    ms.push(3);  // 3 < 4 → pop 1 element
    auto popped = ms.push(2);  // 2 < 3 → pop 1 element
    EXPECT_EQ(popped, 1u);
    EXPECT_EQ(ms.top(), 2);
}

TEST(MonotonicStack, NextGreaterElement) {
    // Using a decreasing monotonic stack to find next-greater-element pattern.
    // Sequence: [2, 1, 5, 3, 4]
    // After processing, remaining elements in stack should be decreasing (bottom→top).
    MonotonicStack<int, std::greater<int>> ms;
    std::vector<int> input = {2, 1, 5, 3, 4};
    //                             5  5 -1  4 -1  (next greater elements for reference)

    for (int x : input) {
        ms.push(x);
    }

    // Verify remaining elements are decreasing from top to bottom
    // i.e., popping yields non-decreasing (since we pop top first)
    int prev = -1;
    while (!ms.empty()) {
        EXPECT_GE(ms.top(), prev);
        prev = ms.top();
        ms.pop();
    }
}
