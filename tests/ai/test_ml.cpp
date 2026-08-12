#include "ai/ml.h"

#include <cmath>
#include <vector>

#include "gtest/gtest.h"

using namespace algorithm_x::ai;

namespace {

TEST(KNN, PredictClass0) {
    std::vector<std::vector<double>> data = {
        {1, 1}, {1, 2}, {2, 1},  // class 0
        {5, 5}, {5, 6}, {6, 5},  // class 1
    };
    std::vector<int> labels = {0, 0, 0, 1, 1, 1};
    std::vector<double> query = {1.5, 1.5};
    EXPECT_EQ(knn_classify(data, labels, query, 3), 0);
}

TEST(KNN, PredictClass1) {
    std::vector<std::vector<double>> data = {
        {1, 1}, {1, 2}, {2, 1},
        {5, 5}, {5, 6}, {6, 5},
    };
    std::vector<int> labels = {0, 0, 0, 1, 1, 1};
    std::vector<double> query = {5.5, 5.5};
    EXPECT_EQ(knn_classify(data, labels, query, 3), 1);
}

TEST(KNN, KEquals1) {
    std::vector<std::vector<double>> data = {{0, 0}, {10, 10}};
    std::vector<int> labels = {0, 1};
    EXPECT_EQ(knn_classify(data, labels, {0.1, 0.1}, 1), 0);
}

TEST(LinearRegression, SimpleLine) {
    // y = 2*x + 3
    std::vector<std::vector<double>> X = {{1}, {2}, {3}};
    std::vector<double> y = {5, 7, 9};
    auto [w, b] = linear_regression(X, y);
    EXPECT_NEAR(w[0], 2.0, 0.1);
    EXPECT_NEAR(b, 3.0, 0.5);
}

TEST(LinearRegression, SinglePoint) {
    std::vector<std::vector<double>> X = {{4}};
    std::vector<double> y = {5};
    auto [w, b] = linear_regression(X, y);
    // With one point, should fit exactly after enough iterations
    double pred = b + w[0] * 4;
    EXPECT_NEAR(pred, 5.0, 0.5);
}

TEST(LogisticRegression, Separable2D) {
    std::vector<std::vector<double>> X = {
        {0, 0}, {0.5, 0.5}, {0, 1},   // class 0
        {5, 5}, {5.5, 5.5}, {6, 5},   // class 1
    };
    std::vector<int> y = {0, 0, 0, 1, 1, 1};
    auto [w, b] = logistic_regression(X, y);

    auto sigmoid = [](double z) { return 1.0 / (1.0 + std::exp(-z)); };
    int correct = 0;
    for (std::size_t i = 0; i < X.size(); ++i) {
        double z = b;
        for (std::size_t j = 0; j < X[i].size(); ++j) z += w[j] * X[i][j];
        int pred = sigmoid(z) >= 0.5 ? 1 : 0;
        if (pred == y[i]) ++correct;
    }
    EXPECT_GE(correct, static_cast<int>(X.size()) * 4 / 5);  // >80%
}

TEST(KMeans, TwoClusters) {
    std::vector<std::vector<double>> data = {
        {0, 0}, {0.5, 0}, {0, 0.5},   // cluster 0
        {5, 5}, {5.5, 5}, {5, 5.5},   // cluster 1
    };
    auto [labels, centroids] = kmeans(data, 2);

    EXPECT_EQ(centroids.size(), 2u);
    // First 3 and last 3 should be in different clusters
    EXPECT_NE(labels[0], labels[3]);
    EXPECT_EQ(labels[0], labels[1]);
    EXPECT_EQ(labels[0], labels[2]);
    EXPECT_EQ(labels[3], labels[4]);
    EXPECT_EQ(labels[3], labels[5]);
}

}  // namespace
