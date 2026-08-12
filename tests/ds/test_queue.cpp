#include <gtest/gtest.h>
#include <stdexcept>
#include "ds/queue.h"

using namespace algorithm_x::ds;

// ==================== Queue ====================

TEST(Queue, FifoOrder) {
    Queue<int> q;
    q.push(1);
    q.push(2);
    q.push(3);
    EXPECT_EQ(q.front(), 1);
    q.pop();
    EXPECT_EQ(q.front(), 2);
    q.pop();
    EXPECT_EQ(q.front(), 3);
    q.pop();
    EXPECT_TRUE(q.empty());
}

TEST(Queue, FrontBack) {
    Queue<int> q;
    q.push(10);
    q.push(20);
    q.push(30);
    EXPECT_EQ(q.front(), 10);
    EXPECT_EQ(q.back(), 30);
    q.pop();
    EXPECT_EQ(q.front(), 20);
    EXPECT_EQ(q.back(), 30);
}

TEST(Queue, EmptyPopThrows) {
    Queue<int> q;
    EXPECT_THROW(q.pop(), std::out_of_range);
    EXPECT_THROW(q.front(), std::out_of_range);
    EXPECT_THROW(q.back(), std::out_of_range);
}

TEST(Queue, SizeAndEmpty) {
    Queue<int> q;
    EXPECT_TRUE(q.empty());
    EXPECT_EQ(q.size(), 0u);
    q.push(1);
    EXPECT_FALSE(q.empty());
    EXPECT_EQ(q.size(), 1u);
    q.push(2);
    EXPECT_EQ(q.size(), 2u);
    q.pop();
    EXPECT_EQ(q.size(), 1u);
    q.pop();
    EXPECT_EQ(q.size(), 0u);
    EXPECT_TRUE(q.empty());
}

// ==================== Deque ====================

TEST(Deque, PushFrontBack) {
    Deque<int> d;
    d.push_back(2);
    d.push_front(1);
    d.push_back(3);
    // Expected: 1 2 3
    EXPECT_EQ(d[0], 1);
    EXPECT_EQ(d[1], 2);
    EXPECT_EQ(d[2], 3);
}

TEST(Deque, PopFrontBack) {
    Deque<int> d;
    d.push_back(1);
    d.push_back(2);
    d.push_back(3);

    d.pop_front();
    EXPECT_EQ(d.front(), 2);

    d.pop_back();
    EXPECT_EQ(d.back(), 2);

    d.pop_front();
    EXPECT_TRUE(d.empty());
}

TEST(Deque, SubscriptAccess) {
    Deque<int> d;
    for (int i = 0; i < 5; ++i) d.push_back(i * 10);
    for (int i = 0; i < 5; ++i) {
        EXPECT_EQ(d[i], i * 10);
    }
    d[2] = 99;
    EXPECT_EQ(d[2], 99);
}

TEST(Deque, FrontBack) {
    Deque<int> d;
    d.push_front(10);
    d.push_back(20);
    EXPECT_EQ(d.front(), 10);
    EXPECT_EQ(d.back(), 20);
}

TEST(Deque, CircularBufferWrapAround) {
    Deque<int> d;
    // Push 3 to front, 3 to back — this shifts head backwards across boundary
    d.push_back(4);
    d.push_back(5);
    d.push_back(6);
    d.push_front(3);
    d.push_front(2);
    d.push_front(1);
    // Expected: 1 2 3 4 5 6

    EXPECT_EQ(d.size(), 6u);
    for (int i = 0; i < 6; ++i) {
        EXPECT_EQ(d[i], i + 1);
    }

    // Pop from front and back to test wrap-around in both directions
    d.pop_front();
    d.pop_front();
    d.pop_back();
    // Expected: 3 4 5
    EXPECT_EQ(d.size(), 3u);
    EXPECT_EQ(d[0], 3);
    EXPECT_EQ(d[1], 4);
    EXPECT_EQ(d[2], 5);
}

TEST(Deque, Copy) {
    Deque<int> d;
    d.push_back(1);
    d.push_back(2);
    d.push_back(3);

    Deque<int> d2(d);
    EXPECT_EQ(d2.size(), 3u);
    EXPECT_EQ(d2[0], 1);
    EXPECT_EQ(d2[1], 2);
    EXPECT_EQ(d2[2], 3);

    d[0] = 99;
    EXPECT_EQ(d2[0], 1);  // deep copy
}

TEST(Deque, Move) {
    Deque<int> d;
    d.push_back(1);
    d.push_back(2);

    Deque<int> d2(std::move(d));
    EXPECT_EQ(d2.size(), 2u);
    EXPECT_EQ(d2[0], 1);
    EXPECT_EQ(d.size(), 0u);
}

TEST(Deque, LargeResize) {
    Deque<int> d;
    // Initial capacity is 4; push 100 elements to trigger multiple resizes
    for (int i = 0; i < 100; ++i) {
        if (i % 2 == 0) {
            d.push_back(i);
        } else {
            d.push_front(-i);
        }
    }
    EXPECT_EQ(d.size(), 100u);

    // Pop all
    while (!d.empty()) {
        d.pop_back();
    }
    EXPECT_TRUE(d.empty());
}
