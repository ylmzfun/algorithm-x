#include "algorithm_x/ds/fibonacci_heap.h"
#include "gtest/gtest.h"
using namespace algorithm_x::ds;
namespace {
TEST(FibHeap, PushTopPop) {
    FibonacciHeap<int> h; h.push(3); h.push(1); h.push(2);
    EXPECT_EQ(h.top(), 1); h.pop(); EXPECT_EQ(h.top(), 2);
}
TEST(FibHeap, EmptyThrows) { FibonacciHeap<int> h; EXPECT_THROW(h.top(), std::out_of_range); }
TEST(FibHeap, Size) { FibonacciHeap<int> h; h.push(1); h.push(2); EXPECT_EQ(h.size(), 2u); }
TEST(FibHeap, Large) { FibonacciHeap<int> h; for (int i=0;i<500;++i) h.push(i); EXPECT_EQ(h.size(),500u); }
}  // namespace
