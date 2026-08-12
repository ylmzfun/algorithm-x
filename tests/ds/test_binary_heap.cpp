#include "ds/binary_heap.h"

#include <algorithm>
#include <gtest/gtest.h>
#include <vector>

using algorithm_x::ds::BinaryHeap;
using algorithm_x::ds::DynamicArray;

TEST(BinaryHeap, MaxHeapPushTopPop) {
    BinaryHeap<int> heap;
    heap.push(3);
    heap.push(1);
    heap.push(5);
    heap.push(2);

    EXPECT_EQ(heap.top(), 5);
    heap.pop();
    EXPECT_EQ(heap.top(), 3);
    heap.pop();
    EXPECT_EQ(heap.top(), 2);
    heap.pop();
    EXPECT_EQ(heap.top(), 1);
    heap.pop();
    EXPECT_TRUE(heap.empty());
}

TEST(BinaryHeap, MinHeapPushTopPop) {
    BinaryHeap<int, std::greater<int>> heap;
    heap.push(3);
    heap.push(1);
    heap.push(5);
    heap.push(2);

    EXPECT_EQ(heap.top(), 1);
    heap.pop();
    EXPECT_EQ(heap.top(), 2);
    heap.pop();
    EXPECT_EQ(heap.top(), 3);
    heap.pop();
    EXPECT_EQ(heap.top(), 5);
    heap.pop();
    EXPECT_TRUE(heap.empty());
}

TEST(BinaryHeap, EmptyPopThrows) {
    BinaryHeap<int> heap;
    EXPECT_THROW(heap.pop(), std::out_of_range);
}

TEST(BinaryHeap, EmptyTopThrows) {
    BinaryHeap<int> heap;
    EXPECT_THROW(heap.top(), std::out_of_range);
}

TEST(BinaryHeap, SizeAndEmpty) {
    BinaryHeap<int> heap;
    EXPECT_TRUE(heap.empty());
    EXPECT_EQ(heap.size(), 0u);

    heap.push(10);
    EXPECT_FALSE(heap.empty());
    EXPECT_EQ(heap.size(), 1u);

    heap.push(20);
    EXPECT_EQ(heap.size(), 2u);

    heap.pop();
    EXPECT_EQ(heap.size(), 1u);
}

TEST(BinaryHeap, HeapifyMaxHeap) {
    DynamicArray<int> arr = {3, 1, 5, 2, 4};
    BinaryHeap<int> heap(arr);

    EXPECT_EQ(heap.size(), 5u);
    EXPECT_EQ(heap.top(), 5);
    heap.pop();
    EXPECT_EQ(heap.top(), 4);
    heap.pop();
    EXPECT_EQ(heap.top(), 3);
    heap.pop();
    EXPECT_EQ(heap.top(), 2);
    heap.pop();
    EXPECT_EQ(heap.top(), 1);
}

TEST(BinaryHeap, HeapifyMinHeap) {
    DynamicArray<int> arr = {3, 1, 5, 2, 4};
    BinaryHeap<int, std::greater<int>> heap(arr);

    EXPECT_EQ(heap.top(), 1);
    heap.pop();
    EXPECT_EQ(heap.top(), 2);
    heap.pop();
    EXPECT_EQ(heap.top(), 3);
    heap.pop();
    EXPECT_EQ(heap.top(), 4);
    heap.pop();
    EXPECT_EQ(heap.top(), 5);
}

TEST(BinaryHeap, RandomOrderSortsCorrectlyMax) {
    BinaryHeap<int> heap;
    std::vector<int> values = {9, 4, 7, 1, 6, 3, 8, 2, 5};
    for (int v : values) heap.push(v);

    std::vector<int> result;
    while (!heap.empty()) {
        result.push_back(heap.top());
        heap.pop();
    }
    EXPECT_TRUE(std::is_sorted(result.begin(), result.end(), std::greater<int>()));
}

TEST(BinaryHeap, RandomOrderSortsCorrectlyMin) {
    BinaryHeap<int, std::greater<int>> heap;
    std::vector<int> values = {9, 4, 7, 1, 6, 3, 8, 2, 5};
    for (int v : values) heap.push(v);

    std::vector<int> result;
    while (!heap.empty()) {
        result.push_back(heap.top());
        heap.pop();
    }
    EXPECT_TRUE(std::is_sorted(result.begin(), result.end()));
}

TEST(BinaryHeap, Duplicates) {
    BinaryHeap<int> heap;
    heap.push(5);
    heap.push(5);
    heap.push(3);
    heap.push(5);

    EXPECT_EQ(heap.top(), 5);
    heap.pop();
    EXPECT_EQ(heap.top(), 5);
    heap.pop();
    EXPECT_EQ(heap.top(), 5);
    heap.pop();
    EXPECT_EQ(heap.top(), 3);
}
