#include "algo/interpolation_search.h"
#include <vector>
#include "gtest/gtest.h"
using namespace algorithm_x::algo;
namespace {
TEST(InterpSearch, Found) {
    std::vector<int> v = {10, 20, 30, 40, 50};
    EXPECT_EQ(*interpolation_search(v.begin(), v.end(), 30), 30);
}
TEST(InterpSearch, NotFound) {
    std::vector<int> v = {10, 20, 30};
    EXPECT_EQ(interpolation_search(v.begin(), v.end(), 25), v.end());
}
TEST(InterpSearch, FirstLast) {
    std::vector<int> v = {10, 20, 30};
    EXPECT_EQ(*interpolation_search(v.begin(), v.end(), 10), 10);
    EXPECT_EQ(*interpolation_search(v.begin(), v.end(), 30), 30);
}
}  // namespace
