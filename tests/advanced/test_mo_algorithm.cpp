#include "advanced/mo_algorithm.h"
#include <vector>
#include "gtest/gtest.h"
using namespace algorithm_x::advanced;
namespace {
TEST(MoAlgorithm, DistinctCount) {
    std::vector<int> arr = {1, 1, 2, 2, 3};
    std::vector<MoQuery> queries = {{0, 1, 0}, {2, 3, 1}, {0, 4, 2}};
    auto ans = mo_algorithm(arr, queries);
    EXPECT_EQ(ans[0], 1); // {1,1} distinct=1
    EXPECT_EQ(ans[1], 1); // {2,2} distinct=1
    EXPECT_EQ(ans[2], 3); // {1,1,2,2,3} distinct=3
}
}  // namespace
