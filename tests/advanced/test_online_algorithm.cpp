#include "algorithm_x/advanced/online_algorithm.h"

#include <vector>

#include "gtest/gtest.h"
using namespace algorithm_x::advanced;
namespace {
TEST(SkiRental, CostFormula) {
    // 策略：前 min(days, buy_cost-1) 天租（每天 1 元），
    // 若 days >= buy_cost 则第 buy_cost 天买（花 buy_cost 元）。
    EXPECT_EQ(ski_rental_cost(7, 3), 3);    // 租 3 天（不足买价，全租）
    EXPECT_EQ(ski_rental_cost(7, 7), 13);   // 租 6 天 + 买 7 = 13
    EXPECT_EQ(ski_rental_cost(7, 10), 13);  // 租 6 天 + 买 7 = 13
    EXPECT_EQ(ski_rental_cost(5, 2), 2);    // 租 2 天
    EXPECT_EQ(ski_rental_cost(5, 5), 9);    // 租 4 天 + 买 5 = 9
    EXPECT_EQ(ski_rental_cost(1, 10), 1);   // 买价 1：第 1 天直接买
    EXPECT_EQ(ski_rental_cost(7, 0), 0);    // 一天都不滑
}

TEST(MoveToFront, HandCalculated) {
    // 初始列表 {1,2,3}：
    // 请求 {1,2,1,3}：1 在位置 0（代价 1）-> 列表不变；
    //                 2 在位置 1（代价 2）-> {2,1,3}；
    //                 1 在位置 1（代价 2）-> {1,2,3}；
    //                 3 在位置 2（代价 3）-> {3,1,2}；总计 1+2+2+3 = 8。
    EXPECT_EQ(move_to_front_search({1, 2, 1, 3}, 3), 8);
    // 每次都请求队首元素：代价恒为 1。
    EXPECT_EQ(move_to_front_search({1, 1, 1}, 3), 3);
    // {2,1,3}：2 在位置 1（2）-> {2,1,3}；1 在位置 1（2）-> {1,2,3}；
    //          3 在位置 2（3）；总计 7。
    EXPECT_EQ(move_to_front_search({2, 1, 3}, 3), 7);
    // 全部请求队尾元素：每次代价 3，共 9。
    EXPECT_EQ(move_to_front_search({3, 2, 1}, 3), 9);
}
}  // namespace
