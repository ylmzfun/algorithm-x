#include "algo/more_algo.h"
#include <vector>
#include "gtest/gtest.h"
using namespace algorithm_x::algo;
namespace {
TEST(BucketSort, Basic) {
    std::vector<int> v = {5, 2, 8, 1, 3};
    bucket_sort(v.begin(), v.end());
    EXPECT_TRUE(std::is_sorted(v.begin(), v.end()));
}
TEST(TernarySearch, Min) {
    auto f = [](double x) { return (x - 3.0) * (x - 3.0); };
    double x = ternary_search(-10.0, 10.0, f, 1e-6);
    EXPECT_NEAR(x, 3.0, 0.01);
}
}  // namespace
