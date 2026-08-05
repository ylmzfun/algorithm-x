#pragma once

#include <algorithm>
#include <cmath>
#include <cstddef>
#include <limits>
#include <map>
#include <random>
#include <vector>

namespace algorithm_x {
namespace ai {

// 蚁群算法求解 TSP。
// dist: n×n 距离矩阵。返回最优路径（顶点排列）。
inline std::vector<int> aco_tsp(const std::vector<std::vector<double>>& dist,
                                 int num_ants = 20, int iterations = 100) {
    int n = static_cast<int>(dist.size());
    if (n <= 2) {
        std::vector<int> tour(n);
        for (int i = 0; i < n; ++i) tour[i] = i;
        return tour;
    }

    const double alpha = 1.0, beta = 2.0, rho = 0.5, Q = 100.0;
    std::vector<std::vector<double>> pheromone(
        static_cast<std::size_t>(n),
        std::vector<double>(static_cast<std::size_t>(n), 1.0));

    std::mt19937 gen(42);
    std::vector<int> best_tour;
    double best_dist = std::numeric_limits<double>::max();

    for (int iter = 0; iter < iterations; ++iter) {
        for (int ant = 0; ant < num_ants; ++ant) {
            std::vector<int> tour;
            std::vector<bool> visited(static_cast<std::size_t>(n), false);
            int cur = std::uniform_int_distribution<int>(0, n - 1)(gen);
            tour.push_back(cur);
            visited[static_cast<std::size_t>(cur)] = true;

            for (int step = 1; step < n; ++step) {
                // 计算转移概率
                std::vector<double> prob(static_cast<std::size_t>(n), 0.0);
                double total = 0.0;
                for (int nxt = 0; nxt < n; ++nxt) {
                    if (visited[static_cast<std::size_t>(nxt)]) continue;
                    double d = dist[static_cast<std::size_t>(cur)]
                                   [static_cast<std::size_t>(nxt)];
                    if (d < 1e-9) d = 1e-9;
                    prob[static_cast<std::size_t>(nxt)] =
                        std::pow(pheromone[static_cast<std::size_t>(cur)]
                                          [static_cast<std::size_t>(nxt)],
                                 alpha) *
                        std::pow(1.0 / d, beta);
                    total += prob[static_cast<std::size_t>(nxt)];
                }
                // 轮盘赌选择
                double r = std::uniform_real_distribution<double>(0, total)(gen);
                double cum = 0.0;
                int chosen = -1;
                for (int nxt = 0; nxt < n; ++nxt) {
                    if (visited[static_cast<std::size_t>(nxt)]) continue;
                    cum += prob[static_cast<std::size_t>(nxt)];
                    if (cum >= r) { chosen = nxt; break; }
                }
                if (chosen == -1) chosen = n - 1;
                tour.push_back(chosen);
                visited[static_cast<std::size_t>(chosen)] = true;
                cur = chosen;
            }

            // 计算路径长度
            double len = 0.0;
            for (int i = 0; i < n; ++i) {
                int u = tour[static_cast<std::size_t>(i)];
                int v = tour[static_cast<std::size_t>((i + 1) % n)];
                len += dist[static_cast<std::size_t>(u)]
                           [static_cast<std::size_t>(v)];
            }
            if (len < best_dist) {
                best_dist = len;
                best_tour = tour;
            }

            // 更新信息素
            for (int i = 0; i < n; ++i) {
                int u = tour[static_cast<std::size_t>(i)];
                int v = tour[static_cast<std::size_t>((i + 1) % n)];
                pheromone[static_cast<std::size_t>(u)]
                         [static_cast<std::size_t>(v)] += Q / len;
                pheromone[static_cast<std::size_t>(v)]
                         [static_cast<std::size_t>(u)] += Q / len;
            }
        }

        // 挥发
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j) {
                pheromone[static_cast<std::size_t>(i)]
                         [static_cast<std::size_t>(j)] *= (1.0 - rho);
            }
        }
    }
    return best_tour;
}

// PCA — 主成分分析，降维到 k 维。
// data: n 个 d 维样本。返回 k 个主成分向量（每个长度为 d）。
inline std::vector<std::vector<double>> pca(
    const std::vector<std::vector<double>>& data, int k) {
    std::size_t n = data.size();
    if (n == 0) return {};
    std::size_t d = data[0].size();

    // 中心化
    std::vector<double> mean(d, 0.0);
    for (auto& row : data) {
        for (std::size_t j = 0; j < d; ++j) mean[j] += row[j];
    }
    for (auto& m : mean) m /= static_cast<double>(n);

    // 协方差矩阵 (d×d)
    std::vector<std::vector<double>> cov(d, std::vector<double>(d, 0.0));
    for (auto& row : data) {
        for (std::size_t i = 0; i < d; ++i) {
            for (std::size_t j = 0; j < d; ++j) {
                cov[i][j] += (row[i] - mean[i]) * (row[j] - mean[j]);
            }
        }
    }
    for (auto& row : cov) {
        for (auto& val : row) val /= static_cast<double>(n - 1);
    }

    // 幂迭代求前 k 个特征向量（简化版）
    std::vector<std::vector<double>> components;
    std::vector<std::vector<double>> residual = cov;

    for (int comp = 0; comp < k && comp < static_cast<int>(d); ++comp) {
        std::vector<double> v(d, 0.0);
        v[static_cast<std::size_t>(comp % static_cast<int>(d))] = 1.0;

        // 幂迭代
        for (int iter = 0; iter < 100; ++iter) {
            std::vector<double> nv(d, 0.0);
            for (std::size_t i = 0; i < d; ++i) {
                for (std::size_t j = 0; j < d; ++j) {
                    nv[i] += residual[i][j] * v[j];
                }
            }
            double norm = 0.0;
            for (auto x : nv) norm += x * x;
            norm = std::sqrt(norm);
            if (norm < 1e-10) break;
            for (std::size_t i = 0; i < d; ++i) nv[i] /= norm;
            v = nv;
        }
        components.push_back(v);

        // 收缩：从 residual 中减去该成分
        double eigval = 0.0;
        {
            std::vector<double> av(d, 0.0);
            for (std::size_t i = 0; i < d; ++i)
                for (std::size_t j = 0; j < d; ++j)
                    av[i] += cov[i][j] * v[j];
            for (std::size_t i = 0; i < d; ++i) eigval += v[i] * av[i];
        }
        for (std::size_t i = 0; i < d; ++i)
            for (std::size_t j = 0; j < d; ++j)
                residual[i][j] -= eigval * v[i] * v[j];
    }
    return components;
}

// 简单 2 层 MLP（ReLU 隐层 + Sigmoid 输出），二分类。
class SimpleMLP {
public:
    SimpleMLP(int input_dim, int hidden_dim = 8)
        : input_dim_(input_dim), hidden_dim_(hidden_dim) {
        std::mt19937 gen(42);
        std::normal_distribution<double> nd(0.0, 0.1);
        w1_.assign(static_cast<std::size_t>(hidden_dim),
                   std::vector<double>(static_cast<std::size_t>(input_dim)));
        b1_.assign(static_cast<std::size_t>(hidden_dim), 0.0);
        w2_.assign(static_cast<std::size_t>(hidden_dim), 0.0);
        b2_ = 0.0;
        for (int i = 0; i < hidden_dim; ++i) {
            for (int j = 0; j < input_dim; ++j) {
                w1_[static_cast<std::size_t>(i)]
                  [static_cast<std::size_t>(j)] = nd(gen);
            }
            w2_[static_cast<std::size_t>(i)] = nd(gen);
        }
    }

    double predict(const std::vector<double>& x) const {
        auto h = forward_hidden(x);
        double z = b2_;
        for (std::size_t i = 0; i < h.size(); ++i) z += w2_[i] * h[i];
        return 1.0 / (1.0 + std::exp(-z));
    }

    void fit(const std::vector<std::vector<double>>& X,
             const std::vector<int>& y,
             int epochs = 500, double lr = 0.1) {
        std::size_t n = X.size();
        for (int e = 0; e < epochs; ++e) {
            for (std::size_t s = 0; s < n; ++s) {
                // forward
                auto h = forward_hidden(X[s]);
                double z = b2_;
                for (std::size_t i = 0; i < h.size(); ++i) z += w2_[i] * h[i];
                double y_pred = 1.0 / (1.0 + std::exp(-z));

                double target = static_cast<double>(y[s]);
                double d_out = (y_pred - target);  // for BCE + sigmoid: dL/dz

                // backprop output layer
                for (std::size_t i = 0; i < h.size(); ++i) {
                    w2_[i] -= lr * d_out * h[i];
                }
                b2_ -= lr * d_out;

                // backprop hidden layer
                for (std::size_t i = 0; i < h.size(); ++i) {
                    double d_hidden = d_out * w2_[i] * (h[i] > 0 ? 1.0 : 0.0);
                    for (int j = 0; j < input_dim_; ++j) {
                        w1_[i][static_cast<std::size_t>(j)] -=
                            lr * d_hidden * X[s][static_cast<std::size_t>(j)];
                    }
                    b1_[i] -= lr * d_hidden;
                }
            }
        }
    }

private:
    std::vector<double> forward_hidden(const std::vector<double>& x) const {
        std::vector<double> h(static_cast<std::size_t>(hidden_dim_));
        for (int i = 0; i < hidden_dim_; ++i) {
            double z = b1_[static_cast<std::size_t>(i)];
            for (int j = 0; j < input_dim_; ++j) {
                z += w1_[static_cast<std::size_t>(i)]
                        [static_cast<std::size_t>(j)] *
                     x[static_cast<std::size_t>(j)];
            }
            h[static_cast<std::size_t>(i)] = std::max(0.0, z);  // ReLU
        }
        return h;
    }

    int input_dim_, hidden_dim_;
    std::vector<std::vector<double>> w1_;
    std::vector<double> b1_, w2_;
    double b2_;
};

}  // namespace ai
}  // namespace algorithm_x
