#include "ai/more_ai.h"
#include <vector>
#include "gtest/gtest.h"
using namespace algorithm_x::ai;
namespace {
TEST(ACO, TSP) {
    std::vector<std::vector<double>> dist = {{0, 10, 15}, {10, 0, 20}, {15, 20, 0}};
    auto tour = aco_tsp(dist, 20, 100);
    EXPECT_EQ(tour.size(), 3u);
}
TEST(PCA, Components) {
    std::vector<std::vector<double>> data = {{1.0, 2.0}, {2.0, 3.0}, {3.0, 4.0}};
    auto components = pca(data, 1);
    EXPECT_EQ(components.size(), 1u);
    EXPECT_EQ(components[0].size(), 2u);
}
TEST(MLP, XOR) {
    SimpleMLP mlp(2, 4);
    std::vector<std::vector<double>> X = {{0,0},{0,1},{1,0},{1,1}};
    std::vector<int> y = {0,1,1,0};
    mlp.fit(X, y, 2000);
    for (int i = 0; i < 4; ++i) {
        double pred = mlp.predict(X[static_cast<std::size_t>(i)]);
        EXPECT_NEAR(pred, y[i], 0.3);
    }
}
}  // namespace
