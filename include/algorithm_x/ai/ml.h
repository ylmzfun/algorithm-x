#pragma once

#include <algorithm>
#include <cmath>
#include <cstddef>
#include <numeric>
#include <queue>
#include <random>
#include <vector>

namespace algorithm_x {
namespace ai {

// K 近邻分类 — 多数表决。
// train_data: 训练样本; train_labels: 对应标签;
// query: 待分类点; k: 邻居数。
inline int knn_classify(const std::vector<std::vector<double>>& train_data,
                         const std::vector<int>& train_labels,
                         const std::vector<double>& query, int k = 3) {
    std::size_t n = train_data.size();
    std::vector<std::pair<double, int>> dists;
    for (std::size_t i = 0; i < n; ++i) {
        double d = 0;
        for (std::size_t j = 0; j < query.size(); ++j) {
            double diff = train_data[i][j] - query[j];
            d += diff * diff;
        }
        dists.emplace_back(d, train_labels[i]);
    }
    std::sort(dists.begin(), dists.end());

    // 多数表决
    std::vector<int> votes(10, 0);  // assume labels 0..9
    for (int i = 0; i < k && i < static_cast<int>(dists.size()); ++i) {
        ++votes[static_cast<std::size_t>(dists[static_cast<std::size_t>(i)].second)];
    }
    return static_cast<int>(
        std::max_element(votes.begin(), votes.end()) - votes.begin());
}

// 线性回归 — y = w·x + b，最小二乘闭式解。
// 返回 {weights, bias}。
inline std::pair<std::vector<double>, double>
linear_regression(const std::vector<std::vector<double>>& X,
                   const std::vector<double>& y) {
    std::size_t n = X.size(), d = X[0].size();

    // X^T X w = X^T y (centered: no bias term for simplicity)
    // We use gradient descent for header-only simplicity
    std::vector<double> w(d, 0);
    double b = 0;
    double lr = 0.01;

    for (int iter = 0; iter < 5000; ++iter) {
        std::vector<double> dw(d, 0);
        double db = 0;
        for (std::size_t i = 0; i < n; ++i) {
            double pred = b;
            for (std::size_t j = 0; j < d; ++j) pred += w[j] * X[i][j];
            double error = pred - y[i];
            for (std::size_t j = 0; j < d; ++j) dw[j] += error * X[i][j];
            db += error;
        }
        for (std::size_t j = 0; j < d; ++j) w[j] -= lr * dw[j] / static_cast<double>(n);
        b -= lr * db / static_cast<double>(n);
    }
    return {w, b};
}

// 逻辑回归 — 二分类，返回 {weights, bias}。
// y[i] 为 0 或 1。
inline std::pair<std::vector<double>, double>
logistic_regression(const std::vector<std::vector<double>>& X,
                     const std::vector<int>& y) {
    std::size_t n = X.size(), d = X[0].size();
    std::vector<double> w(d, 0);
    double b = 0, lr = 0.1;

    auto sigmoid = [](double z) { return 1.0 / (1.0 + std::exp(-z)); };

    for (int iter = 0; iter < 2000; ++iter) {
        std::vector<double> dw(d, 0);
        double db = 0;
        for (std::size_t i = 0; i < n; ++i) {
            double z = b;
            for (std::size_t j = 0; j < d; ++j) z += w[j] * X[i][j];
            double pred = sigmoid(z);
            double error = pred - static_cast<double>(y[i]);
            for (std::size_t j = 0; j < d; ++j) dw[j] += error * X[i][j];
            db += error;
        }
        for (std::size_t j = 0; j < d; ++j) w[j] -= lr * dw[j] / static_cast<double>(n);
        b -= lr * db / static_cast<double>(n);
    }
    return {w, b};
}

// K-Means 聚类 — 返回 {labels, centroids}。
inline std::pair<std::vector<int>, std::vector<std::vector<double>>>
kmeans(const std::vector<std::vector<double>>& data, int k,
       int max_iter = 100) {
    std::size_t n = data.size(), d = data[0].size();
    std::vector<int> labels(n, 0);
    std::vector<std::vector<double>> centroids(
        static_cast<std::size_t>(k), std::vector<double>(d));

    // 随机选 k 个点作为初始质心
    std::mt19937 gen(42);
    std::uniform_int_distribution<int> dis(0, n - 1);
    for (int c = 0; c < k; ++c) {
        centroids[static_cast<std::size_t>(c)] = data[dis(gen)];
    }

    for (int iter = 0; iter < max_iter; ++iter) {
        bool changed = false;
        for (std::size_t i = 0; i < n; ++i) {
            int best_c = 0;
            double best_d = std::numeric_limits<double>::max();
            for (int c = 0; c < k; ++c) {
                double dist = 0;
                for (std::size_t j = 0; j < d; ++j) {
                    double diff = data[i][j] -
                                  centroids[static_cast<std::size_t>(c)][j];
                    dist += diff * diff;
                }
                if (dist < best_d) {
                    best_d = dist;
                    best_c = c;
                }
            }
            if (labels[i] != best_c) {
                labels[i] = best_c;
                changed = true;
            }
        }
        if (!changed) break;

        // 更新质心
        std::vector<int> cnt(static_cast<std::size_t>(k), 0);
        for (auto& c : centroids) std::fill(c.begin(), c.end(), 0.0);
        for (std::size_t i = 0; i < n; ++i) {
            int c = labels[i];
            for (std::size_t j = 0; j < d; ++j) {
                centroids[static_cast<std::size_t>(c)][j] += data[i][j];
            }
            ++cnt[static_cast<std::size_t>(c)];
        }
        for (int c = 0; c < k; ++c) {
            if (cnt[static_cast<std::size_t>(c)] > 0) {
                for (std::size_t j = 0; j < d; ++j) {
                    centroids[static_cast<std::size_t>(c)][j] /=
                        static_cast<double>(cnt[static_cast<std::size_t>(c)]);
                }
            }
        }
    }
    return {labels, centroids};
}

}  // namespace ai
}  // namespace algorithm_x
