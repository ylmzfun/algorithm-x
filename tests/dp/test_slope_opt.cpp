#include "algorithm_x/dp/slope_opt.h"
#include "gtest/gtest.h"
using namespace algorithm_x::dp;
namespace {
TEST(ConvexHullTrick, MinimumQueries) {
    ConvexHullTrick<long long> cht;
    // y = x, y = 5, y = -x + 10（斜率递减），查询 x 递增
    cht.add_line(1, 0);
    cht.add_line(0, 5);
    cht.add_line(-1, 10);

    EXPECT_EQ(cht.query(-10), -10);
    EXPECT_EQ(cht.query(0), 0);
    EXPECT_EQ(cht.query(5), 5);
    EXPECT_EQ(cht.query(10), 0);
    EXPECT_EQ(cht.query(20), -10);
}
TEST(ConvexHullTrick, SingleLine) {
    ConvexHullTrick<long long> cht;
    cht.add_line(2, 1);
    EXPECT_EQ(cht.query(-3), -5);
    EXPECT_EQ(cht.query(4), 9);
}
TEST(ConvexHullTrick, ClearAndEmpty) {
    ConvexHullTrick<long long> cht;
    EXPECT_EQ(cht.query(1), std::numeric_limits<long long>::max());
    cht.add_line(1, 0);
    cht.clear();
    EXPECT_EQ(cht.query(1), std::numeric_limits<long long>::max());
}
}  // namespace
