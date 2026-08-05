#pragma once

#include <algorithm>
#include <cmath>
#include <cstddef>
#include <numeric>
#include <vector>

namespace algorithm_x {
namespace ai {

// Naive Bayes — Gaussian features, binary classification (labels 0/1).
class NaiveBayes {
public:
    void fit(const std::vector<std::vector<double>>& X,
             const std::vector<int>& y) {
        std::size_t n = X.size();
        if (n == 0) return;
        dim_ = X[0].size();

        // 统计每类样本数和均值/方差
        std::size_t cnt[2] = {0, 0};
        mean_.assign(2, std::vector<double>(dim_, 0.0));
        var_.assign(2, std::vector<double>(dim_, 0.0));

        for (std::size_t i = 0; i < n; ++i) {
            int c = y[i];
            ++cnt[static_cast<std::size_t>(c)];
            for (std::size_t j = 0; j < dim_; ++j) {
                mean_[static_cast<std::size_t>(c)][j] += X[i][j];
            }
        }
        for (int c = 0; c < 2; ++c) {
            if (cnt[static_cast<std::size_t>(c)] > 0) {
                for (std::size_t j = 0; j < dim_; ++j) {
                    mean_[static_cast<std::size_t>(c)][j] /=
                        static_cast<double>(cnt[static_cast<std::size_t>(c)]);
                }
            }
        }

        for (std::size_t i = 0; i < n; ++i) {
            int c = y[i];
            for (std::size_t j = 0; j < dim_; ++j) {
                double diff = X[i][j] - mean_[static_cast<std::size_t>(c)][j];
                var_[static_cast<std::size_t>(c)][j] += diff * diff;
            }
        }
        for (int c = 0; c < 2; ++c) {
            double div = cnt[static_cast<std::size_t>(c)] > 1
                             ? static_cast<double>(cnt[static_cast<std::size_t>(c)] - 1)
                             : 1.0;
            for (std::size_t j = 0; j < dim_; ++j) {
                var_[static_cast<std::size_t>(c)][j] =
                    std::max(var_[static_cast<std::size_t>(c)][j] / div, 1e-9);
            }
        }

        prior_[0] = static_cast<double>(cnt[0]) / static_cast<double>(n);
        prior_[1] = static_cast<double>(cnt[1]) / static_cast<double>(n);
    }

    int predict_single(const std::vector<double>& x) const {
        double best_log = -std::numeric_limits<double>::max();
        int best_c = 0;
        for (int c = 0; c < 2; ++c) {
            double log_prob = std::log(prior_[static_cast<std::size_t>(c)]);
            for (std::size_t j = 0; j < dim_; ++j) {
                double diff = x[j] - mean_[static_cast<std::size_t>(c)][j];
                double v = var_[static_cast<std::size_t>(c)][j];
                log_prob += -0.5 * std::log(2.0 * M_PI * v) -
                            0.5 * diff * diff / v;
            }
            if (log_prob > best_log) {
                best_log = log_prob;
                best_c = c;
            }
        }
        return best_c;
    }

    std::vector<int> predict(const std::vector<std::vector<double>>& X) const {
        std::vector<int> result;
        for (const auto& x : X) result.push_back(predict_single(x));
        return result;
    }

private:
    std::size_t dim_ = 0;
    std::vector<std::vector<double>> mean_;
    std::vector<std::vector<double>> var_;
    double prior_[2] = {0.5, 0.5};
};

}  // namespace ai
}  // namespace algorithm_x
