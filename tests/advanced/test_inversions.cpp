#include "algorithm_x/advanced/inversions.h"
#include <vector>
#include "gtest/gtest.h"
using namespace algorithm_x::advanced;
namespace {
TEST(Inversions, Basic) {
    std::vector<int> arr = {2, 3, 8, 6, 1};
    EXPECT_EQ(count_inversions(arr), 5);
}
TEST(Inversions, Sorted) {
    std::vector<int> arr = {1, 2, 3};
    EXPECT_EQ(count_inversions(arr), 0);
}
}  // namespace
