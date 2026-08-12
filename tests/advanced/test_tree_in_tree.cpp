#include "algorithm_x/advanced/tree_in_tree.h"

#include <cstdint>
#include <vector>

#include "gtest/gtest.h"
using namespace algorithm_x::advanced;
namespace {
TEST(SqrtDecomp, RangeSum) {
    std::vector<int64_t> data = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    SqrtDecomp sd(data);
    EXPECT_EQ(sd.range_sum(2, 5), 18);   // 3+4+5+6
    EXPECT_EQ(sd.range_sum(0, 9), 55);   // 全区间 1..10
    EXPECT_EQ(sd.range_sum(4, 4), 5);    // 单点
    EXPECT_EQ(sd.range_sum(0, 0), 1);
    EXPECT_EQ(sd.range_sum(9, 9), 10);
    EXPECT_EQ(sd.range_sum(5, 2), 0);    // 非法区间（l > r）返回 0
}

TEST(SqrtDecomp, PointUpdate) {
    std::vector<int64_t> data = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    SqrtDecomp sd(data);
    sd.point_update(3, 10);  // data[3] = 4 -> 14
    EXPECT_EQ(sd.range_sum(2, 5), 28);  // 3+14+5+6
    sd.point_update(0, -1);  // data[0] = 1 -> 0
    EXPECT_EQ(sd.range_sum(0, 0), 0);
    EXPECT_EQ(sd.range_sum(0, 9), 64);  // 55 + 10 - 1
}

TEST(FenwickOfSets, CountLessEqual) {
    std::vector<int> values = {1, 5, 2, 4, 3};
    FenwickOfSets fos(values);
    EXPECT_EQ(fos.count_less_equal(2, 3), 2u);  // {1,5,2} 中 ≤3：{1,2}
    EXPECT_EQ(fos.count_less_equal(4, 3), 3u);  // {1,5,2,4,3} 中 ≤3：{1,2,3}
    EXPECT_EQ(fos.count_less_equal(0, 0), 0u);  // {1} 中 ≤0：无
    EXPECT_EQ(fos.count_less_equal(4, 4), 4u);  // ≤4：{1,2,3,4}
    EXPECT_EQ(fos.count_less_equal(4, 5), 5u);  // ≤5：全部
    EXPECT_EQ(fos.count_less_equal(2, 0), 0u);  // {1,5,2} 中 ≤0：无
}
}  // namespace
