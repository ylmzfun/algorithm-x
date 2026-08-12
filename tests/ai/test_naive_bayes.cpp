#include "ai/naive_bayes.h"
#include <vector>
#include "gtest/gtest.h"
using namespace algorithm_x::ai;
namespace {
TEST(NaiveBayes, TrainPredict) {
    NaiveBayes nb;
    std::vector<std::vector<double>> X = {{1.0, 2.0}, {2.0, 3.0}, {5.0, 6.0}, {6.0, 7.0}};
    std::vector<int> y = {0, 0, 1, 1};
    nb.fit(X, y);
    EXPECT_EQ(nb.predict_single({1.5, 2.5}), 0);
    EXPECT_EQ(nb.predict_single({5.5, 6.5}), 1);
}
}  // namespace
