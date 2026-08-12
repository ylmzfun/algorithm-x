#include <gtest/gtest.h>

#include <functional>
#include <stdexcept>
#include <vector>

#include "ds/priority_queue.h"

using algorithm_x::ds::PriorityQueue;

// --- Max-heap (default) ---

TEST(PriorityQueue, MaxHeap_TopReturnsMax) {
    PriorityQueue<int> pq;
    pq.push(3);
    pq.push(1);
    pq.push(4);
    pq.push(1);
    pq.push(5);

    EXPECT_EQ(pq.top(), 5);
    pq.pop();
    EXPECT_EQ(pq.top(), 4);
    pq.pop();
    EXPECT_EQ(pq.top(), 3);
    pq.pop();
    EXPECT_EQ(pq.top(), 1);
    pq.pop();
    EXPECT_EQ(pq.top(), 1);
}

TEST(PriorityQueue, MinHeap_TopReturnsMin) {
    PriorityQueue<int, std::greater<int>> pq;
    pq.push(3);
    pq.push(1);
    pq.push(4);
    pq.push(1);
    pq.push(5);

    EXPECT_EQ(pq.top(), 1);
    pq.pop();
    EXPECT_EQ(pq.top(), 1);
    pq.pop();
    EXPECT_EQ(pq.top(), 3);
    pq.pop();
    EXPECT_EQ(pq.top(), 4);
    pq.pop();
    EXPECT_EQ(pq.top(), 5);
}

TEST(PriorityQueue, EmptyPopThrows) {
    PriorityQueue<int> pq;
    EXPECT_THROW(pq.pop(), std::out_of_range);
}

TEST(PriorityQueue, EmptyTopThrows) {
    PriorityQueue<int> pq;
    EXPECT_THROW(pq.top(), std::out_of_range);
}

TEST(PriorityQueue, SizeAndEmpty) {
    PriorityQueue<int> pq;
    EXPECT_TRUE(pq.empty());
    EXPECT_EQ(pq.size(), 0);

    pq.push(10);
    EXPECT_FALSE(pq.empty());
    EXPECT_EQ(pq.size(), 1);

    pq.push(20);
    EXPECT_EQ(pq.size(), 2);

    pq.pop();
    EXPECT_EQ(pq.size(), 1);

    pq.pop();
    EXPECT_TRUE(pq.empty());
}

TEST(PriorityQueue, HeapifySortOrder) {
    PriorityQueue<int> pq;
    std::vector<int> input = {7, 3, 9, 2, 8, 5, 1, 6, 4};
    for (int v : input) {
        pq.push(v);
    }

    std::vector<int> result;
    while (!pq.empty()) {
        result.push_back(pq.top());
        pq.pop();
    }

    // Max-heap should yield descending order
    for (size_t i = 1; i < result.size(); ++i) {
        EXPECT_GE(result[i - 1], result[i]);
    }
}

TEST(PriorityQueue, DuplicateValues) {
    PriorityQueue<int> pq;
    pq.push(5);
    pq.push(5);
    pq.push(3);
    pq.push(5);
    pq.push(3);

    EXPECT_EQ(pq.top(), 5);
    pq.pop();
    EXPECT_EQ(pq.top(), 5);
    pq.pop();
    EXPECT_EQ(pq.top(), 5);
    pq.pop();
    EXPECT_EQ(pq.top(), 3);
    pq.pop();
    EXPECT_EQ(pq.top(), 3);
}
