#include "algo/decrease_conquer.h"

#include <cstddef>
#include <vector>

#include "gtest/gtest.h"

using namespace algorithm_x::algo;

namespace {

TEST(QuickselectKth, BasicArray) {
    const std::vector<int> arr = {3, 1, 4, 1, 5, 9, 2, 6};
    // 排序后为 1, 1, 2, 3, 4, 5, 6, 9
    EXPECT_EQ(quickselect_kth(arr, 0), 1);
    EXPECT_EQ(quickselect_kth(arr, 1), 1);
    EXPECT_EQ(quickselect_kth(arr, 2), 2);
    EXPECT_EQ(quickselect_kth(arr, 3), 3);
    EXPECT_EQ(quickselect_kth(arr, 7), 9);
}

TEST(QuickselectKth, Duplicates) {
    const std::vector<int> arr = {3, 1, 3, 2, 3};
    // 排序后为 1, 2, 3, 3, 3
    EXPECT_EQ(quickselect_kth(arr, 2), 3);
    EXPECT_EQ(quickselect_kth(arr, 4), 3);
}

TEST(QuickselectKth, SingleElement) {
    const std::vector<int> arr = {42};
    EXPECT_EQ(quickselect_kth(arr, 0), 42);
}

TEST(QuickselectKth, OutOfBoundsReturnsMinusOne) {
    const std::vector<int> arr = {3, 1, 4, 1, 5, 9, 2, 6};
    EXPECT_EQ(quickselect_kth(arr, 8), -1);
    EXPECT_EQ(quickselect_kth(arr, 100), -1);
    const std::vector<int> empty;
    EXPECT_EQ(quickselect_kth(empty, 0), -1);
}

TEST(QuickselectKth, DoesNotModifyInput) {
    const std::vector<int> arr = {3, 1, 4, 1, 5, 9, 2, 6};
    (void)quickselect_kth(arr, 2);
    EXPECT_EQ(arr[0], 3);  // 按值传入，原数组不受影响
    EXPECT_EQ(arr[1], 1);
}

TEST(Josephus, StandardCases) {
    // j(1)=0, j(n)=(j(n-1)+k)%n
    EXPECT_EQ(josephus(7, 3), 3);
    EXPECT_EQ(josephus(5, 2), 2);
    EXPECT_EQ(josephus(1, 5), 0);
}

TEST(Josephus, MoreCases) {
    // josephus(6, 3) 手动推演：出列顺序 2, 5, 3, 1, 4，最后幸存者 0
    EXPECT_EQ(josephus(6, 3), 0);
    // josephus(4, 2) 手动推演：出列顺序 1, 3, 2，最后幸存者 0
    EXPECT_EQ(josephus(4, 2), 0);
    // josephus(10, 4) 递推可得 4
    EXPECT_EQ(josephus(10, 4), 4);
}

TEST(Josephus, InvalidInputReturnsMinusOne) {
    EXPECT_EQ(josephus(0, 3), -1);
    EXPECT_EQ(josephus(-2, 3), -1);
}

}  // namespace
