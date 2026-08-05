#include "algorithm_x/ai/decision_tree.h"
#include <vector>
#include "gtest/gtest.h"
using namespace algorithm_x::ai;
namespace {
TEST(DecisionTree, TrainPredict) {
    DecisionTree dt(3);
    std::vector<std::vector<double>> X = {{0, 0}, {0, 1}, {1, 0}, {1, 1}};
    std::vector<int> y = {0, 0, 0, 1};
    dt.fit(X, y);
    EXPECT_EQ(dt.predict_single({0, 0}), 0);
    EXPECT_EQ(dt.predict_single({1, 1}), 1);
}
}  // namespace
