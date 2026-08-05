#pragma once

#include <algorithm>
#include <cmath>
#include <cstddef>
#include <unordered_map>
#include <unordered_set>
#include <vector>

namespace algorithm_x {
namespace ai {

// Decision Tree — CART with Gini impurity. Binary features, binary class labels.
class DecisionTree {
    struct Node {
        int feature = -1;      // 分裂特征索引，-1 表示叶子
        int label = 0;         // 叶子节点的预测类别
        Node* left = nullptr;
        Node* right = nullptr;
        ~Node() { delete left; delete right; }
    };

public:
    DecisionTree(int max_depth = 5) : max_depth_(max_depth) {}
    ~DecisionTree() { delete root_; }

    void fit(const std::vector<std::vector<double>>& X,
             const std::vector<int>& y) {
        root_ = build(X, y, 0);
    }

    int predict_single(const std::vector<double>& x) const {
        Node* cur = root_;
        while (cur && cur->feature != -1) {
            cur = (x[static_cast<std::size_t>(cur->feature)] < 0.5)
                      ? cur->left
                      : cur->right;
        }
        return cur ? cur->label : 0;
    }

    std::vector<int> predict(const std::vector<std::vector<double>>& X) const {
        std::vector<int> result;
        for (const auto& x : X) result.push_back(predict_single(x));
        return result;
    }

private:
    double gini(const std::vector<int>& labels) const {
        if (labels.empty()) return 0;
        double cnt[2] = {0, 0};
        for (int y : labels) ++cnt[static_cast<std::size_t>(y)];
        double n = static_cast<double>(labels.size());
        double p0 = cnt[0] / n, p1 = cnt[1] / n;
        return 1.0 - p0 * p0 - p1 * p1;
    }

    Node* build(const std::vector<std::vector<double>>& X,
                const std::vector<int>& y, int depth) {
        auto* node = new Node();
        // 统计多数类
        int cnt[2] = {0, 0};
        for (int label : y) ++cnt[static_cast<std::size_t>(label)];
        int majority = cnt[0] > cnt[1] ? 0 : 1;

        // 停止条件
        if (depth >= max_depth_ || cnt[0] == 0 || cnt[1] == 0 ||
            X.size() <= 1) {
            node->label = majority;
            return node;
        }

        // 选最佳分裂特征
        std::size_t n = X.size(), dim = X[0].size();
        double best_gini = 1.0;
        int best_feat = -1;

        for (std::size_t f = 0; f < dim; ++f) {
            std::vector<int> left_y, right_y;
            for (std::size_t i = 0; i < n; ++i) {
                if (X[i][f] < 0.5)
                    left_y.push_back(y[i]);
                else
                    right_y.push_back(y[i]);
            }
            if (left_y.empty() || right_y.empty()) continue;
            double g = (left_y.size() * gini(left_y) +
                        right_y.size() * gini(right_y)) /
                       static_cast<double>(n);
            if (g < best_gini) {
                best_gini = g;
                best_feat = static_cast<int>(f);
            }
        }

        if (best_feat == -1) {
            node->label = majority;
            return node;
        }

        node->feature = best_feat;
        std::vector<std::vector<double>> left_X, right_X;
        std::vector<int> left_y, right_y;
        for (std::size_t i = 0; i < n; ++i) {
            if (X[i][static_cast<std::size_t>(best_feat)] < 0.5) {
                left_X.push_back(X[i]);
                left_y.push_back(y[i]);
            } else {
                right_X.push_back(X[i]);
                right_y.push_back(y[i]);
            }
        }
        node->left = build(left_X, left_y, depth + 1);
        node->right = build(right_X, right_y, depth + 1);
        return node;
    }

    Node* root_ = nullptr;
    int max_depth_;
};

}  // namespace ai
}  // namespace algorithm_x
